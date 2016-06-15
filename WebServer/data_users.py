#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
from db_connection import *

db = DatabaseCon('localhost', 'slot', '123123123', 'slot_db')

users = db.get_users_ranking()

print "Content-Type: text/html\n\n"
print "<HTML>\n"
print "<HEAD>\n"
print "<META charset='utf-8'>\n"
print "<STYLE>\n"
print "th, td { border-bottom: 1px solid #ddd;}"
print "table { width: 100%;}"
print "th {background-color: #555555;}"
print "tr:hover {background-color: #f2f2f2;}"
print "</STYLE>\n"
print "\t<TITLE>Curses Slot</TITLE>\n"
print "</HEAD>\n"

print "<form name='input' action='data_users.py' method='get'>"
print "<input type='submit' value='Veure rànguing' align='right'>"
print "</form>"




"""
laps = db.get_race_laps(str(race[0]))
user1 = db.get_user_data(str(race[3]))
user2 = db.get_user_data(str(race[4]))
circuit = db.get_circuit_from_id(str(race[2]))
"""

print "<TABLE th bgcolor='#f002f2'><tr><th bgcolor=#00ffff>Rànquing</th><th>Nom</th><th>Username</th><th>Victòries</th><th>Informació</th></tr>"

print users
ran = 1
for user in users:
    print "<tr><td>", str(ran), " </td>"
    print "<td>", user[1], "</td>"
    print "<td>", user[2], "</td>"
    print "<td>", user[4], "</td>"
    print "<td>", user[3], "</td>"
    ran += 1
    print "</tr>"

print "<hr>"
print "</TABLE>\n"
print "</BODY>\n"
print "</HTML>\n"


db.close_con()
