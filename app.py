from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """this gets the pre-made surveys that are established from the surveys.py file and displays them"""
    survey_list = surveys

    """this is to set up the Flask session to capture all answers ((and reset when a user completes the survey and returns to the home page))"""
    session["responses"] = []
    return render_template('root.html', surveys=survey_list)


@app.route('/<survey_name>/questions/<int:question_id>', methods=["POST", "GET"])
def question_page(survey_name, question_id):
    responses = session["responses"]

    """this sets up each question from the correspond survey as well as every choice"""
    question_num = question_id
    survey_content = surveys[f"{survey_name}"]

    """this captures the current survey so that the redirect can occur in the /answer route"""
    current_survey = survey_name

    """these conditionals are what prevents the user from jumping ahead or using the wrong URL"""
    if(question_id > len(survey_content.questions) or question_id < 0):
        flash(f"Invalid. Finish this question before proceeding.")
        return redirect(f"/{survey_name}/questions/{len(responses)}")

    if(len(responses) != question_id):
        flash(f"Invalid question id: {question_id}. Finish this question before proceeding.")
        return redirect(f"/{survey_name}/questions/{len(responses)}")
    else:
        question = survey_content.questions[question_id]
        return render_template('question.html', q_num=question_num, question=question, survey_name=current_survey)





@app.route('/answer', methods=['POST'])
def obtain_answer():
    """this captures the users answer and then appends it."""
    answer = request.form.get("question", "Not Answered")
    current_responses_session = session["responses"]
    current_responses_session.append(answer)
    session["responses"] = current_responses_session

    """this sets up the redirect using hidden form data/post variables"""
    current_survey = request.form.get("current_survey")
    next_question = int(request.form.get("current_question")) + 1

    """this sets the conditional for to establish whether the survey is complete or not based on length of questions"""
    question_count = len(surveys[f"{current_survey}"].questions) - 1

    if(next_question > question_count):
        return redirect('/completed')
    else:
        """this appends the answer to the Flask session cookie and then redirects to the next question"""
        return redirect(f'/{current_survey}/questions/{next_question}')



@app.route('/completed')
def thank_you():
    """sends user the thank you page along with the answers that the user chose"""
    return render_template('thanks.html')


