FROM python:3.9.6-slim-buster

RUN pip install poetry
# Configuring poetry
RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /usr/src/app/
COPY pyproject.toml /usr/src/app/

WORKDIR /usr/src/app/

# Installing requirements
RUN poetry install

# Removing gcc
RUN apt-get purge -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Copying actuall application
COPY . /usr/src/app/
RUN poetry install

CMD ["/usr/local/bin/python", "-m", "efmarketplace"]
