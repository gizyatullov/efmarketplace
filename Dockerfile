FROM python:3.9.6-slim-buster

RUN pip install poetry==1.3.2
# Configuring poetry
RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /usr/src/app/

WORKDIR /usr/src/app/

# Installing requirements
RUN poetry install --only main --no-interaction --no-ansi

# Copying actually application
COPY . /usr/src/app/

CMD ["/usr/local/bin/python", "-m", "efmarketplace"]
