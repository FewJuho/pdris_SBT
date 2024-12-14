pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'web-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                dir('web') {
                    sh 'pip install -r requirements.txt'
                    // Установка зависимостей для тестов
                    sh 'pip install pytest pytest-allure-adaptor'
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                dir('web') {
                    sh 'pytest --alluredir=allure-results'
                }
            }
            post {
                always {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'web/allure-results']]
                    ])
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                        sonar-scanner \
                        -Dsonar.projectKey=web-app \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=${SONAR_HOST_URL} \
                        -Dsonar.login=${SONAR_AUTH_TOKEN}
                    """
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                dir('web') {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
