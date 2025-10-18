ferramenta_de_preenchimento_de_questionarios
Source code of the survey completion tool, to run locally.

If first time running the tool:

Make sure the following are installed: 
  Python
  PIP
  venv 
    To install: python -m venv name_of_virtual_environment
    To activate: name_of_virtual_environment\Scripts\activate.bat
  Django
    To install: python -m pip install Django (Note: venv must be activated)

To create all the tables in the local database:
  py manage.py migrate

To collect all static files:
  py manage.py collectstatic

To run the app:
  py manage.py runserver

  In the browser:
  http://127.0.0.1:8000/
In the following times, just do this:

  Activate venv: name_of_virtual_environment\Scripts\activate.bat

  If changes were performed to the database schema:
    python manage.py makemigrations
    py manage.py migrate

  If changes were performed to static files:
    py manage.py collectstatic

  To run the app:
  py manage.py runserver

    In the browser:
    http://127.0.0.1:8000/