pipeline {
  agent none

  environment {
    DOCKER_IMAGE = "python:3.9"
    REGISTRY_CREDENTIALS = credentials('docker-cred')
    WORKSPACE_DIR = "${WORKSPACE.replace('\\', '/')" } 
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
          args "-v ${WORKSPACE_DIR}:${WORKSPACE_DIR}"  // Ensure volume mount uses the correct absolute path
        }
      }
      steps {
        script {
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
          args "-v ${WORKSPACE_DIR}:${WORKSPACE_DIR}"
        }
      }
      steps {
        script {
          echo "Building Docker image"
          sh 'docker build -t ${DOCKER_IMAGE} .'

          echo "Pushing Docker image to registry"
          docker.withRegistry('https://index.docker.io/v1/', 'docker-cred') {
            sh 'docker push ${DOCKER_IMAGE}'
          }
        }
      }
    }

    stage('Deploy') {
      agent {
        docker {
          image "${DOCKER_IMAGE}"
          args "-v ${WORKSPACE_DIR}:${WORKSPACE_DIR}"
        }
      }
      steps {
        script {
          echo "Deploying to Kubernetes"
          sh 'kubectl apply -f k8s/deployment.yaml'
          sh 'kubectl apply -f k8s/service.yaml'
        }
      }
    }
  }
}
