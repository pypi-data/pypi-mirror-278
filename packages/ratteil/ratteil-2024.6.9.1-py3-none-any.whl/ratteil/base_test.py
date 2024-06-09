"""
RatTeil is a app to live stream the Holly Quran to youtube
Copyright (C) 2024  Ali Elfatih

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import ratteil.base as base
recs = {
   'hazza': {'id': 168, 'name': 'هزاع البلوشي', 'letter': 'ه', 'moshaf': [{'id': 187, 'name': 'حفص عن عاصم - مرتل', 'server': 'http:\\/\\/localhost:8181\\/hazza\\/', 'surah_total': 75, 'moshaf_type': 116, 'surah_list': '1,13,14,15,18,19,25,29,30,31,36,37,38,39,40,42,44,47,49,50,51,52,53,54,55,56,57,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114'}]},
   'shur': {'id': 30, 'name': 'سعود الشريم', 'letter': 'س', 'moshaf': [{'id': 30, 'name': 'حفص عن عاصم - مرتل', 'server': 'http:\\/\\/localhost:8181\\/shur\\/', 'surah_total': 114, 'moshaf_type': 116, 'surah_list': '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114'}]},
   'sds': {'id': 49, 'name': 'عبدالرحمن السديس', 'letter': 'ع', 'moshaf': [{'id': 52, 'name': 'حفص عن عاصم - مرتل', 'server': 'http:\\/\\/localhost:8181\\/sds\\/', 'surah_total': 114, 'moshaf_type': 116, 'surah_list': '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114'}]}
} #for local test



import threading
 
 
def print_cube(num):
    print("Cube: {}" .format(num * num * num))
 
 
def print_square(num):
    print("Square: {}" .format(num * num))
 
 
if __name__ =="__main__":
    t1 = threading.Thread(target=print_square, args=(10,))
    t2 = threading.Thread(target=print_cube, args=(10,))
 
    t1.start()
    t2.start()
 
    t1.join()
    t2.join()
 
    print("Done!")