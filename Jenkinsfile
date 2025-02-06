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
                    docker run --rm ^
                    -v %CD%:/usr/src ^
                    sonarsource/sonar-scanner-cli:latest ^
                    -Dsonar.projectKey=Spam-Detection-Project ^
                    -Dsonar.sources=/usr/src ^
                    -Dsonar.host.url=http://host.docker.internal:9000 ^
                    -Dsonar.login=%sonarQ%
                '''
        }
      }
    }
  }
}
