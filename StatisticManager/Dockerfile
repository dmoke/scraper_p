FROM python:3.9.1

RUN mkdir -p /usr/src/app/StatisticManager
WORKDIR /usr/src/app/StatisticManager

COPY . /usr/src/app/StatisticManager
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "covid_scrap.py"]