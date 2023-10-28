
import os
import subprocess

# Define the directory where the files will be saved and deployed from
DIRECTORY = "/home/user/Desktop/ROBOT_JOB"

def run_command(command):
    """Execute a system command and return its output."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if error:
        print(f"Error: {error.decode('utf-8')}")
    return output.decode('utf-8')

def write_file(filename, content):
    """Helper function to write content to a file in DIRECTORY."""
    with open(os.path.join(DIRECTORY, filename), "w") as f:
        f.write(content)

# Create a Dockerfile for the Python Flask app
write_file("Dockerfile", """FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
""")

# Write the Python Flask app code which connects to a MySQL database
write_file("app.py", """from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    connection = mysql.connector.connect(user='root', password='yourpassword',
                              host='mysql-service',
                              database='testdb')
    cursor = connection.cursor()
    cursor.execute('SELECT message FROM testtable')
    row = cursor.fetchone()
    return jsonify(message=row[0])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
""")

# Specify Python packages required for the Flask app
write_file("requirements.txt", """Flask==2.0.1
mysql-connector-python==8.0.26
""")

# Create Kubernetes configuration for deploying MySQL
write_file("mysql-deployment.yaml", """
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
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
spec:
  selector:
    matchLabels:
      app: mysql
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - image: mysql:5.7
        name: mysql
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "yourpassword"
        - name: MYSQL_DATABASE
          value: "testdb"
        ports:
        - containerPort: 3306
          name: mysql
""")

# Create Kubernetes configuration for deploying the Flask app
write_file("app-deployment.yaml", """
apiVersion: v1
kind: Service
metadata:
  name: flaskapp-service
spec:
  selector:
    app: flaskapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flaskapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flaskapp
  template:
    metadata:
      labels:
        app: flaskapp
    spec:
      containers:
      - image: myflaskapp:latest
        name: flaskapp
        ports:
        - containerPort: 5000
          name: flask-app
""")

# Change to the defined directory
os.chdir(DIRECTORY)

# Build the Docker image using the Dockerfile
print("Building Docker Image...")
docker_build_command = "docker build -t myflaskapp ."
output = run_command(docker_build_command)
print(output)

# Use Kubernetes to deploy the MySQL configuration
print("Deploying MySQL on Kubernetes...")
mysql_deploy_command = "kubectl apply -f mysql-deployment.yaml"
output = run_command(mysql_deploy_command)
print(output)

# Use Kubernetes to deploy the Flask app configuration
print("Deploying Flask App on Kubernetes...")
app_deploy_command = "kubectl apply -f app-deployment.yaml"
output = run_command(app_deploy_command)
print(output)

print("Deployment complete!")

