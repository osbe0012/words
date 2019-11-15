from flask import Flask, request, Response, render_template, jsonify, url_for
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Regexp
import re
import ast
import json

class WordForm(FlaskForm):
  avail_letters = StringField("Letters:", validators= [
    Regexp(r'^[a-z]+$', message="Must contain letters only")])
  wordLengthDropDownMenu = SelectField("Specific Word Length:", choices=[
    ('0','All'), ('3','3'), ('4','4'), ('5','5'), ('6','6'), ('7','7'), ('8','8'),
    ('9','9'), ('10','10')])
  patternTextBox = StringField("Pattern to Match:", validators=[
  Regexp(r'^$|^[a-z\.]+$', message="Must contain letters and/or '.' only")])
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
  # If errors, load index.html
  form = WordForm()
  if form.validate_on_submit():
    letters = form.avail_letters.data
  else:
    # Add enforcement requirements here
    return render_template("index.html", form=form)
  
  # Otherwise load wordlist.html
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
  resultJSON = result.json()
  reworkedList = ast.literal_eval(wordList)
  return render_template('wordlist.html',
    wordlist=reworkedList,
    resultJSON=resultJSON,
    match=word)