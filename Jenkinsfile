pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')  // Credenciales de Docker Hub
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
                    docker run -d -p 8000:8000 --name vetsoft-container germansalinas1994/vetsoft:latest
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
                echo 'La aplicación fue desplegada en la VM de Azure.'
            }
        }
    }
    failure {
        echo 'Uno o más pasos fallaron. Deteniendo el pipeline.'
    }
}

}
