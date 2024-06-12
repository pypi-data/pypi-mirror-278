





"""
	movies_ogv RSA_fernet_v0 clone-enzymes --de "ACC/ENZYMES" --to "ENZYMES/1"
"""

import click
@click.command	("clone-enzymes")
@click.option	('--de',		required = True)
@click.option	('--to',		required = False, default = "2048")
@click.option	('--replace',	is_flag = True)

def command (
	de,
	to,
	replace
):
	print (
		de,
		to
	)
	
	import os
	CWD = os.getcwd ()
	
	from os.path import normpath, join, dirname
	DE 	= normpath (join (CWD, de))
	DE_COLD_1 	= normpath (join (DE, "COLD.1.ENZYME"))
	DE_COLD_2 	= normpath (join (DE, "COLD.2.ENZYME"))
	DE_HOT_2 	= normpath (join (DE, "HOT.2.ENZYME"))

	TO 			= normpath (join (CWD, to))
	TO_COLD_1 	= normpath (join (TO, "COLD.1.ENZYME"))
	TO_COLD_2 	= normpath (join (TO, "COLD.2.ENZYME"))
	TO_HOT_2 	= normpath (join (TO, "HOT.2.ENZYME"))

	if (not replace):
		try:
			assert (not os.path.exists (TO))
		except Exception as E:
			print (E)
			print ("OUTPUT LOCATIONS WERE NOT EMPTY")
			print ("'--replace' TO REPLACE")
			return;
	else:
		import shutil
		try:
			shutil.rmtree (TO)
		except Exception as E:
			print ("DEALLOCATION EXCEPTION", E)
			#return;
			
	os.makedirs (TO, exist_ok = True)

	import shutil
	shutil.copytree (DE, TO, dirs_exist_ok = True)
	
	print ()
	print ("-------------------------------------------------")
	print ()
	print ("	~~~~ ENZYMES CLONED ~~~~")
	print ()
	print ("	COLD 1	 	ENZYME:", TO_COLD_1)
	print ("	COLD 2		ENZYME:", TO_COLD_2)
	print ("	HOT 2		ENZYME:", TO_HOT_2)
	print ()
	print ("-------------------------------------------------")
	print ()
	
	assert (os.path.exists (TO_COLD_1))
	assert (os.path.exists (TO_COLD_2))
	assert (os.path.exists (TO_HOT_2))
	
	return;