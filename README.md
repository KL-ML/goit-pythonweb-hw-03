# goit-pythonweb-hw-03

### Create docker image

```
docker build -t hw3 .
```

### start docker container

```
docker run -p 3000:3000 -v ./storage:/app/storage --name hw3 hw3
```
