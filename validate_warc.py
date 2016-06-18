#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     18/06/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Stdlib
import os
# Libs
import warc
# Local


def validate_record(record):
    """Validate a page from a CYOC.net grab warc file"""
    assert(record.type == 'response')

    if ('cyoc.net/modules.php' in record.url):
        # Validate a basic story page
        html = record.payload.read()
        # Ensure user was logged in
        assert('&op=logout' in html)
        assert('You must be logged in to view this site' not in html)
        assert('Please login or Register Via the login box on the lef' not in html)

    elif ( ('cyoc.net/interactives/' in record.url) and (record.url.endswith('outline.html')) ):
        # Validate a CYOA outline page
        html = record.payload.read()
        # Ensure user was logged in
        assert('&op=logout' in html)
        assert('You are not logged in. Log in' not in html)

    elif ('cyoc.net/interactives/chapter' in record.url):
        # Validate a CYOA chapter page
        html = record.payload.read()
        # Ensure user was logged in
        assert('&op=logout' in html)
        assert('You are not logged in. Log in' not in html)

    return True# If all tests passed.


def validate_file(warc_path):
    """Validate a CYOC.net grab warc file"""
    wf = warc.open(warc_path)
    for record in wf:
        if record.type == 'response':
            validate_record(record)
    return



##warc_path = os.path.join('temp', 'cyoc.normal_story.1500-1550.2016-06-18_09.54.07.warc.gz')
##wf = warc.open(warc_path)
##for record in wf:
##    if record.type == 'response':
##        print('record.type: %r' % (record.type))
##        print('record.url: %r' % (record.url))
##        print('record.payload.length: %r' % (record.payload.length))
##        if 'cyoc.net/modules.php' in record.url:
##            # Validate basic story page
##            html = record.payload.read()
##            assert('&op=logout' in html)
##            # Ensure user was logged in
##            assert('You must be logged in to view this site' not in html)
##            assert('Please login or Register Via the login box on the lef' not in html)
##        print('')
##        print('')


def main():
    warc_path = os.path.join('temp', 'cyoc.normal_story.1500-1550.2016-06-18_09.54.07.warc.gz')
    validate_file(warc_path)

if __name__ == '__main__':
    main()
