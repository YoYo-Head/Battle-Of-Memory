FROM python:3.14

WORKDIR /app

COPY . /app



RUN pip install -r requirements.txt

CMD [ "python", "ssh-server.py" ]

EXPOSE 2222