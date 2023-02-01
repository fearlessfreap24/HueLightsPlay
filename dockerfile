FROM python:3.10.7-alpine3.16

WORKDIR /usr/huelightsapp/

COPY . .

RUN mkdir -p /mnt/jj \
&& pip install -r requirements.txt

# flask
# CMD ["python", "./helloworld.py"]

# WSGI
# CMD [ "python", "wsgi.py" ]

# gunicorn - add CMD to k8s yaml
CMD [ "gunicorn", "--bind", "0.0.0.0:5001", "wsgi:app" ]

