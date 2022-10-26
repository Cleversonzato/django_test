FROM python:3.10

ADD . /django_test
COPY requirements.txt /
RUN pip install -r requirements.txt
WORKDIR /django_test/django_test
EXPOSE 8000

CMD ["gunicorn", "django_test.wsgi"]