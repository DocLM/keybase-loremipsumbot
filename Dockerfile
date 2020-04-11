ARG PYTHON_VERSION=3-slim
FROM python:${PYTHON_VERSION} as python-base
ENV PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  VENV_PATH=/opt/venv
ENV PATH="$VENV_PATH/bin:$PATH"
RUN apt-get update \
  && apt-get install --no-install-recommends -y curl \
  && rm -rf /var/lib/apt/lists/*

FROM python-base as builder
ENV POETRY_PATH=/opt/poetry
ENV PATH="$POETRY_PATH/bin:$PATH"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python \
  && mv /root/.poetry $POETRY_PATH \
  && python -m venv $VENV_PATH \
  && poetry config virtualenvs.create false \
  && rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev --no-interaction --no-ansi -vvv

FROM python-base as runtime
RUN apt-get update \
  && curl --remote-name https://prerelease.keybase.io/keybase_amd64.deb \
  && apt install --no-install-recommends -y ./keybase_amd64.deb \
  && rm -rf ./keybase_amd64.deb \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m keybase \
  && mkdir /var/log/keybase \
  && chown keybase:keybase /var/log/keybase

COPY --from=builder $VENV_PATH $VENV_PATH
COPY ./keybase_loremipsumbot /loremipsumbot

USER keybase
ENV \
  KEYBASE_USERNAME="" \
  KEYBASE_PAPERKEY="" \
  KEYBASE_USERNAME_FILE="" \
  KEYBASE_PAPERKEY_FILE=""  

COPY ./entrypoint /usr/bin/entrypoint
ENTRYPOINT [ "entrypoint" ]
CMD [ "python", "-m", "loremipsumbot"]
