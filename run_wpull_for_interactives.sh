# Run Wpull with the right arguments
# Needs to load cookies, restrict to desired URL patterns, save to WARC with headers,
# limit speed to prevent overloading, 
wpull\
--load-cookies cyoc_cookies.txt\
--warc-file JOBNAME.RANGE.DATE.warc\
--warc-header TODO\
--warc-max-size 20GB_TODO\
--level 1\
--page-requisites\
--accept-regex TODO\
--user-agent TODO\
--database TODO\
--no-robots\
--waitretry 30\
--wait=2\
--no-check-certificate\
-o TODO_wpull.log\