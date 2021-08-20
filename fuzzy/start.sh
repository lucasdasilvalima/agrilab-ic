#!/bin/bash

docker build -t flasgger .
docker run -it --rm -p 5000:5000 --name flasgger flasgger
