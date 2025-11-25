# app/Dockerfile

FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

RUN mkdir -p /backup

ENV BACKUP_DIR=/backup

WORKDIR /code/app

EXPOSE 80

CMD ["streamlit", "run", "survey.py", "--server.address=0.0.0.0", "--server.port=80"]