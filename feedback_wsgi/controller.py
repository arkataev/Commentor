from  . import app
from .response import json_response, render


def add_comment(token):
    valid = app.validate_token(token)
    text = "valid" if valid else 'Not valid'
    return json_response(**{'text': text})

def comment(**kwargs):
    return render('comment.html', **kwargs)

def delete_comment(uid):
    pass

def get_stats():
    pass

def get_locations(region_uid):
    pass

def view_comments(**kwargs):
    data = {'text': 'View all comments'}
    return render('view.html', **data)