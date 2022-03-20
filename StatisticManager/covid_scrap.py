import requests
import sqlite3
import csv
import time
from datetime import datetime
from bs4 import BeautifulSoup

headers = {
    'accept': '*/*',
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/98.0.4758.102 Safari/537.36"
}


class DataBase:
    def __init__(self, filepath):
        self.db = sqlite3.connect(filepath, check_same_thread=False)

    def create_table(self):
        cursor = self.db.cursor()
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS world (
                time TEXT,
                total_cases BIGINT,
                new_cases TEXT,
                total_deaths BIGINT,
                new_deaths TEXT,
                total_recovered BIGINT,
                new_recovered TEXT,
                active_cases BIGINT,
                serious_cases BIGINT,
                cases_per_1m BIGINT,
                deaths_per_1m BIGINT,
                UNIQUE(total_cases)
            )""")
            self.db.commit()
        except Exception as e:
            print("Error creating the table:", e)

    def write(self):
        cursor = self.db.cursor()
        try:
            with open("resources/data.csv", 'r') as file:
                world_row = [e for e in csv.reader(file)][1]
            now = datetime.now()
            data = world_row[2:12]
            data.insert(0, now.strftime('%Y-%m-%d %H:%M:%S'))
            cursor.execute(f"INSERT OR IGNORE INTO world VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
            self.db.commit()
        except Exception as e:
            print("Error copying data from csv:", e)

    def get_data(self):
        cursor = self.db.cursor()
        data = []
        for time, t_cases in cursor.execute("SELECT time, total_cases FROM world"):
            data.append((time, t_cases))

        return data


def parse(url):
    page = requests.get(url, headers=headers)

    with open("resources/index.html", 'w', encoding="utf-8") as file:
        file.write(page.text)


def write_to_csv():
    with open("resources/index.html") as file:
        src = file.read()

    #  header
    soup = BeautifulSoup(src, "lxml")
    raws = soup.find(id="main_table_countries_today").find_all("tr")
    head_raw = [e for e in raws[0] if e != "\n"]

    with open("resources/data.csv", "w", encoding="UTF-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([e.text for e in head_raw[:15]])

    #  global section
    world_section = soup.find(id="main_table_countries_today").find_all(class_="total_row_world")
    world_row = [e for e in world_section[-1] if e != "\n"]

    with open("resources/data.csv", "a", encoding="UTF-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([e.text for e in world_row[:15]])

    #  main table data
    data = []
    table = soup.find('table', id="main_table_countries_today")
    tbody = table.find('tbody')

    rows = tbody.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [e.text.strip() for e in cols]
        data.append([e for e in cols])

    with open("resources/data.csv", "a", encoding="UTF-8", newline='') as file:
        writer = csv.writer(file)
        for row in data[8:]:
            writer.writerow(row[:15])


def main():
    db = DataBase("resources/covid_world.db")
    while True:
        parse('https://www.worldometers.info/coronavirus/')
        write_to_csv()
        db.create_table()
        db.write()
        time.sleep(600)


if __name__ == '__main__':
    main()
