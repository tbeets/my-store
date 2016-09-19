FROM tbeets/python-base

MAINTAINER Todd Beets

WORKDIR /code

ADD . /code
RUN pip install -r requirements.txt

# Equiv to --workers gunicorn parameter; override as docker run --env WEB_CONCURRENCY=x
ENV WEB_CONCURRENCY=2

# In order to make the convenience -P flag work; make the same as the default CMD parameter...
EXPOSE 5000

# CMD parameters may be overriden with docker run parameters...
CMD ["--bind","0.0.0.0:5000"]

ENTRYPOINT ["gunicorn","app.main:app"]