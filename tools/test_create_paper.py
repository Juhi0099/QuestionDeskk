import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QuestionsDeskApp.settings')
# ensure parent path is in sys.path
import sys
# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
django.setup()

from Users.models import User
from django.test import Client
from Questions.models import QuestionPaper

u = User.objects.first()
print('using user:', u.username)
# set a known password
u.set_password('pass1234')
u.save()

c = Client()
logged = c.login(username=u.username, password='pass1234')
print('login ok?', logged)

resp = c.post('/create/question-paper/', {
    'subject_id': '1',
    'title': 'Automated Shell Paper',
    'question_id[]': ['1', '2'],
    'assigned_mark[]': ['4', '2']
})
print('status:', resp.status_code)
try:
    print('response json:', resp.json())
except Exception as e:
    print('response content:', resp.content[:400])

print('papers count:', QuestionPaper.objects.count())
for p in QuestionPaper.objects.order_by('-id')[:5]:
    print(p.id, p.title, p.subject_id, p.created_by_id)
