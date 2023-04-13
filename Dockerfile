FROM python:3
COPY . /reco
WORKDIR  /reco
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --workers=4 --bind 0.0.0.0:&PORT manage:manage