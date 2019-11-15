from flask import Flask, request, Response, render_template, jsonify, url_for
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Regexp
import re
import ast

class WordForm(FlaskForm):
  avail_letters = StringField("Letters", validators= [
      Regexp(r'^[a-z]+$', message="must contain letters only")
  ])
  submit = SubmitField("Go")


csrf = CSRFProtect()
app = Flask(__name__)
app.config["SECRET_KEY"] = "row the boat"
csrf.init_app(app)

@app.route('/')
def index():
  form = WordForm()
  return render_template("index.html", form=form)


@app.route('/words', methods=['POST','GET'])
def letters_2_words():
  form = WordForm()
  if form.validate_on_submit():
    letters = form.avail_letters.data
  else:
    return render_template("index.html", form=form)

  with open('sowpods.txt') as f:
    good_words = set(x.strip().lower() for x in f.readlines())

  word_set = set()
  for l in range(3,len(letters)+1):
    for word in itertools.permutations(letters,l):
      w = "".join(word)
      if w in good_words:
        word_set.add(w)

  return render_template('wordlist.html',
    wordlist=sorted(word_set, key=len))


@app.route('/proxy/<wordList>/<word>')
def proxy(wordList, word):
  mwKey = 'f9863492-b5fd-44b1-8a55-d80a273e1b54'
  print(f'Requesting: https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={mwKey}')
  result = requests.get(f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={mwKey}')
  print("Result: " + str(result))
  resultJSON = result.json()
  print("Result JSON shortdef: " + str(resultJSON[0]['shortdef']))
  reworkedList = ast.literal_eval(wordList)
  print("Reworded List: " + str(reworkedList))
  return render_template('wordList.html',
  wordlist=reworkedList,
  resultJSON=resultJSON,
  match=word)