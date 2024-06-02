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
    
    `http://nagp.flaskapp.com:80/v1/`


* GET Endpoint for User List
    
    `http://nagp.flaskapp.com:80/v1/get_user`


* POST Endpoint for Adding User
    
    `http://nagp.flaskapp.com:80/v1/add_user`

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
  3. Run command `kubectl apply -f flask-nodeport.yaml` to create Node Port Service.
  4. Run command `gcloud compute firewall-rules create nodeport-rule --allow tcp:32000 --project <project_id>` to enable firewall for nodeport.
* Ingress Deployment:
  1. Run command `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/cloud/deploy.yaml` to create ingress-nginx controller.
  2. Run command `kubectl apply -f flask-ingress.yaml` to create ingress for flask application.
  3. Once ingress is created and running, we need to add ingress's external IP and domain `nagp.flaskapp.com` to hosts file at `/etc/hosts` location.
* Horizontal Pod AutoScaling:
  1. Run command `kubectl apply -f flask-autoscaling.yaml` to create HPA on flask deployment.

