pipeline {
  agent any

  environment {
    IMAGE_REPO = "tuboy/demo-app"     // ganti
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
        sh '''
          docker build -t ${IMAGE_REPO}:${IMAGE_TAG} .
        '''
      }
    }

    stage('Unit Test (smoke)') {
      steps {
        sh '''
          cid=$(docker run -d -p 5000:5000 ${IMAGE_REPO}:${IMAGE_TAG})
          sleep 3
          curl -sf http://localhost:5000/ | grep -q "Hello, World!"
          docker rm -f $cid
        '''
      }
    }

    stage('Push to DockerHub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                         usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh '''
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
            docker push ${IMAGE_REPO}:${IMAGE_TAG}
            docker logout
          '''
        }
      }
    }

    stage('Deploy with Helm') {
      steps {
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
          sh '''
            kubectl create namespace ${KUBE_NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
            helm upgrade --install demo ${CHART_PATH} \
              --namespace ${KUBE_NAMESPACE} \
              --set image.repository=${IMAGE_REPO} \
              --set image.tag=${IMAGE_TAG}
          '''
        }
      }
    }

    stage('Verify Deployment') {
      steps {
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
          sh '''
            kubectl -n ${KUBE_NAMESPACE} get pods
            kubectl -n ${KUBE_NAMESPACE} get svc
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
