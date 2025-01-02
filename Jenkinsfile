pipeline {
    agent {
        docker {
            image 'python:3.9'
            args '-u root -v /var/run/docker.sock:/var/run/docker.sock -w /workspace/Django_Pipeline'
        }
    }
    stages {
        stage('Test Docker') {
            steps {
                script {
                    sh 'docker --version'
                }
            }
        }
    }
}
