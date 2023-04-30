FROM python:3.11.3-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Copy project
COPY . /code