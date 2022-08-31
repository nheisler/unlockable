from flask import Flask, render_template
import pandas
import random

df = pandas.read_csv('clues.csv')
index1 = random.randint(0, len(df.index))
index2 = random.randint(0, len(df.index))
index3 = random.randint(0, len(df.index))
index4 = random.randint(0, len(df.index))

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template('start.html')

@app.route("/first")
def first_page():
    return render_template('first_value.html', hint=df["clue"][index1])

@app.route("/second")
def second_page():
    return render_template('second_value.html', hint=df["clue"][index2])

@app.route("/third")
def third_page():
    return render_template('third_value.html', hint=df["clue"][index3])

@app.route("/fourth")
def fourth_page():
    return render_template('fourth_value.html', hint=df["clue"][index4])

@app.route("/solution")
def solution_page():
    return render_template('solution.html', v1=1, v2=2, v3=3, v4=4)