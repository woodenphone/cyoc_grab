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
import subprocess
import time
# local
import config



USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
WPULL_PATH = 'wpull'
PROJECT_NAME = 'cyoc_pic_story'



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


def run(low_id, high_id):
    logging.info('begin run()')
    job_name = '%s.%s-%s.%s' % (PROJECT_NAME, low_id, high_id, time.strftime("%Y%m%d-%H%M%S"))
    log_path = ("%s/wpull.log" % (job_name))
    warc_path = ("%s/%s" % (job_dirs, job_name))

    wpull_args = [
    WPULL_PATH,
    "--user-agent", USER_AGENT,
    "-o", log_path,
    "--warc-file", warc_path,
    ]
    logging.debug('wpull_args%r' % (wpull_args))
    subprocess.check_call(wpull_args)
    logging.info('end run()')



def main():
    try:
        setup_logging(log_file_path=os.path.join('debug','run_wpull_for_picture_story_url_list_log.txt'))

        run(low_id=1, high_id=100)

        logging.info('Finished.')

    except Exception, e:# Log fatal exceptions
        logging.critical("Unhandled exception!")
        logging.critical(str( type(e) ) )
        logging.exception(e)

if __name__ == '__main__':
    main()
