pipeline {
    agent any
    options {
        // Detener la ejecución si un paso falla
        skipStagesAfterUnstable()
    }

    stages {
        stage('Install dependencies') {
            steps {
                // Instala las dependencias del proyecto
                sh 'pip install -r requirements-dev.txt'
            }
        }

        stage('Check') {
            steps {
                // Verificar si la aplicación Django tiene errores usando el comando check
                sh 'python manage.py check'

            }
        }
        stage('Build') {
            steps {
                // Recoge y compila archivos estáticos de Django
                sh 'python manage.py collectstatic --noinput'
            }
        }
            stage('Run Static Test') {
            steps {
                // Ejecutar el análisis estático de código usando el entorno virtual
                sh 'ruff check'
            }
        }

        stage('Run Unit Tests') {
            steps {
                // Ejecuta las pruebas unitarias
                sh 'coverage run --source="./app" --omit="./app/migrations/**" manage.py test app'
            }
            post {
                always {
                    // Publica el reporte de cobertura de las pruebas
                    sh 'coverage report'
                    junit 'test-reports/*.xml'
                }
            }
        }

        stage('Check coverage') {
            steps {
                // Verifica que la cobertura sea al menos del 90%
                sh 'coverage report --fail-under=90'
            }
        }


    }

    post {
        success {
            // Mensaje en caso de éxito total
            echo 'All stages passed successfully. Ready to merge or deploy.'
        }
        failure {
            // Mensaje en caso de fallo en alguna etapa
            echo 'One or more stages failed. Stopping pipeline.'
            error('Pipeline failed due to failed tests.')
        }
    }
}
