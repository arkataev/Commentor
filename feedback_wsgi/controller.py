from  . import app
from .response import json_response, render


def add_comment(**kwargs):
    valid = app.validate_token(kwargs['token'])
    text = "valid" if valid else 'Not valid'
    return json_response(**{'text': text})

def comment(**kwargs):
    return render('comment.html', **kwargs)

def delete_comment(uid):
    pass

def view_stats(**kwargs):
    data = {'text': 'These are some cool nums '}
    return render('stats.html', **data)

def get_stats():
    # returns json object with statistics
    pass

def get_locations(region_uid):
    pass

def view_comments(**kwargs):
    html = '<h1>$text</h1>\n<p>$text1</p>'
    data = {
        'embed_html': html,
        'vars': {
            'text': 'View all comments',
            'text1':'Here we have some new comments'
        }
    }
    return render('view.html', **data)