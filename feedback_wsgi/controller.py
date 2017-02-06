from .response import json_response, render
from .request import Request


def add_comment(request:'Request'):
    text = "valid" if request.valid_token else 'Not valid'
    return json_response(**{'text': text})

def comment(request:'Request', **kwargs):
    return render('comment.html', **kwargs)

def delete_comment(request:'Request'):
    pass

def view_stats(request:'Request'):
    data = {'text': 'These are some cool nums '}
    return render('stats.html', **data)

def get_stats(request:'Request'):
    # returns json object with statistics
    pass

def get_locations(request:'Request'):
    pass

def view_comments(request:'request.Request'):
    html = '<h1>$text</h1>\n<p>$text1</p>'
    data = {
        'embed_html': html,
        'vars': {
            'text': 'View all comments',
            'text1':'Here we have some new comments'
        }
    }
    return render('view.html', **data)