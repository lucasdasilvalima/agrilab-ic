# syntax=docker/dockerfile:1
FROM ubuntu
RUN apt update && apt install python3 python3-pip -y
WORKDIR /app
COPY . ..
RUN pip install -r requeriments.txt
EXPOSE 5000
CMD ["python3", "main.py"]