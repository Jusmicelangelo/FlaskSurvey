from flask import Flask, render_template, request, redirect, flash
from surveys import satisfaction_survey

app = Flask (__name__)
app.config['SECRET_KEY'] = "never-tell-anybody"

responses = []

@app.route("/")
def survey():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("survey.html", title = title, instructions = instructions)


@app.route("/questions/<int:id>")
def questions(id):
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
    return render_template("thankyou.html")

@app.route("/answer", methods=["POST"])
def handling_answers():
    # get the response choice
    answer = request.form['answer']
    responses.append(answer)

    if len(responses) == len(satisfaction_survey.questions):
        return redirect ("/thankyou")
    else:
        return redirect(f"/questions/{len(responses)}")