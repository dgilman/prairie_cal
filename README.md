prairie\_cal.py
===============

`prairie_cal.py` is a CGI script which generates an iCal format calendar based off of Silicon Prairie News' calendar page at [http://www.siliconprairienews.com/events](http://www.siliconprairienews.com/events).

This script is hosted [here](http://dgilman.xen.prgmr.com/prairie_cal/prairie_cal.py) and you're welcome to use that link instead of running the program yourself.

Running your own prairie\_cal.py
--------------------------------

`prairie_cal.py` has dependencies on lxml, pytz and icalendar.

Most people probably haven't configured Apache to use a CGI script in years.  Here's a refresher:

    <Directory "/var/www/prairie_cal">
        Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
        AddHandler cgi-script .py
    </Directory>
