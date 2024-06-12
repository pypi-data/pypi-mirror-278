




def add_paths_to_system (paths):
	import pathlib
	from os.path import dirname, join, normpath
	import sys
	
	this_directory = pathlib.Path (__file__).parent.resolve ()	
	for path in paths:
		sys.path.insert (0, normpath (join (this_directory, path)))

add_paths_to_system ([
	'../../parties',
])


import json
import pathlib
from os.path import dirname, join, normpath


this_party_name = "movies_ogv"

this_directory = pathlib.Path (__file__).parent.resolve ()
parties = "/habitat/parties"

this_module = str (normpath (join (
	parties, 
	this_party_name
)))

#status_assurances_path = str (normpath (join (this_directory, "insurance")))
status_assurances_path = str (normpath (join (this_directory, "..")))

import sys
if (len (sys.argv) >= 2):
	glob_string = status_assurances_path + '/' + sys.argv [1]
	db_directory = False
else:
	glob_string = status_assurances_path + '/**/status_*.py'
	db_directory = normpath (join (this_directory, "DB"))

print ("glob string:", glob_string)

import biotech
scan = biotech.start (
	glob_string = glob_string,
	simultaneous = True,
	module_paths = [
		parties
	],
	relative_path = status_assurances_path,
	
	db_directory = db_directory
)
