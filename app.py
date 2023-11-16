from flask import Flask, render_template, request, redirect, flash, session
from surveys import satisfaction_survey

app = Flask (__name__)
app.config['SECRET_KEY'] = "never-tell-anybody"


@app.route("/")
def survey():
    """Starting Page of the Survey"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("survey.html", title = title, instructions = instructions)

@app.route("/session", methods=["POST"])
def handle_session():
    """Clearing Responses"""
    session["responses"] =[]

    return redirect("/questions/0")


@app.route("/questions/<int:id>")
def questions(id):
    """Hanlding the questions"""
    responses = session.get("responses")

    if id <= len(satisfaction_survey.questions):    
        question = satisfaction_survey.questions[id]
        choice_a = question.choices[0]
        choice_b = question.choices[1] 
    else:
        flash("You have tryied to access an invalid question, we directed you to the next valid!")
    if id > len(satisfaction_survey.questions):
        return redirect(f"/questions/{len(responses)}")
    if len(responses) != id:
        return redirect(f"/questions/{len(responses)}")
    else:
        return render_template("questions.html", question= question, choice_a=choice_a, choice_b=choice_b)

@app.route("/thankyou")
def thank_you():
    """Informing that survey is over"""
    return render_template("thankyou.html")

@app.route("/answer", methods=["POST"])
def handling_answers():
    """Handling Responses"""

    # get the response choice
    answer = request.form['answer']
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect ("/thankyou")
    else:
        return redirect(f"/questions/{len(responses)}")