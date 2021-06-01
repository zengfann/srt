FROM python:3.9

WORKDIR /code

COPY requirements/prod.txt requirements.txt

RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt \
    -f https://download.pytorch.org/whl/torch_stable.html

COPY app app
COPY ml ml

RUN mkdir /data

VOLUME [ "/data" ]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:app"]
