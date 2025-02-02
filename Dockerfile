RUN apk add --no-cache gcc musl-dev mariadb-dev curl

RUN mkdir /app
WORKDIR /app

ENV POETRY_HOME=/usr/local/poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=$POETRY_HOME/bin:$PATH

COPY pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry lock
RUN poetry install
