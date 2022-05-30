from datetime import datetime
from MyVocabulary import db

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256),unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    point = db.Column(db.Integer, nullable=False)
    motherLanguage = db.Column(db.String(256), nullable=False)
    foreignLanguage = db.Column(db.String(256), nullable=False)
    loginDate = db.Column(db.DateTime, nullable=False , default = datetime.now)
    words = db.relationship("Word",backref="user",lazy=True)

    def __init__(self, username, name, email, password, point, motherLanguage, foreignLanguage):
        self.username         = username
        self.name             = name
        self.email            = email
        self.password         = password
        self.point            = point
        self.motherLanguage   = motherLanguage
        self.foreignLanguage  = foreignLanguage

    def __repr__(self):
        return f'User: { self.username }, { self.point }'

class Word(db.Model):
    wordId = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(256), nullable=False)
    wordTranslate = db.Column(db.String(256), nullable=False)
    sentence = db.Column(db.String(256),nullable=False)
    sentenceTranslate = db.Column(db.String(256), nullable=False)
    sourceLanguage = db.Column(db.String(4), nullable=False)
    targetLanguage = db.Column(db.String(4), nullable=False)
    isMemorized = db.Column(db.Boolean, default = False)
    wordAddedDate = db.Column(db.DateTime, nullable=False , default = datetime.now)
    wordMemorizedDate = db.Column(db.DateTime)
    userId = db.Column(db.Integer, db.ForeignKey("user.userId"),nullable=False)

    def __init__(self, word, wordTranslate, sentence, sentenceTranslate, sourceLanguage, targetLanguage, isMemorized, userId):
        self.word             = word
        self.wordTranslate    = wordTranslate
        self.sentence         = sentence
        self.sentenceTranslate= sentenceTranslate
        self.sourceLanguage   = sourceLanguage
        self.targetLanguage   = targetLanguage
        self.isMemorized      = isMemorized
        self.userId           = userId

    def __repr__(self):
        return f'User: { self.word }, { self.wordTranslate }'

class NavbarWord(db.Model):
    navbarWordId = db.Column(db.Integer, primary_key=True)
    sourceLanguage = db.Column(db.String(256), nullable=False)
    sourceLanguageWord = db.Column(db.String(256), nullable=False)
    sourceLanguageSentences = db.Column(db.String(256), nullable=False)
    targetLanguage = db.Column(db.String(256), nullable=False)
    targetLanguageWord = db.Column(db.String(256), nullable=False)
    targetLanguageSentences = db.Column(db.String(256), nullable=False)

