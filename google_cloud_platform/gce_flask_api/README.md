# gce_flask_api

> A Flask-Docker project

## Run Flask

```
$ python main.py
```
Once up and running, either use curl or Postman. For Postman, create a POST
to http://0.0.0.0:5000, select body -> raw with Content-Type = application/json
and create a json file similar to:

```
{
  "data": "/9j/4AAQSkZJRgABAQAAAQABAA..."
}
```

Curl:
```
(echo -n '{"data": "'; base64 cat.jpg; echo '"}') |
curl -X POST -H "Content-Type: application/json" -d @- http://0.0.0.0:5000
```

## Run Docker and Google Deploy

```
$ docker build -t [name] .
$ docker tag [name] [HOSTNAME]/[PROJECT_ID]/[DOCKER IMAGE NAME]
$ gcloud docker -- push [HOSTNAME]/[PROJECT_ID]/[DOCKER IMAGE NAME]
```
- Hostname => us.gci.io
- Project_ID => gcloud projects list

Once on your GCE server...
```
$ curl -sSL https://get.docker.com | sh
$ gcloud docker pull [HOSTNAME]/[PROJECT_ID]/[DOCKER IMAGE NAME]
$ sudo docker run -td -p 80:80 [HOSTNAME]/[PROJECT_ID]/[DOCKER IMAGE NAME]
$ sudo docker ps #get container ID
$ sudo docker logs --follow [container_ID] 
```
