pipeline {
  agent any

  environment {
    PATH = "${env.HOME}/.local/bin:${env.PATH}"
  }

  stages {

    stage('Build') {
      steps {
        echo 'Installing dependencies'
        sh 'pip install --break-system-packages -r requirements.txt'
      }
    }

    stage('Test') {
      steps {
        echo 'Running tests'
        sh 'PYTHONPATH=. pytest tests'
      }
    }

    stage('Code Quality') {
      steps {
        echo 'Running flake8'
        sh 'flake8 app'
      }
    }

    stage('Security Scan') {
      steps {
        echo 'Running bandit'
        sh 'bandit -r app -f json -o bandit-report.json || true'
      }
    }

    stage('Deploy to Test') {
      steps {
        echo 'Deploying app using Docker Compose'
        sh 'docker-compose up -d --build || echo "Docker deploy skipped (permission denied in Jenkins container)"'
      }
    }

    stage('Release to Prod') {
      steps {
        echo 'Promoting build to production environment...'
        sh 'echo "Simulated release to production complete"'
      }
    }

    stage('Monitoring') {
      steps {
        echo 'Simulating production monitoring...'
        sh '''
          curl --fail http://localhost:5000/health || echo "ALERT: App is down!"
        '''
      }
    }
  }

  post {
    always {
      echo 'Cleaning up'
      // You can add cleanup commands if needed
    }
  }
}
