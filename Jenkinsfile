pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'web-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
        PATH = "$PATH:/var/lib/jenkins/.local/bin"
        PYTHON_PATH = "/usr/bin/python3"
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
                    sh '''
                        python3 -m pip install --user --upgrade pip
                        python3 -m pip install --user -r requirements.txt
                        python3 -m pip install --user pytest allure-pytest
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                dir('web') {
                    sh 'python3 -m pytest --alluredir=allure-results'
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
        
        stage('Generate Allure Report') {
            steps {
                sh '/opt/allure/bin/allure generate web/allure-results -c -o allure-report'
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                        -Dsonar.projectKey=web-app \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=${SONAR_HOST_URL} \
                        -Dsonar.login=${SONAR_AUTH_TOKEN}
                    '''
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
