from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)


def loadData(t):
    myconn = mysql.connector.connect(host="82.180.142.51",
                                     database="u978805288_land",
                                     user="u978805288_root",
                                     password="ACSL@b123")

    sql_select_query = "SELECT sensor_id, value FROM data_log, info_time WHERE data_log.info_id = info_time.info_id AND data_log.triplet_id = %s ORDER BY data_log.info_id DESC LIMIT 60"
    date_select_query = "SELECT Date_Time FROM info_time WHERE triplet_id = %s ORDER BY info_id DESC LIMIT 1"

    cursor = myconn.cursor()
    cursor.execute(sql_select_query, (t,))
    data = cursor.fetchall()

    cursor.execute(date_select_query, (t,))
    date = cursor.fetchall()

    myconn.close()
    return data, date[0][0]


@app.route('/')
def index():
    triplet_id = "t51"
    data, date_value = loadData(triplet_id)
    return render_template('index.html', data=data, date=date_value)


if __name__ == '__main__':
    app.run(debug=True)
