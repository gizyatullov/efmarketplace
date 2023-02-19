FROM python:3.9.6-slim-buster
RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip

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
COPY . /app/src/
RUN poetry install

CMD ["/usr/local/bin/python", "-m", "efmarketplace"]
