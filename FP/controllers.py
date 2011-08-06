#!/usr/bin/python
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
import csv
from FeedPaper.FP.models import feedDB

# This function Parses and adds the CSV file to the feedDB
def parseCSV(file , ignore_first_line = True):
    """
    # This function Parses and adds the CSV file to the feedDB
    """
    reader = csv.reader(file)
    for row in reader:
        if ignore_first_line :
            ignore_first_line = False
            continue
        feedDB(
               keyword = row[0],
               url = row[1],
               ).save()