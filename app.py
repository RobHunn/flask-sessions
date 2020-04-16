from flask import Flask, render_template, request, redirect, jsonify,flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, surveys
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
RESPONSES_KEY = 'responces'
responses = []
@app.route('/')
def home():
    serv = surveys['satisfaction']
    title = serv.title
    instructions = serv.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route('/questions/<int:id>',methods=['GET','POST'])
def handel_questions(id):
    responses = session.get(RESPONSES_KEY)
    serv_len = len(list(surveys['satisfaction'].questions))
    if (len(responses) == serv_len):
        return render_template('end.html')

    if (len(responses) != id):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(responses)}")

    serv = surveys['satisfaction'].questions[id]
    return render_template('question.html', ask_question=serv, id=id)


@app.route('/answers', methods=['POST'])
def handel_answers():
    serv_len = len(list(surveys['satisfaction'].questions))
    choice = request.form['answer']
    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    if (len(responses) == serv_len):
        # They've answered all the questions! Thank them.
        return render_template('end.html')
    else:
        return redirect(f"/questions/{len(responses)}")
   
