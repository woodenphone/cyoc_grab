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
# stdlib
import logging
import logging.handlers
import subprocess
import time
import datetime
import hashlib
import os
import random
import shutil
import argparse
# local
#import config



USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
WPULL_PATH = 'wpull'
PROJECT_NAME = 'cyoc'
VERSION = '2016-06-18.1'# YYYY-MM-DD.<version that day>
WPULL_HOOKS_SCRIPT = os.path.join(os.getcwd(), 'cyoc_wpull_hooks.py')

def get_hash(filename):
    with open(filename, 'rb') as in_file:
        return hashlib.sha1(in_file.read()).hexdigest()

RUNNER_SHA1 = get_hash(os.path.join(os.getcwd(), 'cyoc_wpull.py'))
WPULL_HOOKS_SHA1 = get_hash(WPULL_HOOKS_SCRIPT)


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
        base, ext = os.path.splitext(log_file_path)
        log_file_path = base+"_"+timestamp_string+ext

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


def generate_job_name(job_type, low_id, high_id):
    """cyoc-img_story.1-100.2016-6-18_12.34.56"""
    job_name = '%s.%s.%s-%s.%s' % (PROJECT_NAME, job_type, low_id, high_id, time.strftime("%Y-%m-%d_%H.%M.%S"))
    return job_name


def generate_img_story_url_list(low_id, high_id):
    """Make a list of URLs for CYOC image story pages for the given range (Low inclusive, high exclusive)"""
    url_list = []
    nums = list(range(int(low_id), int(high_id)))
    random.shuffle(nums)
    for num in nums:
        url_list.append(
        'http://www.cyoc.net/modules.php?op=modload&name=Image_Stories&file=view_story&story_id={0}'.format(num)
        )
    return url_list


def generate_normal_story_url_list(low_id, high_id):
    """Make a list of URLs for CYOC regular story pages for the given range (Low inclusive, high exclusive)"""
    url_list = []
    nums = list(range(int(low_id), int(high_id)))
    random.shuffle(nums)
    for num in nums:
        url_list.append(
        'http://www.cyoc.net/modules.php?op=modload&name=Stories&file=article&sid={0}&mode=nested&order=0&thold=-1'.format(num)
        )
    return url_list


def generate_cyoa_outline_url_list(low_id, high_id):
    """Make a list of URLs for CYOC CYOA outline pages for the given range (Low inclusive, high exclusive)"""
    url_list = []
    nums = list(range(int(low_id), int(high_id)))
    random.shuffle(nums)
    for num in nums:
        url_list.append(
        ' http://www.cyoc.net/interactives/story_{0}/outline.html'.format(num)
        )
    return url_list


def run(job_name, url_list):
    """Invoke Wpull"""
    logging.info('begin run()')
    # Pre-generate filepaths and create directories
    if os.path.isdir(job_name):
            shutil.rmtree(job_name)
    os.makedirs(job_name)

    wpull_log_path = os.path.join(job_name, "wpull.log")
    open(wpull_log_path, "w").close()# Create file

    warc_path = os.path.join(job_name, job_name)

    db_path = os.path.join(job_name, 'wpull.db')
    open(db_path, "w").close()# Create file

    # Generate arguments to give to Wpull
    wpull_args = [
    WPULL_PATH,
    "--user-agent", USER_AGENT,
    "--output-file", wpull_log_path,
    "--no-robots",
    "--no-check-certificate",
    "--load-cookies", os.path.join(os.getcwd(), 'cyoc_cookies.txt'),
    #"--delete-after",# We only need the WARC file
    "--no-parent",
    "--database", db_path,

    "--plugin-script", WPULL_HOOKS_SCRIPT,

    "--timeout", "60",
    "--tries", "inf",

    "--wait=2",
    "--random-wait",
    "--waitretry", "30",

    "--page-requisites",# This should grab the embeds

    "--warc-file", warc_path,
    "--warc-header", "operator: Anonarchive",
    "--warc-header", "cyoc-dld-script-version: %s" % (VERSION),
    "--warc-header", "cyoc-dld-script-sha1: %s" % (RUNNER_SHA1),# In case the version string is forgotten
    "--warc-header", "cyoc-dld-hooks-sha1: %s" % (WPULL_HOOKS_SHA1),
    "--warc-header", "job_name: %s" % (job_name),
    ]

    # Append the URLs to the command
    for url in url_list:
        wpull_args.append(url)

    # Run the command
    logging.debug('wpull_args%r' % (wpull_args))
    subprocess.check_call(wpull_args)

    logging.info('end run()')
    return


def main():
    # TODO: argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('job_type', help='what job type to run (img_story, normal_story, cyoa_outline, or cyoa_chapter)',
                    type=str)
    parser.add_argument('low_id', help='low end of the range to work over (inclusive)',
                    type=int)
    parser.add_argument('high_id', help='high end of the range to work over (exclusive)',
                    type=int)
    args = parser.parse_args()
    logging.debug('args: %r' % (args))

    low_id = args.low_id
    high_id = args.high_id
    job_type = args.job_type

    # Name the job
    job_name = generate_job_name(job_type, low_id, high_id)
    logging.debug('job_name: %r' % (job_name))

    # Run the job
    if job_type == 'img_story':
        url_list = generate_img_story_url_list(low_id, high_id)
        run(job_name, url_list)

    elif job_type == 'normal_story':
        url_list = generate_normal_story_url_list(low_id, high_id)
        run(job_name, url_list)

    elif job_type == 'cyoa_outline':
        url_list = generate_cyoa_outline_url_list(low_id, high_id)
        run(job_name, url_list)

    elif job_type == 'cyoa_chapter':
        url_list = generate_cyoa_chapter_url_list(low_id, high_id)
        run(job_name, url_list)

    else:
        raise Exception('Invalid job type')
    return


if __name__ == '__main__':
    try:
        log_file_path=os.path.join('debug','run_wpull_for_picture_story_url_list_log.txt')
        setup_logging(log_file_path)

        main()

        logging.info('Finished.')

    except Exception as e:# Log fatal exceptions
        logging.critical("Unhandled exception!")
        logging.critical(str( type(e) ) )
        logging.exception(e)
        raise
