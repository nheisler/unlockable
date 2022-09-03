from flask import Flask, render_template, request
import pandas
import random
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
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

scheduler = BackgroundScheduler()
scheduler.add_job(func=setData, trigger="cron", day_of_week='mon-sun', hour=1, minute=0)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

setData()

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template('index.html')

@app.route("/play", methods = ['GET','POST'])
def game_page():
    return render_template('game_page.html', hint1=df["clue"][index1], hint2=df["clue"][index2], hint3=df["clue"][index3], hint4=df["clue"][index4])

def checkAnswer(answer1, answer2, answer3, answer4):
    if answer1 == str(df["value"][index1]) and answer2 == str(df["value"][index2]) and answer3 == str(df["value"][index3]) and answer4 == str(df["value"][index4]):
        return True
    else:
        return False

@app.route("/solution", methods=['GET', 'POST'])
def solution_page():
    if request.method == 'POST':
        answer1 = request.form.get('answer1')
        answer2 = request.form.get('answer2')
        answer3 = request.form.get('answer3')
        answer4 = request.form.get('answer4')
    finalMessage = "Your solution was correct! The lock has been opened"
    
    if not checkAnswer(answer1, answer2, answer3, answer4):
        finalMessage = "Your solution was incorrect! The correct combination is "
        finalMessage += str(df["value"][index1])
        finalMessage += str(df["value"][index2])
        finalMessage += str(df["value"][index3])
        finalMessage += str(df["value"][index4])
        finalMessage += " -- Try again tomorrow"

    return render_template('solution.html', d1=answer1, d2=answer2, d3=answer3, d4=answer4, message=finalMessage)