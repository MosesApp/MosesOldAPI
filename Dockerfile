FROM python:3.4

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
		gcc \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY . /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD python manage.py migrate && \
	python manage.py runserver 0.0.0.0:8000


# A better way to do this is keeping an image on DockerHub that
# has all python dependencies installed and the /usr/src/app created.
#
# Than we'd have to call only:
# COPY . /usr/app
# CMD python manage.py migrate && \
#		python manage.py runserver 0.0.0.0:8000
