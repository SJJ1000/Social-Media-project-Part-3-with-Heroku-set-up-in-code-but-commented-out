Project has a requirements.txt with all the needed packages. Below are the steps get website to work:
py -3 -m venv .venv, 
    .\.venv\Scripts\activate, 
 pip install -U pip, 
 pip install -r requirements.txt, 
 python manage.py makemigrations, 
 python manage.py migrate, 
 python manage.py runserver
