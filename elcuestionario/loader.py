# -*- coding: utf-8 -*-

# Copyright (c) 2005-2013 Jochen Kupperschmidt
# Released under the terms of the GNU General Public License
#  _                               _
# | |_ ___ _____ ___ _ _ _ ___ ___| |_
# |   | . |     | ._| | | | . |  _| . /
# |_|_|___|_|_|_|___|_____|___|_| |_|_\
#   http://homework.nwsnet.de/

import json

from .evaluation import Evaluator, RatingLevel
from .questionnaire import Answer, Question, Questionnaire


def load(f):
    """Load questionnaire and rating results from a file-like object."""
    data = json.load(f)
    questionnaire = load_questionnaire(data)
    evaluator = load_evaluator(data)
    return questionnaire, evaluator

def load_questionnaire(data):
    title = _load_title(data)

    questionnaire = Questionnaire(title)

    for question, answers in _load_questions(data, questionnaire):
        questionnaire.add_question_with_answers(question, answers)

    return questionnaire

def _load_title(data):
    return data['title']

def _load_questions(data, questionnaire):
    return map(
        lambda question_data: _load_question(question_data, questionnaire),
        data['questions'])

def _load_question(data, questionnaire):
    text = data['text']
    question = Question(text)
    answers = _load_answers(data)
    return question, answers

def _load_answers(data):
    return frozenset(map(_load_answer, data['answers']))

def _load_answer(data):
    text = data['text']
    weighting = float(data['weighting'])
    return Answer(text, weighting)

def load_evaluator(data):
    rating_levels = list(_load_rating_levels(data))
    return Evaluator(rating_levels)

def _load_rating_levels(data):
    for rating_level in data['rating_levels']:
        minimum_score = int(rating_level['minimum_score'])
        text = rating_level['text']
        yield RatingLevel(minimum_score, text)
