# Rooms management and message dissemination.

## Internet Based Systems Architecture (ASInt) course project.

### Deploy instructions
Follow [Running Django in the App Engine Flexible Environment]

### Deploy information
Project name: ist-roomsmanagement

Project ID: ist-roomsmanagement

Project number: 968854237878

DB Instance ID: ist-roomsmanagement-db

Default user: postgres

Default password: postgres 

Instance connection name: ist-roomsmanagement:europe-west2:ist-roomsmanagement-db

Initialize Cloud SQL instance (Proxy)
```shell
./cloud_sql_proxy -instances="ist-roomsmanagement:europe-west2:ist-roomsmanagement-db"=tcp:5432
```

DB name: roomsmanagement

DB user name: roomsmanagement

DB password: roomsmanagement

GCS Bucket: ist-roomsmanagement


### Details
Fall Semester of 2017/2018.

Development using [Django].

Deployment using [Google Cloud Platform] services.

### Authors
José Coelho

Xavier Reis


   [Running Django in the App Engine Flexible Environment]: <https://cloud.google.com/python/django/flexible-environment?hl=en>
   [Django]: <https://www.djangoproject.com/>
   [Google Cloud Platform]: <https://cloud.google.com/>
