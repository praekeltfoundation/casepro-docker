FROM praekeltfoundation/django-bootstrap:py3.6-stretch

RUN apt-get-install.sh curl && curl -sL https://deb.nodesource.com/setup_12.x | bash && \
    apt-get install nodejs -y && apt-get remove curl -y

ARG CASEPRO_VERSION
RUN echo "Downloading Casepro from https://github.com/rapidpro/casepro/archive/${CASEPRO_VERSION}.tar.gz"
RUN apt-get update
RUN apt-get-install.sh wget
RUN wget -O casepro.tar.gz "https://github.com/rapidpro/casepro/archive/${CASEPRO_VERSION}.tar.gz"
RUN tar -xf casepro.tar.gz --strip-components=1
RUN rm casepro.tar.gz
RUN apt-get remove wget -y
RUN apt-get-install.sh build-essential

COPY nginx.conf /etc/nginx/conf.d/django.conf
RUN nginx; service nginx reload

COPY setup.py ./setup.py
COPY settings.py casepro/settings.py

RUN pip install --upgrade pip && pip install --upgrade poetry

RUN poetry install --no-dev
RUN poetry add django-environ

RUN npm install -g less coffeescript

ENV PROJECT_ROOT /casepro/
ENV DJANGO_SETTINGS_MODULE "casepro.settings"
RUN poetry run python ./manage.py collectstatic --noinput

RUN poetry run python ./manage.py compress

# RUN django-admin collectstatic --noinput && \  
    # USE_DEFAULT_CACHE=True django-admin compress

CMD ["casepro.wsgi:application", "--timeout", "1800"]
