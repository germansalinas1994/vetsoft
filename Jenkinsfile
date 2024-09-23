pipeline {
    agent any
    options {
        // Detener la ejecución si un paso falla
        skipStagesAfterUnstable()
    }

    stages {
        stage('Set up Python Virtual Environment') {
            steps {
                // Crear un entorno virtual en el directorio .venv
                sh 'python3 -m venv .venv'
                // Activar el entorno virtual e instalar las dependencias
                sh '. .venv/bin/activate && pip install -r requirements.txt'
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

        // stage('Set up Python Virtual Environment') {
        //     steps {
        //         // Crear un entorno virtual en el directorio .venv
        //         sh 'python3 -m venv .venv'
        //         // Activar el entorno virtual e instalar las dependencias
        //         sh '. .venv/bin/activate && pip install -r requirements.txt'
        //     }
        // }

        // stage('Install dependencies') {
        //     steps {
        //         // Instalar dependencias dentro del entorno virtual
        //         sh './venv/bin/pip install -r requirements-dev.txt'
        //     }
        // }

        // stage('Check') {
        //     steps {
        //         // Verificar si la aplicación Django tiene errores usando el comando check
        //         sh './venv/bin/python manage.py check'
        //     }
        // }

        // stage('Build') {
        //     steps {
        //         // Recoger y compilar archivos estáticos de Django
        //         sh './venv/bin/python manage.py collectstatic --noinput'
        //     }
        // }

        // stage('Run Static Test') {
        //     steps {
        //         // Ejecutar análisis estático de código usando ruff en el entorno virtual
        //         sh './venv/bin/ruff check'
        //     }
        // }

        // stage('Run Unit Tests') {
        //     steps {
        //         // Ejecuta las pruebas unitarias
        //         sh './venv/bin/python -m coverage run --source="./app" --omit="./app/migrations/**" manage.py test app'
        //     }
        //     post {
        //         always {
        //             // Publicar el reporte de cobertura de las pruebas
        //             sh './venv/bin/coverage report'
        //             junit 'test-reports/*.xml'
        //         }
        //     }
        // }

        // stage('Check coverage') {
        //     steps {
        //         // Verificar que la cobertura sea al menos del 90%
        //         sh './venv/bin/coverage report --fail-under=90'
        //     }
        // }
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
