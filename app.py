from flask import Flask, render_template
import pandas
import random
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

def setData():
    global df
    global index1
    global index2
    global index3
    global index4

    df = pandas.read_csv('clues.csv')
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
    return render_template('start.html')

@app.route("/play")
def game_page():
    return render_template('game_page.html', hint1=df["clue"][index1], hint2=df["clue"][index2], hint3=df["clue"][index3], hint4=df["clue"][index4])

@app.route("/solution")
def solution_page():
    finalMessage = "Your solution was correct! The lock has been opened"
    
    if True:
        finalMessage = "Your solution was incorrect! The correct combination is "
        finalMessage += str(df["value"][index1])
        finalMessage += str(df["value"][index2])
        finalMessage += str(df["value"][index3])
        finalMessage += str(df["value"][index4])
        finalMessage += " -- Try again tomorrow"

    return render_template('solution.html', d1=1, d2=2, d3=3, d4=4, message=finalMessage)