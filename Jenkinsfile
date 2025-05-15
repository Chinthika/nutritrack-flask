pipeline {
  agent any

  options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
    ansiColor('xterm')
  }

  environment {
    PATH = "${env.HOME}/.local/bin:${env.PATH}"
    IMAGE_TAG = "nutritrack:${env.BUILD_NUMBER}"
  }

  stages {

    /* ---------- BUILD ---------- */
    stage('Build') {
      steps {
        echo 'Installing dependencies & building artefact'
        sh 'pip install --break-system-packages -r requirements.txt'
        sh "docker build -t $IMAGE_TAG ."
        archiveArtifacts artifacts: 'Dockerfile', fingerprint: true
      }
    }

    /* ---------- TEST ---------- */
    stage('Test') {
      steps {
        echo 'Running unit & integration tests'
        sh 'PYTHONPATH=. pytest -q --junitxml=test-report.xml'
        junit 'test-report.xml'
      }
    }

    /* ---------- CODE QUALITY ---------- */
    stage('Code Quality') {
      steps {
        echo 'flake8 with quality gate'
        // capture output to count violations
        script {
          def out = sh(returnStatus: true, script: 'flake8 app | tee flake8.txt')
          archiveArtifacts 'flake8.txt'
          if (out != 0) {
            error "Flake8 threshold breached – fix style issues."
          }
        }
      }
    }

    /* ---------- SECURITY ---------- */
    stage('Security Scan') {
      steps {
        echo 'Bandit static analysis'
        script {
          def out = sh(returnStatus: true,
                       script: 'bandit -r app -ll -o bandit-report.json -f json')
          archiveArtifacts 'bandit-report.json'
          // Allow LOW, fail on MEDIUM / HIGH
          if (out != 0) {
            error "Bandit found MEDIUM/HIGH severity issues – see report."
          }
        }
      }
    }

    /* ---------- DEPLOY (Staging) ---------- */
    stage('Deploy to Test') {
      steps {
        echo 'docker-compose up – staging environment'
        sh 'docker-compose -f docker-compose.yml --project-name nutritrack-test up -d --build'
      }
    }

    /* ---------- RELEASE (Prod) ---------- */
    stage('Release to Prod') {
      steps {
        echo 'Tag & push image'
        sh """
           docker tag $IMAGE_TAG nutritrack-prod:$BUILD_NUMBER
           docker-compose -f docker-compose.yml --project-name nutritrack-prod up -d
        """
      }
    }

    /* ---------- MONITORING ---------- */
    stage('Monitoring') {
      steps {
        echo 'Health-check endpoint & simulate alert'
        script {
          def status = sh(returnStatus: true, script: 'curl -sf http://localhost:5000/health')
          if (status != 0) {
            echo 'ALERT: /health endpoint failed – incident simulated.'
          } else {
            echo 'Health-check OK'
          }
        }
      }
    }
  }

  post {
    success {
      echo 'Pipeline complete – all stages passed.'
    }
    failure {
      echo 'Pipeline failed – investigate stage logs.'
    }
    always {
      echo 'Cleaning Docker test stack'
      sh 'docker-compose -f docker-compose.yml --project-name nutritrack-test down || true'
    }
  }
}
