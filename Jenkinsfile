pipeline {
  agent {
    docker {
      image 'python:3.9'  // Python Docker image for Django
      args '--user root'  // Running as root to avoid permission issues
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
          pwsh 'pip install -r requirements.txt'  // Using PowerShell for pip installation
        }
      }
    }

    stage('Static Code Analysis with SonarQube') {
      steps {
        script {
          echo "Running static code analysis with SonarQube"
          pwsh '''
            sonar-scanner `
              -Dsonar.projectKey=Spam-Detection-Project `
              -Dsonar.sources=. `
              -Dsonar.host.url=http://localhost:9000 `
              -Dsonar.login=$Env:sonarQube
          '''
        }
      }
    }

    stage('Build and Push Docker Image') {
      environment {
        DOCKER_IMAGE = "manuagasimani/django-app:${BUILD_NUMBER}"  // Image tag with Jenkins build number
        REGISTRY_CREDENTIALS = credentials('docker')  // Docker credentials ID from Jenkins credentials store
      }
      steps {
        script {
          echo "Building Docker image"
          pwsh '''
            docker build -t ${Env:DOCKER_IMAGE} .
          '''
          echo "Tagging and pushing Docker image"
          pwsh '''
            docker tag ${Env:DOCKER_IMAGE} manuagasimani/django-app:${Env:BUILD_NUMBER}
            docker login -u "$Env:REGISTRY_CREDENTIALS_USR" -p "$Env:REGISTRY_CREDENTIALS_PSW"
            docker push manuagasimani/django-app:${Env:BUILD_NUMBER}
          '''
        }
      }
    }

    stage('Deploy Application') {
      steps {
        script {
          echo "Deploying application to Kubernetes"
          pwsh '''
            kubectl apply -f k8s/deployment.yaml
            kubectl apply -f k8s/service.yaml
          '''
        }
      }
    }
  }
}
