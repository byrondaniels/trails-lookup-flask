FROM python:3.7.3

WORKDIR /usr/src/trails-flask

COPY ./ ./
RUN pip install pipenv
RUN pipenv install


CMD ["/bin/bash"]