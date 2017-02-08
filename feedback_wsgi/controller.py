from .response import success_json, render, restricted_json, page_not_found
from .request import Request
from . import database as db

def add_comment(request:'Request'):
    if not request.valid_token: return restricted_json({'error':'token mismatch'})
    user_fields = ['last_name', 'first_name', 'fam_name', 'phone', 'email']
    city = request.post.getvalue('city')
    comment = request.post.getvalue('comment')
    user_data = dict(zip(user_fields,[request.post.getvalue(field) for field in user_fields]))
    # Insert into users table user data + city_id to DB if not exists, get last_id
    # insert commment into comments table using user last_id
    comm_id = db.save_comment(user_data)
    return success_json(user_data)

def comment(request:'Request', **kwargs):
    regions = dict(db.get_regions())
    html = ''
    for uid in regions:
        html += '<option id={id} value={id}>{text}</option>\n'.format(**{'id':uid, 'text':regions[uid]})
    kwargs.update({'regions': html})
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
    regions = dict(db.get_locations(request.post.getvalue('region_id')))
    return success_json(regions)

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