# NAGP_KUBERNETES_DEMO

This repo is having NAGP Assignment of Kubernetes where I have created flask application which is using MySQL database for read and write operation and Kubernetes YAML files.

# Table of Contents
* [Repository Link](#repository-link)
* [DockerHub Link](#docker-hub-link)
* [Service API URL](#service-api-url)
* [Recording Link](#recording-link)
* [Deployment Steps](#deployment-steps)


## Repository Link
[GitHub Link](https://github.com/ketansomani47/NAGP_KUBERNETES_DEMO)

## DockerHub Link
[DockerHub Link](https://hub.docker.com/repository/docker/ketansomani/nagp_flask/general)

## Service API URL
This section is containing the details about the flask application endpoints:

* GET Endpoint for Server Check
    
    `http://<loadbalancer_external_ip>:80/`


* GET Endpoint for User List
    
    `http://<loadbalancer_external_ip>:80/get_user`


* POST Endpoint for Adding User
    
    `http://<loadbalancer_external_ip>:80/add_user`

    Input Payload:
    
    `{
    "first_name": "ketan",
    "last_name": "somani",
    "email": "ketansomani@gmail.com",
    "age": 29
}`


## Recording Link
[Recording-Link]()


## Deployment Steps

* Create Standard Kubernetes Cluster with min 2 nodes and for each node min 4vCPU and 32GB Memory.
* Once cluster created successfully, open the cloud shell and run the below command:

    `gcloud container clusters get-credentials <cluster_name> --zone <cluster_zone> --project <project_id>`

* Upload all the YAML files present in kubernetes folder of repository to Cloud Shell.
* MySQL Database Server Deployment:
  1. Run command `kubectl apply -f mysql-storageclass.yaml` to create storage class.
  2. Run command `kubectl apply -f mysql-secrets.yaml` to create secrets.
  3. Run command `kubectl apply -f mysql-pvc.yaml` to create Persistent Volume Claim.
  4. Run command `kubectl apply -f mysql-statefulset.yaml` to create pods of mysql server using StatefulSets.
  5. Run command `kubectl apply -f mysql-service.yaml` to create Headless Cluster IP Service.
  6. When mysql pods are up and running we need to login into pod using command `kubectl exec --stdin --tty <mysql_podname> -- /bin/bash`
  7. Once login into bash script we will run command `mysql -p` to login into mysql server by passing password which is available in file `./kubernetes/mysql-secrets.yaml` file.
  8. Run command `create database <db_name>` to create database in server and db_name is available in `./kubernetes/configmap.yaml` file.
  9. Run command `exit` to come outside mysql and run command `exit` to come outside bash script.
* Flask Application Deployment:
  1. Run command `kubectl apply -f configmap.yaml` to create Config Map.
  2. Run command `kubectl apply -f flask-deployment.yaml` to create flask application pods.
  3. Run command `kubectl apply -f flask-service.yaml` to create Load Balancer Service.
* Horizontal Pod AutoScaling:
  1. Run command `kubectl apply -f flask-autoscaling.yaml` to create HPA on flask deployment.

