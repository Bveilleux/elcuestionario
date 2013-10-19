# -*- coding: utf-8 -*-

# Copyright (c) 2005-2013 Jochen Kupperschmidt
# Released under the terms of the GNU General Public License
#  _                               _
# | |_ ___ _____ ___ _ _ _ ___ ___| |_
# |   | . |     | ._| | | | . |  _| . /
# |_|_|___|_|_|_|___|_____|___|_| |_|_\
#   http://homework.nwsnet.de/

from random import shuffle

from flask import Blueprint, Flask, render_template

from .loader import load
from .userinput import UserInput


blueprint = Blueprint('blueprint', __name__)

questionnaire = None
evaluator = None

def create_app(questionnaire_filename):
    app = Flask(__name__)
    app.register_blueprint(blueprint)
    _load_questionnaire_and_evaluator(questionnaire_filename)
    return app


@blueprint.app_template_filter()
def shuffled(iterable):
    """Return a shuffled copy of the given iterable."""
    l = list(iterable)
    shuffle(l)
    return l

@blueprint.app_context_processor
def inject_title():
    return {
        'title': questionnaire.title,
    }

@blueprint.route('/', methods=['GET'])
def view():
    output = {
        'questionnaire': questionnaire,
        'submitted': False,
    }

    return render_template('questionnaire.html', **output)

@blueprint.route('/', methods=['POST'])
def evaluate():
    user_input = UserInput.from_request(questionnaire)

    output = {
        'username': user_input.name,
    }

    if user_input.all_questions_answered:
        result = evaluator.get_result(questionnaire, user_input)
        output['result'] = result
        return render_template('result.html', **output)
    else:
        output['questionnaire'] = questionnaire
        output['submitted'] = True
        output['user_input'] = user_input
        return render_template('questionnaire.html', **output)

def _load_questionnaire_and_evaluator(filename):
    if not filename:
        raise Exception('No questionnaire filename specified.')

    global questionnaire, evaluator
    with blueprint.open_resource(filename) as f:
        questionnaire, evaluator = load(f)
