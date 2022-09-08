from multiprocessing.connection import wait
from flask import Flask, render_template, request
import pandas
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pandas.io.json import json_normalize
import datetime
import threading
import time

def setData():
    global df
    global idx0
    global idx1
    global idx2
    global idx3

    df = pandas.read_csv("static/clues.csv")

    idx0 = (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).days % len(df.index) * 4
    while idx0 > (len(df.index) - 1):
        idx0 = idx0 - (len(df.index) - 1)
    idx1 = idx0 + 1
    while idx1 > (len(df.index) - 1):
        idx1 = idx1 - (len(df.index) - 1)
    idx2 = idx1 + 1
    if idx2 > (len(df.index) - 1):
        idx2 = idx2 - (len(df.index) - 1)
    idx3 = idx2 + 1
    if idx3 > (len(df.index) - 1):
        idx3 = idx3 - (len(df.index) - 1)

def startupThread():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(
            year="*", month="*", day="*", hour="1", minute="0", second="5"
        )
    scheduler.add_job(func=setData, trigger=trigger)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    setData()

app = Flask(__name__)

@app.before_first_request
def before_first_request():
    global startup_thread
    startup_thread = threading.Thread(target=startupThread, name="Startup")
    startup_thread.start()

@app.route("/")
def main_page():
    return render_template('index.html')

@app.route("/play", methods = ['GET','POST'])
def game_page():
    while startup_thread.is_alive():
        time.sleep(1)
    return render_template('game_page.html', hint1=df["clue"][idx0], hint2=df["clue"][idx1], hint3=df["clue"][idx2], hint4=df["clue"][idx3], answer1=df["value"][idx0], answer2=df["value"][idx1], answer3=df["value"][idx2], answer4=df["value"][idx3])

if __name__ == '__main__':
    app.run()