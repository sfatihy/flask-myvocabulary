from flask import Flask, session, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from googletrans import Translator
import random
from functools import wraps

app = Flask(__name__)

app.secret_key = "hello"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myVocabulary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

languages = [
    ('af','Afrikaans'),
    ('sq', 'Albanian'),
    ('am', 'Amharic'),
    ('ar', 'Arabic'),
    ('hy', 'Armenian'),
    ('az', 'Azerbaijani'),
    ('eu', 'Basque'),
    ('be', 'Belarusian'),
    ('bn', 'Bengali'),
    ('bs', 'Bosnian'),
    ('bg', 'Bulgarian'),
    ('ca', 'Catalan'),
    ('ceb', 'Cebuano'),
    ('ny', 'Chichewa'),
    ('zh-cn', 'Chinese (simplified)'),
    ('zh-tw', 'Chinese (traditional)'),
    ('co', 'Corsican'),
    ('hr', 'Croatian'),
    ('cs', 'Czech'),
    ('da', 'Danish'),
    ('nl', 'Dutch'),
    ('en', 'English'),
    ('eo', 'Esperanto'),
    ('et', 'Estonian'),
    ('tl', 'Filipino'),
    ('fi', 'Finnish'),
    ('fr', 'French'),
    ('fy', 'Frisian'),
    ('gl', 'Galician'),
    ('ka', 'Georgian'),
    ('de', 'German'),
    ('el', 'Greek'),
    ('gu', 'Gujarati'),
    ('ht', 'Haitian creole'),
    ('ha', 'Hausa'),
    ('haw', 'Hawaiian'),
    ('iw', 'Hebrew'),
    ('he', 'Hebrew'),
    ('hi', 'Hindi'),
    ('hmn', 'Hmong'),
    ('hu', 'Hungarian'),
    ('is', 'Icelandic'),
    ('ig', 'Igbo'),
    ('id', 'Indonesian'),
    ('ga', 'Irish'),
    ('it', 'Italian'),
    ('ja', 'Japanese'),
    ('jw', 'Javanese'),
    ('kn', 'Kannada'),
    ('kk', 'Kazakh'),
    ('km', 'Khmer'),
    ('ko', 'Korean'),
    ('ku', 'Kurdish (kurmanji)'),
    ('ky', 'Kyrgyz'),
    ('lo', 'Lao'),
    ('la', 'Latin'),
    ('lv', 'Latvian'),
    ('lt', 'Lithuanian'),
    ('lb', 'Luxembourgish'),
    ('mk', 'Macedonian'),
    ('mg', 'Malagasy'),
    ('ms', 'Malay'),
    ('ml', 'Malayalam'),
    ('mt', 'Maltese'),
    ('mi', 'Maori'),
    ('mr', 'Marathi'),
    ('mn', 'Mongolian'),
    ('my', 'Myanmar (burmese)'),
    ('ne', 'Nepali'),
    ('no', 'Norwegian'),
    ('or', 'Odia'),
    ('ps', 'Pashto'),
    ('fa', 'Persian'),
    ('pl', 'Polish'),
    ('pt', 'Portuguese'),
    ('pa', 'Punjabi'),
    ('ro', 'Romanian'),
    ('ru', 'Russian'),
    ('sm', 'Samoan'),
    ('gd', 'Scots Gaelic'),
    ('sr', 'Serbian'),
    ('st', 'Sesotho'),
    ('sn', 'Shona'),
    ('sd', 'Sindhi'),
    ('si', 'Sinhala'),
    ('sk', 'Slovak'),
    ('sl', 'Slovenian'),
    ('so', 'Somali'),
    ('es', 'Spanish'),
    ('su', 'Sundanese'),
    ('sw', 'Swahili'),
    ('sv', 'Swedish'),
    ('tg', 'Tajik'),
    ('ta', 'Tamil'),
    ('te', 'Telugu'),
    ('th', 'Thai'),
    ('tr', 'Turkish'),
    ('uk', 'Ukrainian'),
    ('ur', 'Urdu'),
    ('ug', 'Uyghur'),
    ('uz', 'Uzbek'),
    ('vi', 'Vietnamese'),
    ('cy', 'Welsh'),
    ('xh', 'Xhosa'),
    ('yi', 'Yiddish'),
    ('yo', 'Yoruba'),
    ('zu', 'Zulu') ]

#User Login Decorator
def login_required(f):
   @wraps(f)
   def decorated_function(*args, **kwargs):
      if "logged_in" in session:
         return f(*args, **kwargs)
      else:
         flash("Please login if you want to continue")
         return redirect(url_for("login"))
   return decorated_function

#Return letter code into language
def shortToLong(shortLanguage):

   for x in languages:
      if x[0] == shortLanguage:
         result = x[1]

   #print(shortLanguage + " --> " + result)

   return result

#Return language into letter code
def longToShort(longLanguage):

   for x in languages:
      if x[1] == longLanguage:
         result = x[0]

   #print(longLanguage + " --> " + result)

   return result

#Translate
def translate(data,source,target):

   translator = Translator()

   translation = translator.translate(data , src=source, dest=target)

   #print(translation.origin, ' -> ', translation.text)

   return translation.text

#Random words for navbar
def navbarwords():
   n = random.randint(1,5)

   navbarword = Word.query.filter_by(wordId = n).first()

   return navbarword


from MyVocabulary.models import Word
from MyVocabulary import routes

