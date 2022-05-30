from MyVocabulary import languages
from wtforms import Form,StringField,TextAreaField,PasswordField,SelectField,validators

class RegisterForm(Form):
    username = StringField("",validators=[validators.Length(min = 5, max = 30)])
    name = StringField("",validators=[validators.Length(min = 4, max = 25)])
    motherLanguage = SelectField("",choices=languages, default="en")
    foreignLanguage = SelectField("",choices=languages, default="es")
    email = StringField("",validators=[validators.Email(message = "Please enter a valid email address")])
    password = PasswordField("" ,validators=[
        validators.DataRequired(message = "Please enter a password"),
        validators.EqualTo(fieldname = "confirm", message="Passwords don't match")
    ])
    confirm = PasswordField("")

class LoginForm(Form):
    username = StringField("",validators=[validators.Length(min = 1, message="You must type something in!")])
    password = PasswordField("",validators=[validators.Length(min = 1, message="You must type something in!")])

class WordsFormGoogle(Form):
    word = StringField("",validators=[validators.Length(min = 3, message="You must type something in!")])
    sentence = StringField("",)
    sourceLanguage = SelectField("",choices=languages,default=None)
    targetLanguage = SelectField("",choices=languages,default=None)

class WordsFormManuel(Form):
    word = StringField("",validators=[validators.Length(min = 1, message="You must type something in!")])
    wordTranslate = StringField("",validators=[validators.Length(min = 2, message="You must type something in!")])
    sentence = StringField("",)
    sentenceTranslate = StringField("",)
    sourceLanguage = SelectField("",choices=languages,default=None)
    targetLanguage = SelectField("",choices=languages,default=None)