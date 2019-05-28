FROM python:3.7.3

WORKDIR /usr/src/trails-flask

COPY ./ ./
RUN pip install -r requirements.txt

CMD ["python3", "app.py"]
