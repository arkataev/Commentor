from functools import partial
from .response import set_token, response
from . import controller
from . import request
from .template import Renderer


def dispatch(request:'request.Request'):
    if request.is_static: return serve_statics
    return {
        '/comment': partial(controller.comment, csrf=set_token()),
        '/stats': controller.view_stats,
        '/view': controller.view_comments,
        '/save_comment': controller.add_comment,
        '/delete_comment': controller.delete_comment,
        '/get_locations': controller.get_locations,
    }.get(request.route, controller.not_found)

def serve_statics(request:'request.Request'):
    resp = response(content_type=request.content_type)
    path = '/'.join(request.route[1:].split('/')[1:])
    return resp(Renderer().render)(path)