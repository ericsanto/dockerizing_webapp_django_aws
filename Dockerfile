# syntax=docker/dockerfile:experimental

FROM python:3.11-alpine3.19

#SET WORK DIRECTORY
WORKDIR /app

# IMPEDE QUE O PYTHON MANDE ARQUIVOS PYCACHE
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#INSTALL DEPENDECIES
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . .

