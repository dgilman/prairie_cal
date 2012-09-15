#!/usr/bin/env python
# vim: ts=3 et sw=3 sts=3:

# Copyright 2012 David Gilman
#
# This file is part of prairie_cal.
#
# atom_maker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# atom_maker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with atom_maker.  If not, see <http://www.gnu.org/licenses/>.

from lxml import html
import datetime
import pytz
import icalendar
import hashlib

now = datetime.datetime.utcnow()

def parse_html():
   t = html.parse('http://www.siliconprairienews.com/events')
   event_table = t.xpath("//table[@class='events']")[0]

   events = []
   for event_tree in event_table:
      event = {}

      event['title'] = event_tree.xpath('td[@class="event-name"]')[0].text_content().strip()

      time_elem = event_tree.xpath('td[@class="event-date"]/span/span[@class="value-title"]')[0]
      time_str = time_elem.attrib['title']

      # Hack around lack of %z in strptime
      ts = time_str[:-6]
      tz = pytz.timezone('US/Central')
      event['time'] = tz.localize(datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S'))

      event['description'] = html.tostring(event_tree.xpath('td[@class="read-more"]/a')[0]).strip()
      # there's an unclosed span tag on the page, so this xpath looks weird
      try:
         event['location'] = event_tree.xpath('td[@class="location vcard"]/span/span/span')[0].text_content().strip()
      except IndexError:
         event['location'] = 'Unknown location'
      events.append(event)
   return events

def make_calendar(events):
   cal = icalendar.Calendar()

   cal.add('X-WR-CALNAME', 'Silicon Prairie News Events')
   cal.add('X-WR-TIMEZONE', 'America/Chicago')
   cal.add('X-WR-CALDESC', 'The latest events from Silicon Prairie News')
   cal.add('PRODID', '-//gilslotd.com//Silicon Prairie News Calendar v1//EN')
   cal.add('VERSION', '2.0')
   cal.add('CALSCALE', 'GREGORIAN')

   for event in events:
      hashstr = hashlib.sha1(repr(event).encode('UTF-8')).hexdigest()

      ev = icalendar.Event()
      ev.add('DTSTART', event['time'])
      ev.add('DTEND', event['time'])
      ev.add('DTSTAMP', now)
      ev.add('CREATED', now)
      ev.add('UID', '%s@gilslotd.com' % hashstr)
      ev.add('LAST-MODIFIED', now)
      ev.add('STATUS', 'CONFIRMED')
      ev.add('SUMMARY', event['title'])
      ev.add('DESCRIPTION', event['location'] + ' | ' + event['description'])
      ev.add('TRANSP', 'TRANSPARENT')
      ev.add('SEQUENCE', 0)

      cal.add_component(ev)
   return cal

def main():
   try:
      events = parse_html()
      cal = make_calendar(events)
   except:
      import sys
      import traceback
      sys.stderr.write(traceback.format_exc())
      return

   print "Content-Type: text/calendar; charset=UTF-8"
   print
   print cal.to_ical()

if __name__ == "__main__":
   main()
