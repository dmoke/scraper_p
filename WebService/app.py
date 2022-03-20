from flask import Flask, render_template
from StatisticManager.covid_scrap import DataBase

app = Flask(__name__)


@app.route('/')
def cases_plot():
    db = DataBase("../StatisticManager/resources/covid_world.db")
    data = db.get_data()
    labels = [e[0] for e in data]
    values = [e[1].replace(',', '') for e in data]
    return render_template("plot.html", labels=labels, values=values)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
