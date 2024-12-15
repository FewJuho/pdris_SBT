pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'web-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
        PYTHONPATH = "${WORKSPACE}/web"
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
                        python -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        pip install pytest pytest-allure-adaptor pytest-cov flake8
                    '''
                }
            }
        }
        
        stage('Code Quality') {
            steps {
                dir('web') {
                    sh '''
                        . venv/bin/activate
                        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                dir('web') {
                    sh '''
                        . venv/bin/activate
                        pytest --alluredir=allure-results --cov=. --cov-report=xml
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
                }
            }
        }
        
        stage('SonarQube Analysis') {
            environment {
                SONAR_SCANNER_OPTS = "-Xmx512m"
            }
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                        sonar-scanner \
                        -Dsonar.projectKey=web-app \
                        -Dsonar.sources=web \
                        -Dsonar.python.coverage.reportPaths=web/coverage.xml \
                        -Dsonar.host.url=${SONAR_HOST_URL} \
                        -Dsonar.login=${SONAR_AUTH_TOKEN} \
                        -Dsonar.python.version=3.9
                    """
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                dir('web') {
                    script {
                        try {
                            sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                            sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                        } catch (Exception e) {
                            currentBuild.result = 'FAILURE'
                            error("Docker build failed: ${e.message}")
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            sh '''
                if [ -d "web/venv" ]; then
                    rm -rf web/venv
                fi
            '''
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
