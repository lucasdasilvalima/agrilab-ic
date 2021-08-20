# syntax=docker/dockerfile:1
FROM ubuntu
RUN apt update && apt install python3 python3-pip -y
WORKDIR /app
COPY . .
RUN pip install -r requeriments.txt
CMD ["python3", "main.py"]