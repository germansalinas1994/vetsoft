pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        SMTP_CREDENTIALS = credentials('jenkins-ci-cd')
    }
    stages {
        stage('Verify Docker Access') {
            steps {
                sh 'docker --version'
            }
        }

        stage('Set up Python Virtual Environment') {
            steps {
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install -r requirements-dev.txt'
            }
        }

        stage('Build and Check') {
            steps {
                sh '. .venv/bin/activate && python manage.py check'
            }
        }

        stage('Run Static Test') {
            steps {
                sh '. .venv/bin/activate && ruff check'
            }
        }

        stage('Run Unit and Integration Tests') {
            steps {
                sh '. .venv/bin/activate && coverage run --source="./app" --omit="./app/migrations/**" manage.py test app'
            }
        }

        stage('Check Coverage') {
            steps {
                sh '. .venv/bin/activate && coverage report --fail-under=90'
            }
        }

        stage('Build Docker Image for dev') {
            when {
                branch 'dev'
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_TOKEN')]) {
                        // Construye la imagen Docker para el ambiente desa
                        sh 'docker build -t ${DOCKERHUB_USERNAME}/vetsoft:desa .'
                        // Inicia sesión en Docker Hub
                        sh 'echo ${DOCKERHUB_TOKEN} | docker login -u ${DOCKERHUB_USERNAME} --password-stdin'
                        // Subir la imagen a Docker Hub
                        sh 'docker push ${DOCKERHUB_USERNAME}/vetsoft:desa'
                    }
                }
            }
        }

        stage('Build Docker Image for main') {
            when {
                branch 'main'
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_TOKEN')]) {
                        // Construye la imagen Docker para producción
                        sh 'docker build -t ${DOCKERHUB_USERNAME}/vetsoft:latest .'
                        // Inicia sesión en Docker Hub
                        sh 'echo ${DOCKERHUB_TOKEN} | docker login -u ${DOCKERHUB_USERNAME} --password-stdin'
                        // Subir la imagen a Docker Hub
                        sh 'docker push ${DOCKERHUB_USERNAME}/vetsoft:latest'
                    }
                }
            }
        }

        stage('Deploy to Azure VM (desa)') {
            when {
                branch 'dev'
            }
            // 8001:8000: Esto significa que el puerto 8001 en el host se mapea al puerto 8000 dentro del contenedor.
            steps {
                script {
                    sh """
                    docker stop vetsoft-container-desa || true
                    docker rm vetsoft-container-desa || true
                    docker run -d -p 8001:8000 --name vetsoft-container-desa --restart unless-stopped germansalinas1994/vetsoft:desa
                    """
                }
            }
        }

        stage('Deploy to Azure VM (main)') {
            when {
                branch 'main'
            }
            // 8000:8000: Esto significa que el puerto 8001 en el host se mapea al puerto 8000 dentro del contenedor.
            //El contenedor sigue usando el puerto 8000 para la aplicación.
            //La máquina host usa 8000 para producción y 8001 para desa, mapeando ambos al puerto 8000 dentro del contenedor.
            steps {
                script {
                    sh """
                    docker stop vetsoft-container || true
                    docker rm vetsoft-container || true
                    docker run -d -p 8000:8000 --name vetsoft-container --restart unless-stopped germansalinas1994/vetsoft:latest
                    """
                }
            }
        }
    }

    post {
        success {
            script {
                echo 'Todos los tests corrieron exitosamente.'
                if (env.BRANCH_NAME == 'main') {
                    echo 'Se realizó el deploy a producción.'
                    mail to: 'germansalinas.fce@gmail.com, fedebravo2016@gmail.com',
                        subject: "Deploy exitoso en producción",
                        body: "El deploy a producción de la rama ${env.BRANCH_NAME} fue exitoso.",
                        from: 'germansalinas.fce@gmail.com',
                        smtpHost: 'smtp.gmail.com',
                        smtpPort: '465',
                        username: "${SMTP_CREDENTIALS_USR}",
                        password: "${SMTP_CREDENTIALS_PSW}",
                        useSsl: true
                } else if (env.BRANCH_NAME == 'dev') {
                    echo 'Se realizó el deploy al ambiente desa.'
                    mail to: 'germansalinas.fce@gmail.com, fedebravo2016@gmail.com',
                        subject: "Deploy exitoso en desa",
                        body: "El deploy al ambiente desa de la rama ${env.BRANCH_NAME} fue exitoso.",
                        from: 'germansalinas.fce@gmail.com',
                        smtpHost: 'smtp.gmail.com',
                        smtpPort: '465',
                        username: "${SMTP_CREDENTIALS_USR}",
                        password: "${SMTP_CREDENTIALS_PSW}",
                        useSsl: true
                }
            }
        }

        failure {
            script {
                echo 'Uno o más pasos fallaron. Deteniendo el pipeline.'
                if (env.BRANCH_NAME == 'main') {
                    mail to: 'germansalinas.fce@gmail.com, fedebravo2016@gmail.com',
                        subject: "Error en el deploy a producción",
                        body: "El deploy a producción ha fallado.",
                        from: 'germansalinas.fce@gmail.com',
                        smtpHost: 'smtp.gmail.com',
                        smtpPort: '465',
                        username: "${SMTP_CREDENTIALS_USR}",
                        password: "${SMTP_CREDENTIALS_PSW}",
                        useSsl: true
                } else if (env.BRANCH_NAME == 'dev') {
                    mail to: 'germansalinas.fce@gmail.com, fedebravo2016@gmail.com',
                        subject: "Error en el deploy a desa",
                        body: "El deploy al ambiente desa ha fallado.",
                        from: 'germansalinas.fce@gmail.com',
                        smtpHost: 'smtp.gmail.com',
                        smtpPort: '465',
                        username: "${SMTP_CREDENTIALS_USR}",
                        password: "${SMTP_CREDENTIALS_PSW}",
                        useSsl: true
                }
            }
        }
    }
}
