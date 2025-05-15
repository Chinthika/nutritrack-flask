pipeline {
    agent any

    environment {
        APP_NAME = "nutritrack-flask"
    }

    stages {
        stage('Build') {
            steps {
                echo "Installing dependencies"
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo "Running tests"
                sh 'pytest tests'
            }
        }

        stage('Code Quality') {
            steps {
                echo "Running flake8"
                sh 'flake8 app'
            }
        }

        stage('Security Scan') {
            steps {
                echo "Running bandit"
                sh 'bandit -r app || true'
            }
        }

        stage('Deploy to Test') {
            steps {
                echo "Deploying app using Docker Compose"
                sh 'docker-compose up -d --build'
            }
        }

        stage('Monitoring') {
            steps {
                echo "Checking /health endpoint"
                sh 'sleep 5 && curl -f http://localhost:5000/health || echo "Health check failed"'
            }
        }
    }

    post {
        always {
            echo "Cleaning up"
            sh 'docker-compose down || true'
        }
    }
}
