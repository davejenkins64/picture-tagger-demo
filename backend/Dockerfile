FROM ubuntu:latest
LABEL com.demo.picture_tagger_server=0.0.1
RUN apt-get update && apt-get install -y python3 python3-pip
COPY requirements.txt /usr/src/api/
RUN pip3 install --no-cache-dir -r /usr/src/api/requirements.txt
COPY api.py PictureDB.py /usr/src/api/
RUN mkdir /usr/src/api/data
EXPOSE 5000
WORKDIR /usr/src/api
CMD [ "python3", "/usr/src/api/api.py" ]
