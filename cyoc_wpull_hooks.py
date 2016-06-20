#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     19/06/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------



# https://wpull.readthedocs.io/en/master/scripting.html
import datetime
import re

from wpull.application.hook import Actions
from wpull.application.plugin import WpullPlugin, PluginFunctions, hook
from wpull.protocol.abstract.request import BaseResponse
from wpull.pipeline.session import ItemSession


class MyExamplePlugin(WpullPlugin):
    def activate(self):
        super().activate()
        print('Hello world!')

    def deactivate(self):
        super().deactivate()
        print('Goodbye world!')

    @hook(PluginFunctions.accept_url)
    def my_accept_func(self, item_session, verdict, reasons):
        return 'dog' not in item_session.request.url

    @event(PluginFunctions.get_urls)
    def my_get_urls(self, item_session):
        print('MyExamplePlugin.my_get_urls(): dir(item_session): {0}'.format( repr(dir(item_session)) ) )
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
    def my_handle_response(item_session):
        if item_session.response.response_code == 429:
            return Actions.STOP
















def main():
    pass

if __name__ == '__main__':
    main()
