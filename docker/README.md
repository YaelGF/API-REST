# Config Ubuntu 20.04 and Python with FastAPI

## 1. Dockefile 
```
FROM ubuntu:20.04
LABEL description = "Tarea 2.1"
RUN apt update
RUN apt upgrade -y

RUN apt-get install -y python3
RUN apt-get install -y sqlite3
RUN apt install -y python3-pip

ENV requirements /home/requirements.txt
COPY requirements.txt ${requirements}

RUN pip3 install uvicorn==0.17.6
RUN pip3 install fastapi==0.78.0
RUN pip3 install pytest==7.1.1

RUN pip3 install web.py==0.62

RUN pip3 install black==22.3.0
RUN pip3 install flake8==4.0.1
RUN pip3 install isort==5.10.1
RUN pip3 install mypy==0.961

WORKDIR /home/
```

## 2. Build Docker image
```
docker build -t fastapi:v1 .
```

## 3. Create docker container
nota:regresar a la carpeta principal
```
cd ..
```

```
docker run -it -v $(pwd)/code:/PaginaFastAPI --net host --name fastapy -h python fast:0.1
```

## 4. Run Web Page

```
$ cd PaginaFastAPI
$ uvicorn main:app --reload
```



ENV requirements /home/requirements.txt
COPY requirements.txt ${requirements}
WORKDIR /home/