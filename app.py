from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# This sets up our fake database:
responses = []

@app.route('/')
def home_page():
    """this gets the pre-made surveys that are established from the surveys.py file and displays them"""
    survey_list = surveys
    return render_template('root.html', surveys=survey_list)


@app.route('/<survey_name>/questions/<int:question_id>', methods=["POST", "GET"])
def question_page(survey_name, question_id):
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
        return render_template('question.html', q_num=question_num, question=question, responses=responses, survey_name=current_survey)
        """TO-DO: Get rid of current_responses from above and within the render_template as we want this to occur on the backend"""





@app.route('/answer', methods=['POST'])
def obtain_answer():
    """this specifically captures the answer and then appends it to the responses list in surveys.py"""
    answer = request.form.get("question", "not answered")
    current_responses = responses
    if answer != None:
        current_responses.append(answer)

    """this sets up the redirect using hidden form data/post variables"""
    current_survey = request.form.get("current_survey")
    next_question = int(request.form.get("current_question")) + 1

    """this sets the conditional for to establish whether the survey is complete or not based on length of questions"""
    question_count = len(surveys[f"{current_survey}"].questions) - 1

    if(next_question > question_count):
        return redirect('/completed')
    else:
        return redirect(f'/{current_survey}/questions/{next_question}')



@app.route('/completed')
def thank_you():
    return render_template('thanks.html')




# To do: add sessions --  once that is learned.