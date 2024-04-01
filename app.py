# from flask import Flask, render_template
# import mysql.connector

# app = Flask(__name__)


# def loadData(t):
#     myconn = mysql.connector.connect(host="82.180.142.51",
#                                      database="u978805288_land",
#                                      user="u978805288_root",
#                                      password="ACSL@b123")

#     sql_select_query = "SELECT sensor_id, value FROM data_log, info_time WHERE data_log.info_id = info_time.info_id AND data_log.triplet_id = %s ORDER BY data_log.info_id DESC LIMIT 60"
#     date_select_query = "SELECT Date_Time FROM info_time WHERE triplet_id = %s ORDER BY info_id DESC LIMIT 1"

#     cursor = myconn.cursor()
#     cursor.execute(sql_select_query, (t,))
#     data = cursor.fetchall()

#     cursor.execute(date_select_query, (t,))
#     date = cursor.fetchall()

#     myconn.close()
#     return data, date[0][0]


# @app.route('/')
# def index():
#     triplet_id = "t51"
#     data, date_value = loadData(triplet_id)
#     return render_template('index.html', data=data, date=date_value)


# if __name__ == '__main__':
#     app.run(debug=True)

import tensorflow as tf
import threading
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
from tensorflow.keras.models import load_model
from multiprocessing import cpu_count
from warnings import catch_warnings
from warnings import filterwarnings
from pandas import read_csv
import matplotlib.pyplot as plt
from pandas import DataFrame
import time
# from datetime import datetime
import datetime
import itertools
import mysql.connector
from mysql.connector import connection
from mysql.connector import errorcode
from statistics import mean

from flask import Flask, render_template
from datetime import datetime, timedelta
import mysql.connector

app = Flask(__name__)

# Function to load data from MySQL database


def loadData(triplet_id):
    myconn = mysql.connector.connect(host="82.180.142.51",
                                     database="u978805288_land",
                                     user="u978805288_root",
                                     password="ACSL@b123")
    sql_select_query = "select sensor_id, value from data_log, info_time where data_log.info_id = info_time.info_id AND data_log.triplet_id = '" + \
        triplet_id+"' ORDER BY data_log.info_id desc limit 60"
    date_select_query = "select Date_Time from info_time where triplet_id='" + \
        triplet_id+"' order by info_id desc limit 1"

    cursor = myconn.cursor()
    cursor.execute(sql_select_query)
    data = cursor.fetchall()

    cursor.execute(date_select_query)
    date = cursor.fetchall()

    myconn.close()
    return data, date[0][0]


# Function to preprocess data
# triplet_id = "t41"
# data, date_value = loadData(triplet_id)


def dataPreprocess(data):
    result = []
    data.reverse()

    combined_data = []
    for i in range(0, len(data), 7):
        row = data[i:i+7]
        sensor_data = []

        for s, d in row:
            sid = s
            if sid == 's6':
                continue
            elif sid == 's5':
                x = d.split(',')[:6]
                for j in x:
                    sensor_data.append(float(j))
                x = d.split(',')[-1]
                sensor_data.append(float(x))
            elif sid.startswith('s'):
                x = d.split(',')[:]
                for j in x:
                    sensor_data.append(float(j))

        combined_data.extend(sensor_data)

    data = np.array(combined_data)
    return combined_data


# preprocessed_data = dataPreprocess(data)
# split_rows = [preprocessed_data[i:i+13]
#               for i in range(0, len(preprocessed_data), 13)]

# Function to run model
STOREDIR = ('finalmodel')
model1 = tf.saved_model.load(STOREDIR)
predict_fn = model1.signatures["serving_default"]
# Load the second model
STOR = "/content/drive/MyDrive/Count_data-LMS/urni dhank/"
model2 = tf.keras.models.load_model('website1.h5')


def runModel(data_tensor):
    previous = 1
    try:
        # Run the prediction on the first model
        pred = predict_fn(data_tensor)
        pred = np.argmax(pred)
        pred = np.round(pred).astype(int)

        # Run the prediction on the second model
        dt = data_tensor[:, :, 0:5]
        pred1 = model2.predict(dt)

        combined_list = []
        combined_list.extend([round(x, 2) for x in pred1.tolist()[0]])
        combined_list.append(pred)

        return (combined_list)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

# Function to insert data into database


def insertDatabase(prediction, triplet_id):
    connection = mysql.connector.connect(host="82.180.142.51",
                                         database="u978805288_land",
                                         user="u978805288_root",
                                         password="ACSL@b123")
    try:
        current_time = datetime.now()
        val = "(NULL,'" + triplet_id + "'," + str(prediction[0]) + "," + str(prediction[1]) + "," + str(prediction[2]) + "," + str(
            prediction[3]) + "," + str(prediction[4]) + "," + str(prediction[5]) + ",'" + str(current_time) + "','no')"
        add_prediction = "INSERT INTO Prediction_Real_Data  VALUES "+val
        cursor = connection.cursor()
        cursor.execute(add_prediction)
        connection.commit()
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into prediction table {}".format(error))

    finally:
        if connection.is_connected():
            connection.close()


# THIS ONE
def continuousLoop():
    try:
        with app.app_context():
            # Define your station IDs here
            triplet_ids = ['t62']
            
            # triplet_ids = ['t38', 't36', 't37', 't40','t70','t71','t74','t75','t76','t77','t83','t82',
            #               't83','t63','t64','t66','t68','t41', 't50', 't51']
            
            # dictionary to store prediction history for each triplet ID
            all_prediction_history = {}
            for triplet_id in triplet_ids:
                prediction_history = []
                data, date = loadData(triplet_id)
                if data:
                    date = date + timedelta(minutes=10)
                    # data = dataPreprocess(data)
                    preprocessed_data = dataPreprocess(data)
                    data_list = []
                    count = 0
                    for i in range(10):
                        d = preprocessed_data[count:count+13]
                        data_list.append(d)
                        count += 13

                    data_array = np.array(data_list)
                    data_array = data_array.reshape((-1, 10, 13))
                    data_tensor = tf.convert_to_tensor(
                        data_array, dtype=tf.float32)
                    prediction = runModel(data_tensor)
                    insertDatabase(prediction, triplet_id)
                    prediction_history.append(prediction)
                    print(prediction_history)
                    print("Inserted for: ", triplet_id)
                    # time.sleep(10)
                else:
                    print("No data found for triplet ID:", triplet_id)
                # Store prediction history for the current triplet ID
                all_prediction_history[triplet_id] = prediction_history
                print(all_prediction_history)
            # Sleep 10 seconds before running again
            time.sleep(10)
    except Exception as e:
        print(f"Error occurred in continuous loop: {str(e)}")
    return all_prediction_history  


# Start the background thread
thread = threading.Thread(target=continuousLoop)
thread.daemon = True
thread.start()
# END


# Main route
# @app.route('/')
# def index():
#     return render_template('index2.html')

@app.route('/')
def index():
    all_prediction_history = continuousLoop()
    return render_template('index2.html', all_prediction_history=all_prediction_history)


if __name__ == '__main__':
    app.run(debug=True)
