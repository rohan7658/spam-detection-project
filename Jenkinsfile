pipeline {
  agent none

  environment {
    DOCKER_IMAGE = "python:3.9"
    REGISTRY_CREDENTIALS = credentials('docker')
  }

  stages {
    stage('Checkout') {
      agent { label 'docker' }
      steps {
        script {
          echo "Cloning the repository"
          git branch: 'main', url: 'https://github.com/manuCprogramming/spam-detection-project.git'
        }
      }
    }

    stage('Build and Test') {
      agent {
        docker {
          image "${DOCKER_IMAGE}"
          args "-v ${env.WORKSPACE}:${env.WORKSPACE}"  // Ensure volume mount uses the correct absolute path
        }
      }
      steps {
        script {
          // Normalize the path for Windows
          def workspaceDir = "${env.WORKSPACE}".replace('\\', '/')
          echo "Normalized workspace path: ${workspaceDir}"
          
          echo "Installing dependencies"
          sh 'pip install -r requirements.txt'

          echo "Running tests"
          sh 'pytest tests/'
        }
      }
    }

    stage('Build Docker Image') {
      agent {
        docker {
          image "${DOCKER_IMAGE}"
          args "-v ${env.WORKSPACE}:${env.WORKSPACE}"
        }
      }
      steps {
        script {
          def workspaceDir = "${env.WORKSPACE}".replace('\\', '/')
          echo "Normalized workspace path for docker build: ${workspaceDir}"

          echo "Building Docker image"
          sh 'docker build -t ${DOCKER_IMAGE} .'

          echo "Pushing Docker image to registry"
          docker.withRegistry('https://index.docker.io/v1/', 'docker') {
            sh 'docker push ${DOCKER_IMAGE}'
          }
        }
      }
    }

    stage('Deploy') {
      agent {
        docker {
          image "${DOCKER_IMAGE}"
          args "-v ${env.WORKSPACE}:${env.WORKSPACE}"
        }
      }
      steps {
        script {
          def workspaceDir = "${env.WORKSPACE}".replace('\\', '/')
          echo "Normalized workspace path for kubectl deploy: ${workspaceDir}"

          echo "Deploying to Kubernetes"
          sh 'kubectl apply -f k8s/deployment.yaml'
          sh 'kubectl apply -f k8s/service.yaml'
        }
      }
    }
  }
}
