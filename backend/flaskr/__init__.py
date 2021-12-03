import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category
import json
QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    # starting from zero so page -1
    page = request.args.get('page', 1, type=int) - 1

    start = page * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    # create list of all questions as question formate id , question , answer etc
    questions = [question.format() for question in questions]

    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  Set up CORS. Allow '*' for origins.
  '''
    CORS(app, resources={'/': {'origins': '*'}})

    '''
  Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.all()
            category_types_arr = []
            for category in categories:
                category_types_arr.append(category.type)

            if ((len(category_types_arr))):
                print("no category type in database")

            return jsonify({
                'success': True,
                'categories': category_types_arr
            })
        except Exception:
            abort(500)

    '''
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''

    @app.route('/questions')
    def get_questions():
        #  query all questions
        questions = Question.query.all()
        print(questions)

        # find out how many question there are
        total_questions = len(questions)

        current_questions = paginate_questions(request, questions)
        print("CURRENT Qs", current_questions)

        categories = Category.query.all()
        category_types = []
        for category in categories:
            category_types.append(category.type)

        if (len(current_questions) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'categories': category_types,
            'current_category': 'will be setup later'
        })

    '''
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is not None:
            # delete that question with that id
            question.delete()

            # question has something in it and it is not none - return success message
            return jsonify({
                'success': True
            })
        # if the question is none - not found in the database
        # was deleted
        # not found - return 404 error
        abort(404)

    '''
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions', methods=['POST'])
    def post_question():

        # get the form info form the from
        body = request.get_json()

        if body:
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_difficulty = body.get('difficulty', None)
            new_category = body.get('category', None)

        try:
            question = Question(question=new_question, answer=new_answer,
                                difficulty=new_difficulty, category=new_category)

            # commit to the database
            question.insert()

            selection = Question.query.order_by(Question.id).all()

            return jsonify({
                'success': True,
                'created': question.id
            })

        except:
            abort(404)

    '''
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        # get the form info form the from
        body = request.get_json()

        # get the search term
        search_term = body.get('searchTerm')

        if search_term:
            search_results = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            # get all the questions
            questions = paginate_questions(request, search_results)
            print(search_term)
            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(search_results),
                'current_category': "None"
            })

        else:
            abort(404)
    '''
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):

        # # get the category by id
        questions = Question.query.filter(
            Question.category == str(category_id)).all()

        # make list of all the questions form that category
        all_questions_by_category = [question.format()
                                     for question in questions]
        if questions:
            return jsonify({
                'success': True,
                'questions': all_questions_by_category,
                'total_questions': len(questions),
                'current_category': category_id
            })
        abort(404)

    '''
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz_using_random_questions():

        # to access the request body
        body = request.get_json()

        category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')

        # print(category, previous_questions)

        # if click means all was selected - all the questions except previous_questions
        if category['type'] == 'click':
            questions = Question.query.filter(
                Question.id.notin_((previous_questions))).all()

        # else there is a specific category
        else:
            questions = Question.query.filter_by(
                category=category['id']).filter(Question.id.notin_((previous_questions))).all()

        # making sure that there is no none
        Not_none_values = []
        for x in questions:
            if x.answer != None:
                Not_none_values.append(x)
                print(x.answer)
        questions = []
        questions = Not_none_values

        # get ramdom question
        new_question = random.choice(questions)

        return jsonify({
            'success': True,
            'question': new_question.format() if new_question else None,
        })
        abort(404)

    '''
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "The resource is not found."
        }), 404

    return app
