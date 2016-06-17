#-------------------------------------------------------------------------------
# Name:        module1
# Purpose: Get cookie for wget/wpull/httrack
#
# Author:      User
#
# Created:     17/06/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# StdLib
import logging
import logging.handlers
import datetime
import os
import cookielib
import time
import random
# Libs
import requests
# Local
import config




def setup_logging(log_file_path,timestamp_filename=True,max_log_size=104857600):
    """Setup logging (Before running any other code)
    http://inventwithpython.com/blog/2012/04/06/stop-using-print-for-debugging-a-5-minute-quickstart-guide-to-pythons-logging-module/
    """
    assert( len(log_file_path) > 1 )
    assert( type(log_file_path) == type("") )
    global logger

    # Make sure output dir(s) exists
    log_file_folder =  os.path.dirname(log_file_path)
    if log_file_folder is not None:
        if not os.path.exists(log_file_folder):
            os.makedirs(log_file_folder)

    # Add timetamp for filename if needed
    if timestamp_filename:
        # http://stackoverflow.com/questions/8472413/add-utc-time-to-filename-python
        # '2015-06-30-13.44.15'
        timestamp_string = datetime.datetime.utcnow().strftime("%Y-%m-%d %H.%M.%S%Z")
        # Full log
        log_file_path = add_timestamp_to_log_filename(log_file_path,timestamp_string)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # 2015-07-21 18:56:23,428 - t.11028 - INFO - ln.156 - Loading page 0 of posts for u'mlpgdraws.tumblr.com'
    formatter = logging.Formatter("%(asctime)s - t.%(thread)d - %(levelname)s - ln.%(lineno)d - %(message)s")

    # File 1, log everything
    # https://docs.python.org/2/library/logging.handlers.html
    # Rollover occurs whenever the current log file is nearly maxBytes in length; if either of maxBytes or backupCount is zero, rollover never occurs.
    fh = logging.handlers.RotatingFileHandler(
        filename=log_file_path,
        # https://en.wikipedia.org/wiki/Binary_prefix
        # 104857600 100MiB
        maxBytes=max_log_size,
        backupCount=10000,# Ten thousand should be enough to crash before we reach it.
        )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Console output
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logging.info("Logging started.")
    return logger


def add_timestamp_to_log_filename(log_file_path,timestamp_string):
    """Insert a string before a file extention"""
    base, ext = os.path.splitext(log_file_path)
    return base+"_"+timestamp_string+ext



def fetch(requests_session, url, method='get', data=None, expect_status=200, headers=None):
#    headers = {'user-agent': user_agent}
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
    if headers is None:
        headers = {'user-agent': user_agent}
    elif 'user-agent' not in headers.keys():
        headers['user-agent'] = user_agent


    if headers:
        headers.update(headers)

    for try_num in range(10):
        logging.debug('Fetch %s' % (url))
        if try_num > 1:
            time.sleep(try_num*30)# Back off a bit if something goes wrong

        try:
            if method == 'get':
                response = requests_session.get(url, headers=headers, timeout=300)
            elif method == 'post':
                response = requests_session.post(url, headers=headers, data=data, timeout=300)
            else:
                raise Exception('Unknown method')
        except requests.exceptions.Timeout, err:
            logging.exception(err)
            logging.error('Caught requests.exceptions.Timeout')
            continue
        except requests.exceptions.ConnectionError, err:
            logging.exception(err)
            logging.error('Caught requests.exceptions.ConnectionError')
            continue
        except requests.exceptions.ChunkedEncodingError, err:
            logging.exception(err)
            logging.error('Caught requests.exceptions.ChunkedEncodingError')
            continue

        save_file(
            file_path = os.path.join("debug","fetch_last_response.txt"),
            data = response.content,
            force_save = True,
            allow_fail = True
            )
        if response.status_code == 404:
            logging.error("fetch() 404 for url: %s" % url)
            time.sleep(random.uniform(0.5, 1.5))
            raise FetchGot404(url=url, response=response)
        if response.status_code == 500:
            logging.error("fetch() 500 for url: %s" % url)
            # Error cases where we want to retry
            if (
                ('<h1>CDbException</h1>' in response.content) and
                ('p>CDbCommand failed to execute the SQL statement: SQLSTATE[08S01]: Communication link failure: 1047 WSREP has not yet prepared node for application use</p>' in response.content)
                ):
                logging.error('Caught CDbException, retrying')
                continue
            raise FetchGot500(url=url, response=response)


        if response.status_code != expect_status:
            logging.error('Expected status code: %s but got status code: %s . Sleeping.' % (expect_status, response.status_code))
            time.sleep(60*try_num)
        else:
            time.sleep(random.uniform(0.5, 1.5))
            return response

    raise Exception('Giving up!')


def save_file(file_path,data,force_save=False,allow_fail=False):
    counter = 0
    while counter <= 10:
        counter += 1

        if not force_save:
            if os.path.exists(file_path):
                logging.debug("save_file()"" File already exists! "+repr(file_path))
                return
        foldername = os.path.dirname(file_path)
        if len(foldername) != 0:
            if not os.path.exists(foldername):
                try:
                    os.makedirs(foldername)
                except WindowsError, err:
                    pass
        try:
            file = open(file_path, "wb")
            file.write(data)
            file.close()
            return
        except IOError, err:
            logging.exception(err)
            logging.error(repr(file_path))
            time.sleep(1)
            continue
    logging.warning("save_file() Too many failed write attempts! "+repr(file_path))
    if allow_fail:
        return
    else:
        logging.critical("save_file() Passing on exception")
        logging.critical(repr(file_path))
        raise



def log_in_to_cyoc(requests_session, login_username, login_password):
    """Log in"""
    logging.info('Logging in as %s' % (login_username))
    logging.debug('requests_session.cookies: %s' % (requests_session.cookies))

    # Load front page
    pre_login_response = fetch(
        requests_session=requests_session,
        url='http://www.cyoc.net/index.php',
        method='get',
        expect_status=200,
    )
    logging.debug('pre_login requests_session.cookies: %s' % (requests_session.cookies))

    # Send login request
    login_response = fetch(
        requests_session=requests_session,
        url='http://www.cyoc.net/user.php',
        method='post',
        expect_status=200,
        headers={
            'origin': 'http://www.cyoc.net',
            'pragma': 'no-cache',
            'referer': 'http://www.cyoc.net/index.php',
        },
        data={
            'YII_CSRF_TOKEN': '',
            'uname': login_username,
            'pass': login_password,
            'rememberme': 1,
            'module': 'User',
            'op': 'login',
            'url': 'http://www.cyoc.net/index.php',
        }
    )
    logging.debug('login requests_session.cookies: %s' % (requests_session.cookies))
    save_file(
        file_path = os.path.join("debug","login_response.html"),
        data = login_response.content,
        force_save = True,
        allow_fail = True
    )

    # Follow redirect
    post_login_response = fetch(
        requests_session=requests_session,
        url='http://www.cyoc.net/index.php',
        method='get',
        expect_status=200,
    )
    logging.debug('post_login requests_session.cookies: %s' % (requests_session.cookies))
    save_file(
        file_path = os.path.join("debug","post_login_response.html"),
        data = post_login_response.content,
        force_save = True,
        allow_fail = True
    )

    # Verify we actually logged in
    assert (login_username in post_login_response.content)# Username should be visible
    assert ('user.php?module=NS-User&op=logout' in post_login_response.content)# Logout link should be visible


    logging.info('Logged in as %s' % (login_username))
    return




def main():
    try:
        setup_logging(log_file_path=os.path.join('debug','get_cookie_log.txt'))

        # Setup requests session
        requests_session = requests.Session()
        requests_session.cookies = cookie_jar = cookielib.MozillaCookieJar('cyoc_cookies.txt')

        # Log in
        log_in_to_cyoc(requests_session, config.login_username, config.login_password)
        logging.debug('requests_session.cookies: %s' % (requests_session.cookies))

        # Save cookies to file
        cookie_jar.save()

        logging.info('Finished.')

    except Exception, e:# Log fatal exceptions
        logging.critical("Unhandled exception!")
        logging.critical(str( type(e) ) )
        logging.exception(e)

if __name__ == '__main__':
    main()
