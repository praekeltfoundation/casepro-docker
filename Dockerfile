FROM praekeltfoundation/django-bootstrap:py3.6-stretch

RUN apt-get-install.sh curl && curl -sL https://deb.nodesource.com/setup_12.x | bash && \
    apt-get install nodejs -y && apt-get remove curl -y

ARG CASEPRO_VERSION
RUN echo "Downloading Casepro from https://github.com/rapidpro/casepro/archive/${CASEPRO_VERSION}.tar.gz" && \
    apt-get-install.sh wget  && \
    wget -O casepro.tar.gz "https://github.com/rapidpro/casepro/archive/${CASEPRO_VERSION}.tar.gz" && \
    tar -xf casepro.tar.gz --strip-components=1 && \
    rm casepro.tar.gz && \
    apt-get remove wget -y

COPY nginx.conf /etc/nginx/conf.d/django.conf
RUN nginx; service nginx reload

COPY setup.py ./setup.py
COPY settings.py casepro/settings.py

RUN apt-get-install.sh git gcc libc-dev
RUN pip install -e . && \
    pip install -r pip-requires.txt && \
    pip install -r pip-freeze.txt && \
    pip install django-environ && \
    npm install -g less coffee-script

RUN apt-get remove git gcc libc-dev -y

# to fix a broken migration in v1.1.18 
RUN sed -i 's/name/__name__/g' casepro/statistics/migrations/0015_populate_is_squashed.py

ENV PROJECT_ROOT /casepro/
ENV DJANGO_SETTINGS_MODULE "casepro.settings"
RUN django-admin collectstatic --noinput && \  
    USE_DEFAULT_CACHE=True django-admin compress

CMD ["casepro.wsgi:application", "--timeout", "1800"]
