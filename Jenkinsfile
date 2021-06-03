pipeline {
    agent any
    environment {
        DATABASE_URI = credentials("DATABASE_URI_COVID")
        username = credentials("USERNAME")
        password = credentials("PASSWORD")
    }
    stages {
        stage('Test') {
            steps {
                sh 'bash Jenkins/test.sh'
            }
        }
        stage('Build') {
            steps {
                sh 'docker-compose build --parallel'
                sh 'docker login -u $(username) -p $(password)'
            }
        }
        stage('Push') {
            steps {
                sh 'docker-compose push'
            }
        }
        stage('Run') {
            steps {
                sh 'bash Jenkins/deploy.sh'
            }
        }
    }
    post {
        always {
            junit '**/*.xml'
            cobertura coberturaReportFile: 'coverage.xml', failNoReports: false
        }
    }
}