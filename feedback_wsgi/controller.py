from .response import success_json, render, restricted_json, page_not_found
from .request import Request


def add_comment(request:'Request'):
    if not request.valid_token: return restricted_json({'error':'token mismatch'})
    return success_json({'text': 'hello'})

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

def not_found(request:'Request'):
    return page_not_found('not_found.html')

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