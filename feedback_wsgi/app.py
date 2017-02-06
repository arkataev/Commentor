from .response import page_not_found
from functools import partial
from .response import set_token
from . import controller


def dispatch(route):
    return {
        '/comment': partial(controller.comment, csrf=set_token()),
        '/stats': controller.view_stats,
        '/view': controller.view_comments,
        '/save_comment': controller.add_comment,
        '/delete_comment': controller.delete_comment,
        '/get_locations': controller.get_locations,
    }.get(route, partial(page_not_found, fname='not_found.html'))
