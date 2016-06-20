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
    print('cyoc_wpull_hooks.py inside class')
    # def activate(self):
    #     super().activate()
    #     print('Hello world!')

    # def deactivate(self):
    #     print('cyoc_wpull_hooks.py deactivate()')
    #     super().deactivate()
    #     print('Goodbye world!')

    @hook(PluginFunctions.accept_url)
    def my_accept_func(self, item_session, verdict, reasons):
        print('cyoc_wpull_hooks.py my_accept_func() start')
        return 'dog' not in item_session.request.url

    @event(PluginFunctions.get_urls)
    def my_get_urls(self, item_session):
        print('cyoc_wpull_hooks.py my_get_urls() start')
        if item_session.request.url_info.path != '/':
            return
        #print('cyoc_wpull_hooks.py my_get_urls() repr(locals()): {0}'.format(repr(locals())))
        #print('item_session.response.body.content: {0}'.format(item_session.response.body.content))
        #print('item_session.response.body.content(): {0}'.format(item_session.response.body.content()))
        string_to_search = str(item_session.response.body.content())
        #print('repr(string_to_search): {0}'.format(repr(string_to_search)))
        print('type(string_to_search): {0}'.format(type(string_to_search)))
        matches = re.finditer( r'<div id="profile-(\w+)"',  string_to_search)
        print('cyoc_wpull_hooks.py my_get_urls() after regex run')
        for match in matches:
            url = 'http://example.com/profile.php?username={}'.format( match.group(1) )
            print('cyoc_wpull_hooks.py my_get_urls() adding match')
            item_session.add_child_url(url)
            print('cyoc_wpull_hooks.py my_get_urls() after adding match')
        print('cyoc_wpull_hooks.py my_get_urls() end')
        return

    @hook(PluginFunctions.handle_response)
    def my_handle_response(self, item_session):
        print('cyoc_wpull_hooks.py my_handle_response() start')
        if item_session.response.response_code == 429:
            return Actions.STOP
        return Actions.NORMAL


print('cyoc_wpull_hooks.py last line')