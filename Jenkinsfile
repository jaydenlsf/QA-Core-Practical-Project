pipeline {
    agent any
    environment {
        DATABASE_URI = credentials("DATABASE_URI_COVID")
        DOCKER_LOGIN = credentials('DOCKER_LOGIN')
        install_docker = 'false'
    }
    stages {
        stage('Test') {
            steps {
                sh 'bash Jenkins/test.sh'
            }
        }
        stage('Setup Docker') {
            steps {
                script {
                    if (env.install_docker == 'true') {
                        sh 'bash Jenkins/setup-docker.sh'
                    }
                }
            }
        }
        stage('Build') {
            steps {
                sh 'docker-compose build --parallel'
            }
        }
        stage('Push') {
            steps {
                sh 'docker login -u $DOCKER_LOGIN_USR -p $DOCKER_LOGIN_PSW'
                sh 'docker-compose push'
            }
        }
        stage('Run') {
            steps {
                sh 'docker-compose up -d'
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