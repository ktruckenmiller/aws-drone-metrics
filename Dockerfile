FROM python:alpine
WORKDIR /app
COPY src/requirements.pip requirements.pip

RUN pip install -r requirements.pip
RUN pip install pytest pytest-cov
