FROM alpine
RUN apk update
RUN apk upgrade
RUN apk add libffi-dev gcc git python3-dev libjpeg-turbo-dev zlib-dev postgresql-dev libwebp-dev musl-dev libxml2-dev libxslt-dev
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools wheel
COPY . /opt/miss_evie
WORKDIR /opt/miss_evie
RUN pip3 install -r requirements.txt
CMD [ "python3", "-m", "miss_evie" ]
