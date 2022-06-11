FROM ubuntu:20.04
LABEL description = "Tarea 2.1"
RUN apt update
RUN apt upgrade -y

RUN apt-get install -y python3
RUN apt-get install -y sqlite3
RUN apt install -y python3-pip



RUN pip3 install uvicorn==0.17.6
RUN pip3 install fastapi==0.78.0
RUN pip3 install pytest==7.1.1

RUN pip3 install web.py==0.62

RUN pip3 install black==22.3.0
RUN pip3 install flake8==4.0.1
RUN pip3 install isort==5.10.1
RUN pip3 install mypy==0.961


ENV requirements /home/requirements.txt
COPY requirements.txt ${requirements}
WORKDIR /home/