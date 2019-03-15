FROM tp33/django
RUN pip install --upgrade pip && pip install \
    "django-pipeline==1.6.14 " \
    "requests==2.21.0" \
    "psycopg2==2.7.7" \
    "beautifulsoup4==4.7.1"
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt-get install -y --no-install-recommends \
        postgresql \
        postgresql-contrib \
        nodejs
RUN npm install -g sass
RUN npm install -g yuglify
RUN npm install bootstrap