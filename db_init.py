import os
a = os.system('find . -path "*/migrations/*.py"')
print(a)
b = os.system('find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')
print(b)
os.system('python manage.py makemigrations')
os.system('python manage.py migrate')

#os.system('python input_data.py')