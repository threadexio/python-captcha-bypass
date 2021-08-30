FROM alpine

RUN apk update
RUN apk add chromium chromium-chromedriver ffmpeg python3 py3-pip flac

COPY . /mnt/

RUN pip install -r /mnt/requirements.txt

COPY entry.sh /entry.sh

WORKDIR /mnt/src

CMD [ "sh", "/entry.sh" ]