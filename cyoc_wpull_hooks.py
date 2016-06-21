# encoding=utf-8
# This file is python 3 code because that's what Wpull wants
import datetime
import re

from wpull.application.hook import Actions
from wpull.application.plugin import WpullPlugin, PluginFunctions, hook, event
from wpull.protocol.abstract.request import BaseResponse
from wpull.pipeline.session import ItemSession


class CYOCPlugin(WpullPlugin):
    """Kill the Wpull run if we aren't logged in at some point"""
    @hook(PluginFunctions.handle_response)
    def my_handle_response(self, item_session):
        #print('cyoc_wpull_hooks.py my_handle_response() start')

        # LEARNING
        #print('{}'.format())
        #print('dir(item_session): {0}'.format(dir(item_session)))
        #print('dir(item_session.request): {0}'.format(dir(item_session.request)))
        #print('dir(item_session.response): {0}'.format(dir(item_session.response)))
        # Get important data about this request
        url = item_session.request.url
        status_code = item_session.response.response_code
        page_data = str( item_session.response.body.content() )
        #print('repr(url): {0}'.format(repr(url)))
        #print('repr(status_code): {0}'.format(repr(status_code())))
        # /LEARNING

        # Only check logged in status of target pages, not images, CSS, JS, etc
        if (
            ('cyoc.net/modules.php?op=modload&name=Stories&file=article&sid='.lower() in url.lower()) or# Basic stories
            ('cyoc.net/modules.php?op=modload&name=Image_Stories&file=view_story&story_id'.lower() in url.lower()) or# Image stories
            ('outline.html'.lower() in url.lower()) or# CYOA Outlines
            ('cyoc.net/interactives/chapter_'.lower() in url.lower())# CYOA Chapters
            ):
            # Kill run if not logged in
            lc_page_data = page_data.lower()# Lowercase for easier comparisons
            exclude_strings = [
                'You must be logged in to view this site',
                'Please login or Register Via the login box on the lef',
                'You are not logged in. Log in',
                'You are not logged in.',
            ]
            for exclude_string in exclude_strings:
                lc_exclude_string = exclude_string.lower()# Lowercase for easier comparisons
                if (lc_exclude_string in lc_page_data):
                    print('cyoc_wpull_hooks.py exclude_string matched: {0}'.format(repr(exclude_string)))
                    return(Actions.STOP)

        return Actions.NORMAL# If we don't have any input to make
