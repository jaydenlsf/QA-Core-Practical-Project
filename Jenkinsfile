pipeline {
    agent any
    environment {
        DATABASE_URI = credentials("DATABASE_URI_COVID")
        username = credentials("USERNAME")
        password = credentials("PASSWORD")
        DOCKER_LOGIN = credentials('DOCKER_LOGIN')
    }
    stages {
        stage('Test') {
            steps {
                sh 'bash Jenkins/test.sh'
            }
        }
        stage('Setup Docker') {
            steps {
                sh 'bash Jenkins/setup-docker.sh'
            }
        }
        stage('Build') {
            steps {
                sh 'docker-compose build --parallel'
            }
        }
        stage('Push') {
            steps {
                sh 'docker login -u $(username) -p $(password)'
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