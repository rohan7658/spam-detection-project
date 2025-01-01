pipeline {
  agent {
    docker {
      image 'python:3.9'  // Python Docker image for Django
      args '-u root -v /var/run/docker.sock:/var/run/docker.sock' // Root user and mount Docker socket for Docker operations
    }
  }
  stages {
    stage('Checkout') {
      steps {
        script {
          echo "Cloning the repository"
          git branch: 'main', url: 'https://github.com/manuCprogramming/spam-detection-project.git' 
        }
      }
    }

    stage('Install Dependencies') {
      steps {
        script {
          echo "Installing dependencies"
          sh 'pip install -r requirements.txt'  // Install project dependencies from requirements.txt
        }
      }
    }

    stage('Static Code Analysis with SonarQube') {
      steps {
        script {
          echo "Running static code analysis with SonarQube"
          sh '''
            sonar-scanner \
              -Dsonar.projectKey=Spam-Detection-Project \
              -Dsonar.sources=. \
              -Dsonar.host.url=http://localhost:9000 \
              -Dsonar.login=$sonarQube
          '''
        }
      }
    }

    stage('Build and Push Docker Image') {
      environment {
        DOCKER_IMAGE = "manuagasimani/django-app:${BUILD_NUMBER}"  // Image tag with Jenkins build number
        REGISTRY_CREDENTIALS = credentials('docker-cred')  // Docker credentials ID from Jenkins credentials store
      }
      steps {
        script {
          echo "Building Docker image"
          sh 'docker build -t ${DOCKER_IMAGE} .'  // Build Docker image for the project
          echo "Pushing Docker image to registry"
          docker.withRegistry('https://index.docker.io/v1/', 'docker-cred') {  // Push to DockerHub
            sh 'docker push ${DOCKER_IMAGE}'
          }
        }
      }
    }

    stage('Deploy Application') {
      steps {
        script {
          echo "Deploying application to Kubernetes"
          sh '''
            kubectl apply -f k8s/deployment.yaml  // Apply Kubernetes deployment
            kubectl apply -f k8s/service.yaml     // Apply Kubernetes service
          '''
        }
      }
    }
  }
}
