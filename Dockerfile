FROM python:3
COPY . /reco
WORKDIR  /reco
RUN pip install -r requirements.txt
EXPOSE 8000
# CMD gunicorn --workers=4 --bind 0.0.0.0:&PORT manage:manage
CMD gunicorn recoama.wsgi:application