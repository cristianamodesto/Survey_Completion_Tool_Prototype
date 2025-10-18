Before cloning, perform the following git command: git lfs install 

After cloning, perform the following git command in the project folder: git lfs pull

If first time running the tool:

    Make sure the following are installed: 
      Python
      PIP
      venv 
        To install: python -m venv name_of_virtual_environment
        To activate: name_of_virtual_environment\Scripts\activate.bat
      Django
        To install: python -m pip install Django (Note: venv must be activated)
      requests
        To install: python -m pip install requests (Note: venv must be activated)
      whitenoise
        To install: pip install whitenoise (Note: venv must be activated)
      psycopg2-binary
        To install: pip install psycopg2-binary (Note: venv must be activated)

    To create the local database:
      cd fps
      py manage.py migrate
    
    To collect all static files:
      py manage.py collectstatic
    
    To run the app:
      py manage.py runserver
    
      In the browser:
      http://127.0.0.1:8000/
      
In the following times:

    Activate venv: name_of_virtual_environment\Scripts\activate.bat
    
    If changes were performed to the database schema:
      cd fps
      py manage.py makemigrations
      py manage.py migrate
    
    If changes were performed to static files:
      cd fps
      py manage.py collectstatic
    
    To run the app:
        cd fps
        py manage.py runserver
        
          In the browser:
          http://127.0.0.1:8000/
