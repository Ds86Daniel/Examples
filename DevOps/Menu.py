
import os
import subprocess
import sys
from flask import Flask, jsonify, request
import mysql.connector
#http://localhost:5000/k8s-nodes

def run_command(command):
    return subprocess.getoutput(command)

def build_docker_image():
    dockerfile_content = """
FROM python:3.8-slim
WORKDIR /app
COPY . .
CMD ["python", "app.py"]
"""
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    os.system("docker build -t mypythonapp .")

def deploy_to_kubernetes():
    deployment_content = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: python-app
  template:
    metadata:
      labels:
        app: python-app
    spec:
      containers:
      - name: python-app
        image: mypythonapp:latest
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:5.7
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "password"
---
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
spec:
  selector:
    app: mysql
  ports:
  - protocol: TCP
    port: 3306
    targetPort: 3306
"""
    with open("deployment.yaml", "w") as f:
        f.write(deployment_content)
    os.system("kubectl apply -f deployment.yaml")

def monitor_k8s_resources():
    pods_status = run_command("kubectl get pods")
    print(pods_status)

def start_flask_app():
    app = Flask(__name__)

    @app.route('/search-mysql', methods=['POST'])
    def search_mysql():
        query = request.json.get('query')
        try:
            connection = mysql.connector.connect(user='root', password='password', host='mysql-service', database='testdb')
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)})
        finally:
            connection.close()

    @app.route('/k8s-nodes', methods=['GET'])
    def get_k8s_nodes():
        nodes_command = "kubectl get nodes"
        output = run_command(nodes_command)
        return jsonify({"nodes": output})

    app.run(host="0.0.0.0", port=5000)

def main():
    while True:
        print("\nDevOps Tool")
        print("1. Build Docker Image")
        print("2. Deploy to Kubernetes")
        print("3. Monitor Kubernetes Resources")
        print("4. Start Flask App")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            build_docker_image()
        elif choice == '2':
            deploy_to_kubernetes()
        elif choice == '3':
            monitor_k8s_resources()
        elif choice == '4':
            start_flask_app()
        elif choice == '5':
            sys.exit()
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
