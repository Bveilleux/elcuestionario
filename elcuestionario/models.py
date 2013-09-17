# -*- coding: utf-8 -*-

# Copyright (c) 2005-2013 Jochen Kupperschmidt
# Released under the terms of the GNU General Public License
#  _                               _
# | |_ ___ _____ ___ _ _ _ ___ ___| |_
# |   | . |     | ._| | | | . |  _| . /
# |_|_|___|_|_|_|___|_____|___|_| |_|_\
#   http://homework.nwsnet.de/

from collections import defaultdict, namedtuple
import hashlib

from .evaluation import Evaluator


class Questionnaire(object):
    """A set of questions, answers, selection states and rating levels."""

    def __init__(self, title):
        self.title = title
        self._questions = []
        self._question_answers = defaultdict(dict)
        self.rating_levels = []

    def add_question(self, question):
        self._questions.append(question)

    def get_question(self, hash):
        """Return the question for the given hash."""
        for question in self._questions:
            if question.hash == hash:
                return question

    def get_questions(self):
        return self._questions

    def get_question_hashes(self):
        return (question.hash for question in self.get_questions())

    def add_answer_for_question(self, question, answer):
        self._question_answers[question.hash][answer.hash] = answer

    def get_answers_for_question(self, question):
        return self._question_answers[question.hash].values()

    def get_answer_by_hash(self, question, answer_hash):
        return self._question_answers[question.hash][answer_hash]

    def select_answer_to_question(self, question_hash, answer_hash):
        """Answer the referenced question with the referenced answer."""
        question = self.get_question(question_hash)
        answer = self.get_answer_by_hash(question, answer_hash)
        question.select_answer(answer)

    def add_rating_level(self, rating_level):
        self.rating_levels.append(rating_level)

    def get_result(self, user_input):
        evaluator = Evaluator(self.rating_levels)
        return evaluator.get_result(self, user_input)


class Question(namedtuple('Question', 'text hash')):

    def __new__(cls, text):
        hash = _create_hash(text.encode('latin-1'))
        return super(Question, cls).__new__(cls, text, hash)


class Answer(namedtuple('Answer', 'text weighting hash')):

    def __new__(cls, text, weighting):
        hash = _create_hash(text.encode('latin-1'))
        return super(Answer, cls).__new__(cls, text, weighting, hash)


def _create_hash(value, length=8):
    return hashlib.sha1(value).hexdigest()[:length]
