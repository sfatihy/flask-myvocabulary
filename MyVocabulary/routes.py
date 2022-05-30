from crypt import methods
from flask import render_template, flash, redirect, url_for, request, session
from passlib.hash import sha256_crypt
from datetime import datetime
import random
from sqlalchemy import asc , desc
from MyVocabulary import app, db, languages, longToShort, shortToLong, translate, navbarwords, login_required
from MyVocabulary.forms import RegisterForm, LoginForm, WordsFormGoogle, WordsFormManuel
from MyVocabulary.models import User, Word, NavbarWord

#Register/Sign up
@app.route('/register' , methods =["GET","POST"])
def register():

    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():

        #---Getting data from register form
        username = form.username.data
        name = form.name.data
        motherLanguage = form.motherLanguage.data
        foreignLanguage = form.foreignLanguage.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        point = int(0)
        #---Getting data from register form---

        #---Check languages---
        boolmotherLanguage = False
        for x in languages:
            if x[0] == motherLanguage:
                motherLanguage = x[1]
                boolmotherLanguage = True

        if boolmotherLanguage != True:
            flash("Change your mother language!")
            return render_template("register.html" , form = form)

        boolforeignLanguage = False
        for x in languages:
            if x[0] == foreignLanguage:
                foreignLanguage = x[1]
                boolforeignLanguage = True

        if boolforeignLanguage != True:
            flash("Change your foreign language!")
            return render_template("register.html" , form = form)
        #---Check languages---

        user = User.query.filter_by(username = username).first()
        usermail = User.query.filter_by(email = email).first()

        if user:

            flash("This username is preselected, select another!")
            return render_template("register.html" , form = form)
        
        else:

            if usermail:

                flash("This email address is preselected, enter another!")
                return render_template("register.html" , form = form)

            else:

                newUser = User(username = username, name = name, email = email, password = password, motherLanguage = motherLanguage, foreignLanguage = foreignLanguage, point = point)

                db.session.add(newUser)
                db.session.commit()

                flash("You are successfully registered!")
                return redirect(url_for("login"))

    else:

        if "id" in session:
            return redirect(url_for("addbygoogle"))

        return render_template("register.html" , form = form)

#Login/Sign in
@app.route('/login' , methods =["GET","POST"])
def login():

    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():

        #---Getting data from login form---
        username = form.username.data
        passwordEntered = form.password.data
        #---Getting data from login form---

        user = User.query.filter_by(username = username).first()

        if user:

            userPassword = user.password
            point = user.point
            userId = user.userId

            if sha256_crypt.verify(passwordEntered,userPassword):

                session["logged_in"] = True
                session["username"] = username
                session["point"] = point
                session["id"] = userId

                flash("You are successfully login!")
                return redirect(url_for("addbygoogle"))

            else:

                flash("You entered wrong password!")
                return render_template("login.html" , form = form)

        else:

            flash("This user was not found!")
            return render_template("login.html" , form = form)

    else:

        if "id" in session:
            return redirect(url_for("addbygoogle"))

        return render_template("login.html" , form = form)

#Logout/Sign out
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

#Add word using google api
@app.route('/google', methods =["GET","POST"])
@login_required
def addbygoogle():

    form = WordsFormGoogle(request.form)

    #---User info from session---
    userId = session["id"]
    user = User.query.filter_by(userId = userId).first()

    point = user.point
    mother = user.motherLanguage
    foreign = user.foreignLanguage
    #---User info from session---
   
    #---Selected mother and foreign language is send to form---
    mother = longToShort(mother)
    form.targetLanguage.data = mother

    foreign = longToShort(foreign)
    form.sourceLanguage.data = foreign
    #---Selected mother and foreign language is send to form---

    if request.method == "POST" and form.validate():

        form = WordsFormGoogle(request.form)

        #---Getting data from WordsFormGoogle form---
        word = form.word.data
        sentence = form.sentence.data
        source = form.sourceLanguage.data
        target = form.targetLanguage.data
        #---Getting data from WordsFormGoogle form---

        wordTranslate = translate(str(word), source, target)

        #---Sentence control---
        if len(sentence) == 0:
            sentenceTranslate = " "
        else:
            sentenceTranslate = translate(str(sentence), source, target)
        #---Sentence control---

        source = shortToLong(source)
        target = shortToLong(target)

        isMemorized = False

        newWord = Word(word = word, wordTranslate = wordTranslate, sentence = sentence, sentenceTranslate = sentenceTranslate, sourceLanguage = source, targetLanguage = target, isMemorized = isMemorized, userId = userId)

        db.session.add(newWord)
        db.session.commit()

        user.point = int(user.point) + 10

        point = user.point

        db.session.commit()

        flash( word + " successfully added!")
        return  redirect(url_for("addbygoogle" , form = form , point = point , navbarword = navbarwords()))
    
    else:

        return  render_template("addbygoogle.html" , form = form , point = point , navbarword = navbarwords())

#Add word by user
@app.route('/byuser', methods = ["GET", "POST"])
@app.route('/', methods =["GET","POST"])
@login_required
def addbyuser():

    form = WordsFormManuel(request.form)

    #---User info from session---
    userId = session["id"]
    user = User.query.filter_by(userId = userId).first()

    point = user.point
    mother = user.motherLanguage
    foreign = user.foreignLanguage
    #---User info from session---

    #---Selected mother and foreign language is send to form---
    mother = longToShort(mother)
    form.targetLanguage.data = mother

    foreign = longToShort(foreign)
    form.sourceLanguage.data = foreign
    #---Selected mother and foreign language is send to form---

    if request.method == "POST" and form.validate():

        form = WordsFormManuel(request.form)

        #---Getting data from WordsFormManuel form---
        word = form.word.data
        wordTranslate = form.wordTranslate.data
        sentence = form.sentence.data
        sentenceTranslate = form.sentenceTranslate.data
        source = form.sourceLanguage.data
        target = form.targetLanguage.data
        #---Getting data from WordsFormManuel form---

        source = shortToLong(source)
        target = shortToLong(target)

        isMemorized = False
      
        newWord = Word(word = word, wordTranslate = wordTranslate, sentence = sentence, sentenceTranslate = sentenceTranslate, sourceLanguage = source, targetLanguage = target, isMemorized = isMemorized, userId = userId)
     
        db.session.add(newWord)
        db.session.commit()

        user.point = user.point + 10

        point = user.point

        db.session.commit()

        flash( word + " successfully added")
        return  redirect(url_for("addbyuser" , form = form , point = point , navbarword = navbarwords()))
    
    else:

        return  render_template("addbyuser.html" , form = form , point = point , navbarword = navbarwords())

#User words
@app.route('/words', methods=["GET", "POST"])
@login_required
def words():

    #---User info from session---
    userId = session["id"]
    user = User.query.filter_by(userId = userId).first()
    #---User info from session---

    if request.method == "GET":

        words = Word.query.filter_by(userId = userId).order_by(desc("wordAddedDate")).all()

        return render_template("words.html", words = words , username = user.username , point = user.point , navbarword = navbarwords() )

    else:

        return render_template("words.html" , point = user.point , username = user.username , navbarword = navbarwords() )   

#Word delete
@app.route('/word/delete', methods = ['POST'])
@login_required
def delete():

    id = request.form.get("id")

    word = Word.query.filter_by(wordId = id).first()

    if id and word.word:

        delete = Word.query.filter_by(wordId = id).first()
        
        db.session.delete(delete)
        db.session.commit()

        userId = session["id"]

        user = User.query.filter_by(userId = userId).first()

        user.point = user.point - 20

        db.session.commit()

        flash(word.word + " successfully deleted")
        return(redirect(url_for('words')))


    return 'Not found!!!'

#Word memorize
@app.route('/word/memorize', methods=['POST'])
@login_required
def memorize():

    id = request.form.get("id")

    memorize = Word.query.filter_by(wordId = id).first()

    if memorize:

        memorize.isMemorized = True
        memorize.wordMemorizedDate = datetime.now()

        db.session.commit()

        userId = session["id"]

        user = User.query.filter_by(userId = userId).first()

        user.point = user.point + 20

        db.session.commit()

        flash(memorize.word + " successfully memorized")
        return redirect(url_for("words"))
    
    else:

        return 'Not found!!!'

#Cards
@app.route('/cards' , methods =['GET', 'POST'] )
@login_required
def cards():

    userId = session["id"]

    user = User.query.filter_by(userId = userId).first()

    if request.method == "GET":

        words = Word.query.filter_by(userId = userId).order_by(desc("wordAddedDate")).all()

        return render_template("card.html", words = words , username = user.username , point = user.point , navbarword = navbarwords())
    
    else:

        return render_template("card.html" , username = user.username , point = user.point , navbarword = navbarwords())

#Card Memorize
@app.route('/cardmemorize/<string:id>', methods=['GET', 'POST'])
@login_required
def cardMemorize(id):

    memorize = Word.query.filter_by(wordId = id).first()

    if memorize:

        word = memorize.word
        
        memorize.isMemorized = True
        memorize.wordMemorizedDate = datetime.now()

        db.session.commit()

        userId = session["id"]

        user = User.query.filter_by(userId = userId).first()

        user.point = user.point + 20

        db.session.commit()

        flash(word + " successfully memorized")
        return redirect(url_for("cards"))
    
    else:

        return 'Not found!'

#Memorized
@app.route('/memorized' , methods =['GET', 'POST'])
@login_required
def memorized():

    #---User info from session---
    userId = session["id"]
    user = User.query.filter_by(userId = userId).first()
    #---User info from session---

    if request.method == "GET":

        words = Word.query.filter_by(userId = userId).all()

        return render_template("ezberlenenler.html", words = words , username = user.username , navbarword = navbarwords())

    return render_template("ezberlenenler.html" , navbarword = navbarwords())


#Kullanıcılara ulaşma EN SON <a href="{{ url_for('get_user',username = session['username']) }}"
@app.route("/user", methods=['GET', 'POST'])
@login_required
def get_user():

    userId = session["id"]

    user = User.query.filter_by(userId = userId).first()

    if user.username == session["username"]:

        if request.method == "GET":

            return redirect(url_for("user", username = user.username))
    
    else:
        
        return 'User not found!'

@app.route("/@<string:username>")
@login_required
def user(username):
    
    return render_template("layout.html" , navbarword = navbarwords(), point = session["point"]) +username
          
@app.errorhandler(404)
def not_found(e):
    return render_template("error404.html")

@app.errorhandler(404)
def not_found(e):
    return 'Do not have access.'