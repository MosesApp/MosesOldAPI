FROM python:3.4

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
		gcc \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

#The will be linked from the host machine.
#Makes it easier to debug changes.
VOLUME /usr/src/app

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
