FROM praekeltfoundation/django-bootstrap:py3.6-stretch

EXPOSE 6379

RUN apt-get-install.sh curl && curl -sL https://deb.nodesource.com/setup_12.x | bash && \
    apt-get install nodejs -y && apt-get remove curl -y

ARG CASEPRO_VERSION
RUN echo "Downloading Casepro from https://github.com/rapidpro/casepro/archive/${CASEPRO_VERSION}.tar.gz" && \
    apt-get-install.sh wget && \
    wget -O casepro.tar.gz "https://github.com/rapidpro/casepro/archive/${CASEPRO_VERSION}.tar.gz" && \
    tar -xf casepro.tar.gz --strip-components=1 && \
    rm casepro.tar.gz && \
    apt-get remove wget -y && \
    apt-get-install.sh build-essential 

COPY nginx.conf /etc/nginx/conf.d/django.conf
RUN nginx; service nginx reload

COPY setup.py ./setup.py
COPY settings.py casepro/settings.py

RUN pip install --upgrade pip && pip install --upgrade poetry

# Poetry creates a virtual environment, this tells it not to, as it is in a docker container
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    poetry add django-environ && \
    npm install -g less coffeescript

ENV PROJECT_ROOT /casepro/
ENV DJANGO_SETTINGS_MODULE "casepro.settings"
RUN poetry run python ./manage.py collectstatic --noinput
ENV USE_DEFAULT_CACHE=True
RUN poetry run python ./manage.py compress

CMD ["casepro.wsgi:application", "--timeout", "1800"]
