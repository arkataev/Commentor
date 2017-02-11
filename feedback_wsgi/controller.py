from .response import success_json, render, restricted_json, page_not_found
from .request import Request
from . import database as db
import re


def validate_comment(func):
    required = ['last_name', 'first_name', 'email', 'comment']
    valid_email = lambda email: re.search(r'^\S+@\D+\.[a-z]{2,}$', email)
    valid_phone = lambda phone: re.search(r'^\+?\d?\(\d{3}\)\d{7}$', phone)
    def validator(request:'Request'):
        errors = []
        missing_fields = [i for i in required if not request.post.getvalue(i)]
        if missing_fields: errors.extend([(f, 'required') for f in missing_fields])
        if not valid_email(request.post.getvalue('email')): errors.append(('email', 'invalid'))
        if not valid_phone(request.post.getvalue('phone')): errors.append(('phone', 'invalid'))
        return func(request) if not errors else restricted_json({'errors': dict(errors)})
    return validator

@validate_comment
def add_comment(request:'Request'):
    if not request.valid_token: return restricted_json({'error': 'token mismatch'})
    error = False
    message = 'Comment successfully added!'
    user_fields = ['last_name', 'first_name', 'fam_name', 'phone', 'email', 'city']
    user_data = dict(zip(user_fields,[request.post.getvalue(field) for field in user_fields]))
    comment = request.post.getvalue('comment')
    try: db.save_comment(db.save_user(user_data), comment)
    except BaseException as e:
        error = True
        message = str(e)
    return success_json({'error': error, 'message': message})

def comment(request:'Request', **kwargs):
    regions = dict(db.get_regions())
    html = str()
    for uid in regions:
        html += '<option id={id} value={id}>{text}</option>\n'.format(**{'id':uid, 'text':regions[uid]})
    kwargs.update({'regions': html})
    return render('comment.html', **kwargs)

def delete_comment(request:'Request'):
    db.delete_comment(request.post.getvalue('comment_id'))
    return success_json({'error':False, 'message': 'Comment Deleted'})

def view_stats(request:'Request'):
    q = request.query
    region = 'region' in q
    stats = db.get_city_stats(q['region'][0]) if region else db.get_region_stats()
    html = str()
    for s in stats:
        html += "<tr><td class='location'>"
        if not region: html += "<a href=/stats?region={uid}>{region}</a>".format(region=s[1],uid=s[0])
        else: html += "{region}".format(region=s[1])
        html += "</td><td class='count'>{count}</td></tr>".format(count=s[2])
    return render('stats.html', rows=html)

def get_locations(request:'Request'):
    regions = dict(db.get_locations(request.post.getvalue('region_id')))
    return success_json(regions)

def not_found(request:'Request'):
    return page_not_found('not_found.html')

def view_comments(request:'Request'):
    comments = db.get_comments()
    html = str()
    for c in comments:
        html += '<li class="comment"><span class="user">{fname} {lname}</span><p>{comment}</p>' \
                '<button data-uid="{uid}">Delete</button></li>\n'.format(
                fname=c[2], lname=c[3], comment=c[1], uid=c[0])
    return render('view.html', comments=html)