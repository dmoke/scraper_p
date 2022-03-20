FROM python:3.9.1

RUN mkdir -p /usr/src/app/WebService
WORKDIR /usr/src/app/WebService

COPY . /usr/src/app/WebService
RUN pip install --no-cache-dir -r requirements.txt
ENV TZ Europe/Moscow

EXPOSE 5000

CMD ["python", "app.py"]