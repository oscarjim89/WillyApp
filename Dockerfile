FROM arm32v7/alpine

RUN apk add --no-cache python3-dev \
    && apk add --no-cache py3-pip \
    && pip install --upgrade pip
WORKDIR /opt/WillyApp

COPY . /opt/WillyApp

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /content
EXPOSE 80
CMD [ "python3", "/opt/WillyApp/rest2mongo.py" ]
