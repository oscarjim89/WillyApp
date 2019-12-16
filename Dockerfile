FROM arm32v7/alpine

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

RUN git clone git@github.com:oscarjim89/willyApp.git
#WORKDIR /opt/WillyApp

COPY . /opt/WillyApp

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /content
EXPOSE 80
CMD [ "python3", "/opt/WillyApp/app.py" ]
ggggg