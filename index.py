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
    global index1
    global index2
    global index3
    global index4

    at = airtable.Airtable('appGBN0dHYTIp1VQW', 'keyccjDgGUMhj9hid')
    df = pandas.json_normalize(at.get('Clues')['records'])
    df = df[['fields.Value', 'fields.Hint']]
    df = df.rename(columns={"fields.Value": "value", "fields.Hint": "clue"})
    
    index1 = random.randint(0, (len(df.index) - 1))
    index2 = random.randint(0, (len(df.index) - 1))
    while index2 == index1:
        index2 = random.randint(0, (len(df.index) - 1))

    index3 = random.randint(0, (len(df.index) - 1))
    while index3 == index1 or index3 == index2:
        index3 = random.randint(0, (len(df.index) - 1))

    index4 = random.randint(0, (len(df.index) - 1))
    while index4 == index1 or index4 == index2 or index4 == index3:
        index4 = random.randint(0, (len(df.index) - 1))

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
    return render_template('game_page.html', hint1=df["clue"][index1], hint2=df["clue"][index2], hint3=df["clue"][index3], hint4=df["clue"][index4], answer1=df["value"][index1], answer2=df["value"][index2], answer3=df["value"][index3], answer4=df["value"][index4])

    if __name__ == '__main__':
        app.run()