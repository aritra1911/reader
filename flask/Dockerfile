FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade uWSGI>=2.0.19.1

COPY . .

CMD [ "uwsgi", "app.ini" ]
