FROM python:3.7.3

WORKDIR /usr/src/trails-flask

COPY ./ ./
RUN pip install -r requirements.txt

RUN adduser -D myuser
USER myuser

CMD ["/bin/bash"]
