print('cyoc_wpull_hooks.py first line')

import datetime
import re

from wpull.application.hook import Actions
from wpull.application.plugin import WpullPlugin, PluginFunctions, hook, event

from wpull.protocol.abstract.request import BaseResponse
from wpull.pipeline.session import ItemSession

print('cyoc_wpull_hooks.py after imports')

try:

    class MyExamplePlugin(WpullPlugin):
        print('cyoc_wpull_hooks.py inside class')
        def activate(self):
            super().activate()
            print('Hello world!')

        def deactivate(self):
            super().deactivate()
            print('Goodbye world!')

        @hook(PluginFunctions.accept_url)
        def my_accept_func(self, item_session, verdict, reasons):
            print('cyoc_wpull_hooks.py my_accept_func() start')
            return 'dog' not in item_session.request.url

        @event(PluginFunctions.get_urls)
        def my_get_urls(self, item_session):
            print('cyoc_wpull_hooks.py my_get_urls() start')
            if item_session.request.url_info.path != '/':
                return

            matches = re.finditer(
                r'<div id="profile-(\w+)"', item_session.response.body.content
            )
            for match in matches:
                url = 'http://example.com/profile.php?username={}'.format(
                    match.group(1)
                )
                item_session.add_child_url(url)

        @hook(PluginFunctions.handle_response)
        def my_handle_response(self, item_session):
            print('cyoc_wpull_hooks.py my_handle_response() start')
            if item_session.response.response_code == 429:
                return Actions.STOP

except Exception as err:
    print(repr(err))

print('cyoc_wpull_hooks.py last line')