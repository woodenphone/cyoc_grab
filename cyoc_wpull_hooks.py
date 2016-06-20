# encoding=utf-8
# This file is python 3 code because that's what Wpull wants
print('cyoc_wpull_hooks.py first line')

import datetime
import re

from wpull.application.hook import Actions
from wpull.application.plugin import WpullPlugin, PluginFunctions, hook, event

from wpull.protocol.abstract.request import BaseResponse
from wpull.pipeline.session import ItemSession

print('cyoc_wpull_hooks.py after imports')

class MyExamplePlugin(WpullPlugin):

    @hook(PluginFunctions.handle_response)
    def my_handle_response(self, item_session):
        print('cyoc_wpull_hooks.py my_handle_response() start')
        if item_session.response.response_code == 429:
            return Actions.STOP
        page_data = str( item_session.response.body.content() )
        #print(''.format())

        # Kill run if not logged in
        exclude_strings = [
            'You must be logged in to view this site',
            'Please login or Register Via the login box on the lef',
            'You are not logged in. Log in',
        ]
        for exclude_string in exclude_strings:
            if (exclude_string in page_data):
                print('cyoc_wpull_hooks.py exclude_string matched: {0}'.format(exclude_string))
                return Actions.STOP

        return Actions.NORMAL# If we don't have any input to make


print('cyoc_wpull_hooks.py last line')