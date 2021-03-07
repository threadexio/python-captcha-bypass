FROM alpine

ENV DISPLAY :99

RUN apk update
RUN apk add xvfb firefox ffmpeg python3 py3-pip flac

COPY . /mnt/

RUN pip install -r /mnt/requirements.txt

COPY entry.sh /entry.sh

WORKDIR /mnt/src

CMD [ "sh", "/entry.sh" ]