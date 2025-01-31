pipeline {
  agent any  // Run directly on the Jenkins host machine

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
          bat 'pip install -r requirements.txt'  // Windows batch command
        }
      }
    }

    stage('Static Code Analysis with SonarQube') {
      steps {
        script {
          echo "Running static code analysis with SonarQube"
          bat '''
            sonar-scanner ^
              -Dsonar.projectKey=Spam-Detection-Project ^
              -Dsonar.sources=. ^
              -Dsonar.host.url=http://localhost:9000 ^
              -Dsonar.login=%sonarQube%
          '''
        }
      }
    }

    stage('Build and Push Docker Image') {
      environment {
        DOCKER_IMAGE = "manuagasimani/django-app:%BUILD_NUMBER%"  // Image tag with Jenkins build number
        REGISTRY_CREDENTIALS = credentials('docker-cred')  // Docker credentials from Jenkins
      }
      steps {
        script {
          echo "Building Docker image"
          bat '''
            docker build -t %DOCKER_IMAGE% .
          '''
          echo "Pushing Docker image to registry"
          bat '''
            docker login -u "%REGISTRY_CREDENTIALS_USR%" -p "%REGISTRY_CREDENTIALS_PSW%"
            docker push %DOCKER_IMAGE%
          '''
        }
      }
    }

    stage('Deploy Application') {
      steps {
        script {
          echo "Deploying application to Kubernetes"
          bat '''
            kubectl apply -f k8s/deployment.yaml
            kubectl apply -f k8s/service.yaml
          '''
        }
      }
    }
  }
}
