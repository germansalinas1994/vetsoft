pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')  // Credenciales de Docker Hub
        SMTP_CREDENTIALS = credentials('jenkins-ci-cd')  // Este es el ID en Jenkins para las credenciales de Gmail

    }
    stages {


        //  verifico que se tenga instalado docker en el sistema
        stage('Verify Docker Access') {
            steps {
                sh 'docker --version'
            }
        }

        stage('Set up Python Virtual Environment') {
            steps {
                // Crear un entorno virtual en el directorio .venv
                sh 'python3 -m venv .venv'
                // Activar el entorno virtual e instalar las dependencias
                sh '. .venv/bin/activate && pip install -r requirements-dev.txt'
            }
        }
        stage('Build and Check') {
            steps {
                // Verificar si la aplicación Django tiene errores usando el comando check
                sh '. .venv/bin/activate && python manage.py check'
            }
        }
        stage('Run Static Test') {
            steps {
                // Ejecutar el análisis estático de código usando el entorno virtual
                sh '. .venv/bin/activate && ruff check'
            }
        }
        stage('Run Unit and Integration Tests') {
            steps {
                // Ejecutar las pruebas unitarias y de integración con cobertura
                sh '. .venv/bin/activate && coverage run --source="./app" --omit="./app/migrations/**" manage.py test app'
            }
        }
        stage('Check Coverage') {
            steps {
                // Verificar que el nivel de cobertura no sea menor al 90%
                sh '. .venv/bin/activate && coverage report --fail-under=90'
            }
        }

        stage('Build Docker Image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    // Realizar el login en Docker Hub y construir la imagen
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_TOKEN')]) {
                        // Construye la imagen Docker
                        sh 'docker build -t ${DOCKERHUB_USERNAME}/vetsoft:latest .'

                        // Inicia sesión en Docker Hub
                        sh 'echo ${DOCKERHUB_TOKEN} | docker login -u ${DOCKERHUB_USERNAME} --password-stdin'

                        // Subir la imagen a Docker Hub
                        sh 'docker push ${DOCKERHUB_USERNAME}/vetsoft:latest'
                    }
                }
            }
        }

         // Etapa de despliegue en VM
        stage('Deploy to Azure VM') {
             when {
                branch 'main'
            }
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
                echo 'La imagen Docker se construyó y subió correctamente a Docker Hub.'
                echo 'Se realizó el deploy a producción.'
                // Enviar correo solo si es deploy a producción
                mail to: 'germansalinas.fce@gmail.com, valendiaz01@yahoo.com, fedebravo2016@gmail.com',
                    subject: "Deploy exitoso en producción",
                    body: "El deploy a producción de la rama ${env.BRANCH_NAME} fue exitoso.",
                    from: 'germansalinas.fce@gmail.com',
                    smtpHost: 'smtp.gmail.com',
                    smtpPort: '465',
                    username: "${SMTP_CREDENTIALS_USR}",  // Usuario de las credenciales
                    password: "${SMTP_CREDENTIALS_PSW}",  // Contraseña de las credenciales
                    useSsl: true
            }
        }
    }
    failure {
        echo 'Uno o más pasos fallaron. Deteniendo el pipeline.'
    }
}

}
