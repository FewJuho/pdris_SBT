pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'web-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DB_HOST = 'localhost'
        DB_NAME = 'test_db'
        DB_USER = 'test_user'
        DB_PASSWORD = 'test_password'
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
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                dir('web') {
                    sh '''
                        python -m pytest \
                            --cov=app \
                            --cov-report=xml \
                            --alluredir=allure-results
                    '''
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
                    
                    publishCoverage(
                        adapters: [coberturaAdapter('web/coverage.xml')],
                        sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
                    )
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                        sonar-scanner \
                        -Dsonar.projectKey=web-app \
                        -Dsonar.sources=web \
                        -Dsonar.python.coverage.reportPaths=web/coverage.xml \
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
