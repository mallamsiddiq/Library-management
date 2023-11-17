echo Spinning up

pip install -r requirements.txt
python manage.py makemigrations
python manage.py makemigrations library
python manage.py makemigrations authapp
python manage.py migrate

python manage.py runserver 127.0.0.1:5000