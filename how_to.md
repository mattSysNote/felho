Postgres:
# 1. lépés
oc new-app postgresql:15-el9 \
    --name=postgresql \
    -e POSTGRESQL_USER=<USER> \
    -e POSTGRESQL_PASSWORD=<PASSWORD> \
    -e POSTGRESQL_DATABASE=<DB_NAME>

# 2. lépés
oc set volume deployment/postgresql --add \
    --name=postgresql-data \
    -t pvc \
    --claim-name=postgresql-pvc \
    --claim-size=1Gi \
    --mount-path=/var/lib/pgsql/data

# 4. lépés
oc create secret generic github-secret --from-literal=username=mattSysNote --from-literal=password=<PASSWORD> --type=kubernetes.io/basic-auth
# 5. lépés
oc secrets link builder github-secret
# 6. lépés
oc new-app "python~https://github.com/mattSysNote/felho.git" --name=django-backend --source-secret=github-secret -e DB_HOST=postgresql -e DB_PORT=5432 -e DB_NAME=<DB_NAME> -e DB_USER=<USER> -e DB_PASSWORD=<PASSWORD> -e SECRET_KEY=<SECRET_KEY> -e DEBUG=False

# 7. lépés
oc set volumes deployment/django-backend --add --name=media-storage --type=pvc --claim-name=media-pvc --claim-size=1Gi --mount-path=/app/media


oc patch deployment/django-backend  --patch '{"spec":{"template":{"spec":{"securityContext":{"fsGroup":2000}}}}}'

# 8. lépés
oc start-build django-backend
# 9. lépés
oc expose service django-backend --port=8080
oc scale deployment django-backend --replicas=1
oc get route django-backend

oc delete route django-backend
oc create route edge --service=django-backend --port=8080
oc start-build django-backend --follow



# Törlések:
oc delete all -l app=django-backend
oc delete svc django-backend
oc delete deployment django-backend
oc delete svc postgresql
oc delete deployment postgresql


# plusz env:
oc set env deployment/django-backend SECRET_KEY=<SECRET_KEY> DEBUG=False


# Stop the Django backend
oc scale deployment/django-backend --replicas=0

# Stop the Postgres database
oc scale deployment/postgresql --replicas=0