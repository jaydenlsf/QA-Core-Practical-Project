pipeline {
    agent any
    environment {

    }
    stages {
        stage('Test') {
            steps {
                sh 'bash jenkins/test.sh'
            }
        }
        stage('Build') {
            steps {
                sh 'bash jenkins/deploy.sh'
            }
        }
        stage('Push') {
            steps {
                sh 'docker-compose push'
            }
        }
        stage('Run') {
            steps {
                // steps here
            }
        }
    }
    post {
        junit '**/*.xml'
        cobertura coberturaReportFile: 'coverage.xml', failNoReports: false
    }
}