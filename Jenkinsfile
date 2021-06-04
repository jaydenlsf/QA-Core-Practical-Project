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
        stage('Ansible configuration') {
            steps {
                sh 'sudo apt install ansible -y'
                sh 'bash install_ansible.sh'
                sh 'ansible-playbook -i ./ansible/inventory.yaml ./ansible/playbook.yaml'
            }
        }
        stage('Run') {
            steps {
                sh 'bash deploy.sh'
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