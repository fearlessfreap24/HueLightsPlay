FROM python:3.10.7-alpine3.16

WORKDIR /usr/huelightsapp/

COPY . .

RUN mkdir -p /mnt/jj \
&& pip install -r requirements.txt

CMD ["python", "./helloworld.py"]