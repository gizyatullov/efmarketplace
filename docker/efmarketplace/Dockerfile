FROM python:3.9.6-slim-buster

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip install --upgrade pip

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["/usr/local/bin/python", "-m", "efmarketplace"]
