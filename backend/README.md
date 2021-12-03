# Backend - Full Stack Trivia API

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2) **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

4. **Key Dependencies**

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

### Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## ToDo Tasks

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.

2) Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.

3. Create an endpoint to handle GET requests for all available categories.

4) Create an endpoint to DELETE question using a question ID.

5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.

6) Create a POST endpoint to get questions based on category.

7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.

8) Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.

9. Create error handlers for all expected errors including 400, 404, 422 and 500.

## API

GET `\categories`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
- _Example response:_

```
{
    "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
],
"success": true
}

```

GET `\questions?page=<page_number>`

- Fetches a paginated dictionary of 10 questions of all available categories in the database
- Request Arguments: (optional) page_number:int
- _Example response:_

```
{
    "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
    ],
    "current_category": "will be setup later",
    "questions": [
    {
    "answer": "Maya Angelou",
    "category": "4",
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
    "answer": "Muhammad Ali",
    "category": "4",
    "difficulty": 1,
    "id": 9,
    "question": "What boxer's original name is Cassius Clay?"
    },
    {
    "answer": "Apollo 13",
    "category": "5",
    "difficulty": 4,
    "id": 2,
    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
    "answer": "Tom Cruise",
    "category": "5",
    "difficulty": 4,
    "id": 4,
    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
    "answer": "Edward Scissorhands",
    "category": "5",
    "difficulty": 3,
    "id": 6,
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
    "answer": "Brazil",
    "category": "6",
    "difficulty": 3,
    "id": 10,
    "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
    "answer": "Uruguay",
    "category": "6",
    "difficulty": 4,
    "id": 11,
    "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
    "answer": "George Washington Carver",
    "category": "4",
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
    },
    {
    "answer": "Lake Victoria",
    "category": "3",
    "difficulty": 2,
    "id": 13,
    "question": "What is the largest lake in Africa?"
    },
    {
    "answer": "Agra",
    "category": "3",
    "difficulty": 2,
    "id": 15,
    "question": "The Taj Mahal is located in which Indian city?"
    }
    ],
    "success": true,
    "total_questions": 54
}

```

DELETE `/questions/<question_id>`

- Delete a question from the database
- Request Arguments: question_id:int
- Returns: response with a status of what success and return the Id of the question that was deleted
- _Example response:_

```
{
    'success': True,
    'question_deleted': 4
}

```

POST `/questions`

- Post or add a question and submit it to the database
- Request body: {question:string, answer:string, difficulty:int, category:string}
- _Example response:_

```
{
    'success': True,
    'success': 3
}

```

POST `/questions/search`

- looks in the database and fetches all questions using a substring matches that is provided by search term
- \*Request body: {searchTerm:string}
- _Example response:_

```
{
    'success': True,
    'questions': [
    {
    'id':39
    'question': 'What is the capital of Egypt?',
    'answer': 'Cairo',
    'difficulty': 2,
    'category': '3'
    }
    ],
    'total_questions': 1,
    'current_category': "None"
}
```

POST `/quizzes`

- gets or fetches a random question from the database with a specified category.
- Note: Previously asked questions are not included or asked again.

- \*Request body: {previous_questions: arr, quiz_category: {id:int, type:string}}
- _Example response:_

```
{
  "success": true
  "question": {
    'id':39
    'question': 'What is the capital of Egypt?',
    'answer': 'Cairo',
    'difficulty': 2,
    'category': '3'
  },
}
## Testing

To run the tests, run

```

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

```

```
