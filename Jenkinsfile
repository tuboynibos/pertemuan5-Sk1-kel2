pipeline {
  agent any

  environment {
    IMAGE_REPO = "tuboy/demo-app"     // ganti dengan repo kamu
    IMAGE_TAG  = "latest"
    CHART_PATH = "helm/demo-app"
    KUBE_NAMESPACE = "demo"
  }

  options {
    skipDefaultCheckout(false)
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Image') {
      steps {
        bat '''
          docker build -t %IMAGE_REPO%:%IMAGE_TAG% .
        '''
      }
    }

    stage('Unit Test (smoke)') {
      steps {
        bat '''
          for /f "tokens=*" %%i in ('docker run -d -p 5000:5000 %IMAGE_REPO%:%IMAGE_TAG%') do set CID=%%i
          timeout /t 5 >nul
          curl http://localhost:5000/ | find "Hello, World!"
          docker rm -f %CID%
        '''
      }
    }

    stage('Push to DockerHub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                         usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          bat '''
            echo %DH_PASS% | docker login -u %DH_USER% --password-stdin
            docker push %IMAGE_REPO%:%IMAGE_TAG%
            docker logout
          '''
        }
      }
    }

    stage('Deploy with Helm') {
      steps {
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
          bat '''
            kubectl create namespace %KUBE_NAMESPACE% --dry-run=client -o yaml | kubectl apply -f -
            helm upgrade --install demo %CHART_PATH% ^
              --namespace %KUBE_NAMESPACE% ^
              --set image.repository=%IMAGE_REPO% ^
              --set image.tag=%IMAGE_TAG%
          '''
        }
      }
    }

    stage('Verify Deployment') {
      steps {
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
          bat '''
            kubectl -n %KUBE_NAMESPACE% get pods
            kubectl -n %KUBE_NAMESPACE% get svc
          '''
        }
      }
    }
  }

  post {
    always {
      echo "Pipeline finished."
    }
  }
}
