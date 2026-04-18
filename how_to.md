# Postgres:
## 1. step
oc new-app postgresql:15-el9 \
    --name=postgresql \
    -e POSTGRESQL_USER=<USER> \
    -e POSTGRESQL_PASSWORD=<PASSWORD> \
    -e POSTGRESQL_DATABASE=<DB_NAME>

## 2. step
oc delete pvc postgresql-pvc
oc set volume deployment/postgresql --add \
    --name=postgresql-data \
    -t pvc \
    --claim-name=postgresql-pvc \
    --claim-size=1Gi \
    --mount-path=/var/lib/pgsql/data

oc set volume deployment/postgresql --remove --name=postgresql-data
oc delete pvc postgresql-pvc

# Backend
## 4. step
oc create secret generic github-secret --from-literal=username=mattSysNote --from-literal=password=<PASSWORD> --type=kubernetes.io/basic-auth
## 5. step
oc secrets link builder github-secret
## 6. step
oc new-app "python~https://github.com/mattSysNote/felho.git" --name=django-backend --source-secret=github-secret -e DB_HOST=postgresql -e DB_PORT=5432 -e DB_NAME=<DB_NAME> -e DB_USER=<USER> -e DB_PASSWORD=<PASSWORD> -e SECRET_KEY=<SECRET_KEY> -e DEBUG=False

## 7. step - deprecated pvc -> blob postgres
oc set volume deployment/django-backend --add --name=media-storage --type=persistentVolumeClaim --claim-name=media-pvc --mount-path=/opt/app-root/src/media --overwrite

### delete command:
oc set volume deployment/django-backend --remove --name=media-storage
oc delete pvc media-pvc

## 8. step
oc start-build django-backend
## 9. step
oc expose service django-backend --port=8080
oc scale deployment django-backend --replicas=1
oc get route django-backend

oc delete route django-backend
oc create route edge --service=django-backend --port=8080
oc start-build django-backend --follow

## 10. step
          command:
            - /bin/bash
            - '-c'
            - 'python manage.py migrate && gunicorn --bind 0.0.0.0:8080 photoupload.wsgi'
# delete and util commands:
oc delete all -l app=django-backend
oc delete svc django-backend
oc delete deployment django-backend
oc delete svc postgresql
oc delete deployment postgresql
oc rsh <pod>
python manage.py migrate gallery zero
oc describe bc/django-backend


# env variables:
oc set env deployment/django-backend SECRET_KEY=<SECRET_KEY> DEBUG=False
oc set env deployment/django-backend DEBUG-

# Stop services
oc scale deployment/locust-tester --replicas=0
oc scale deployment/django-backend --replicas=0
oc scale deployment/postgresql --replicas=0

oc scale deployment/postgresql --replicas=1
oc scale deployment/django-backend --replicas=1
oc scale deployment/locust-tester --replicas=1

# HPA:
resources:
    limits:
        cpu: 500m
        memory: 512Mi
    requests:
        cpu: 200m
        memory: 256Mi


oc autoscale deployment/django-backend --min=1 --max=5 --cpu-percent=50
oc delete hpa django-backend
oc get hpa

oc run load-generator --image=busybox --restart=Never -- /bin/sh -c "while true; do wget -q -O- <myservice> > /dev/null; done"

oc delete pod load-generator


# Stress test
oc new-app "python~https://github.com/mattSysNote/felho.git" --name=locust-tester --source-secret=github-secret
oc create route edge --service=locust-tester --port=8089
oc expose service locust-tester --port=8089
oc delete route locust-tester

deployment:
port: 8089

oc start-build locust-tester

plus config:
          command: ["locust"]
          args: 
            - "-f"
            - "locustfile.py"
            - "--host=<BACKEND_URL>"


IaC
oc whoami -t


oc delete all -l app=django-backend
oc delete all -l app=postgresql
oc delete pvc postgresql-pvc