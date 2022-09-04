from flask import Flask, render_template, request
import pandas
import random
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pandas.io.json import json_normalize
from airtable import airtable

def setData():
    global df
    at = airtable.Airtable('appGBN0dHYTIp1VQW', 'keyccjDgGUMhj9hid')
    df = pandas.json_normalize(at.get('DailyAnswers')['records'])
    df = df[['fields.Value', 'fields.Hint']]
    df = df.rename(columns={"fields.Value": "value", "fields.Hint": "clue"})

app = Flask(__name__)

@app.before_first_request
def before_first_request():
    print("setup scheduler")
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(
            year="*", month="*", day="*", hour="1", minute="0", second="5"
        )
    scheduler.add_job(func=setData, trigger=trigger)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    setData()

@app.route("/")
def main_page():
    return render_template('index.html')

@app.route("/play", methods = ['GET','POST'])
def game_page():
    return render_template('game_page.html', hint1=df["clue"][0], hint2=df["clue"][1], hint3=df["clue"][2], hint4=df["clue"][3], answer1=df["value"][0], answer2=df["value"][1], answer3=df["value"][2], answer4=df["value"][3])

if __name__ == '__main__':
    app.run()