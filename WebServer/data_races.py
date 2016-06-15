#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
from db_connection import *

db = DatabaseCon('localhost', 'slot', '123123123', 'slot_db')

races = db.get_races()

print "Content-Type: text/html\n\n"
print "<HTML>\n"
print "<HEAD>\n"
print "<META charset='utf-8'>\n"
print "<STYLE>\n"
print "th, td { border-bottom: 1px solid #ddd;}"
print "table { width: 100%;}"

print "tr:hover {background-color: #f2f2f2;}"
print "</STYLE>\n"
print "\t<TITLE>Curses Slot</TITLE>\n"
print "</HEAD>\n"

print "<form name='input' action='data_users.py' method='get'>"
print "<input type='submit' value='Veure classificació' align='right'>"
print "</form>"
    
for race in races:
    laps = db.get_race_laps(str(race[0]))
    user1 = db.get_user_data(str(race[3]))
    user2 = db.get_user_data(str(race[4]))
    circuit = db.get_circuit_from_id(str(race[2]))

    print "<h3>", race[1], " - ", circuit[0][1], "</h3> "#, circuit[0][2]
    print "<TABLE bgcolor='#f2f2f2'><tr><th bgcolor=#00ffff>Username</th>"
    for lap_n in range(len(laps)):
        print "<th bgcolor=#00ffff>", lap_n+1, "</th>"
    print "<th bgcolor=#00ffff>Total</th></tr>"
    
    p1, p2 = 0, 0
    print "<tr><td>",user1[0][1],"</td>"
    for lap in laps:
        print "<td>",lap[3],"</td>"
        p1 += float(lap[3])
    print "<td>", str(p1), "</td></tr>"
    
    print "<tr><td>",user2[0][1],"</td>"
    for lap in laps:
        print "<td>",str(lap[4]),"</td>"
        p2 += float(lap[4])
    print "<td>", str(p2), "</td></tr>"
        
    print "</TABLE>\n"
    print "<hr>"
print "</BODY>\n"
print "</HTML>\n"


db.close_con()
