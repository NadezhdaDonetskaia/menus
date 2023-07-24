FROM python:3.10

ENV POETRY_VERSION=1.2.2


# Install poetry and application
RUN python3 -m pip install -U pip setuptools && \
    python3 -m pip install -U poetry==${POETRY_VERSION}

COPY . /srv/application/menus_ylab

WORKDIR /srv/application/menus_ylab

# Install application
RUN poetry install

ENTRYPOINT [ "/srv/application/menus_ylab/docker-entrypoint.sh" ]