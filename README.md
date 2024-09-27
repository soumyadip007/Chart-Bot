# AI-Powered Helm Chart Generator

## Overview
This project provides a Flask-based API for generating Helm charts for Kubernetes applications using advanced AI models. By leveraging GPT-Neo for intelligent text generation and FAISS for efficient similarity search, this solution automates the creation of comprehensive and accurate Helm charts based on user-provided parameters.

## Features
- **Automated Helm Chart Generation**: Generate complete Helm charts including `Chart.yaml`, `values.yaml`, `deployment.yaml`, and `service.yaml` files.
- **AI-Powered Text Generation**: Utilize GPT-Neo for generating Helm chart configurations based on provided prompts.
- **Efficient Similarity Search**: Use FAISS to find and utilize similar YAML configurations to improve accuracy and relevance.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup
1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/helm-chart-generator.git
    cd helm-chart-generator
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Flask application:**
    ```bash
    python app.py
    ```

## Usage

### API Endpoint
- **Endpoint:** `/generate`
- **Method:** `POST`
- **Payload:**
    ```json
    {
        "name": "my-app",
        "repository": "my-registry/my-app",
        "port": "8080",
        "version": "1.0.0",
        "description": "A Helm chart for deploying my-app on Kubernetes",
        "maintainers": [
            {
                "name": "John Doe",
                "email": "john.doe@example.com"
            }
        ],
        "appVersion": "2.1.0",
        "service": {
            "type": "ClusterIP",
            "ports": [
                {
                    "port": 8080,
                    "targetPort": 8080
                }
            ]
        },
        "resources": {
            "requests": {
                "cpu": "100m",
                "memory": "128Mi"
            },
            "limits": {
                "cpu": "200m",
                "memory": "256Mi"
            }
        },
        "environment": {
            "NODE_ENV": "production",
            "API_KEY": "your-api-key"
        },
        "replicaCount": 3,
        "ingress": {
            "enabled": true,
            "annotations": {
                "kubernetes.io/ingress.class": "nginx",
                "nginx.ingress.kubernetes.io/rewrite-target": "/"
            },
            "hosts": [
                {
                    "host": "my-app.example.com",
                    "paths": ["/"]
                }
            ],
            "tls": [
                {
                    "secretName": "my-app-tls",
                    "hosts": ["my-app.example.com"]
                }
            ]
        }
    }
    ```

### Sample Request
```bash
curl -X POST http://localhost:5000/generate \
-H "Content-Type: application/json" \
-d '{
    "name": "my-app",
    "repository": "my-registry/my-app",
    "port": "8080",
    "version": "1.0.0",
    "description": "A Helm chart for deploying my-app on Kubernetes",
    "maintainers": [
        {
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
    ],
    "appVersion": "2.1.0",
    "service": {
        "type": "ClusterIP",
        "ports": [
            {
                "port": 8080,
                "targetPort": 8080
            }
        ]
    },
    "resources": {
        "requests": {
            "cpu": "100m",
            "memory": "128Mi"
        },
        "limits": {
            "cpu": "200m",
            "memory": "256Mi"
        }
    },
    "environment": {
        "NODE_ENV": "production",
        "API_KEY": "your-api-key"
    },
    "replicaCount": 3,
    "ingress": {
        "enabled": true,
        "annotations": {
            "kubernetes.io/ingress.class": "nginx",
            "nginx.ingress.kubernetes.io/rewrite-target": "/"
        },
        "hosts": [
            {
                "host": "my-app.example.com",
                "paths": ["/"]
            }
        ],
        "tls": [
            {
                "secretName": "my-app-tls",
                "hosts": ["my-app.example.com"]
            }
        ]
    }
}'
```

### Response

```bash
{
    "helm_chart": "Generated Helm chart YAML content here..."
}
```

**Chart.yaml**
```bash
apiVersion: v2
name: application
description: Helm chart for a generic application
type: application
version: 1.0.0
appVersion: "1.0.0"
```


**Values.yaml**
```bash
replicaCount: 1
image:
  repository: registry.example.com/application
  pullPolicy: Always
  tag: "latest"
service:
  type: ClusterIP
  port: 8080
```

**Service.yaml**
```bash
apiVersion: v1
kind: Service
metadata:
  name: application-service
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8080
  selector:
    app: application
```


**Deployment.yaml**
```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: application-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: application
  template:
    metadata:
      labels:
        app: application
    spec:
      containers:
      - name: application
        image: registry.example.com/application:latest
        ports:
        - containerPort: 8080
```
### Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
