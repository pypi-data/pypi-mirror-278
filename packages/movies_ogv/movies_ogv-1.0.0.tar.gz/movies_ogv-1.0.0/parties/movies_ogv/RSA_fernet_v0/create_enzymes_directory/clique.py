

'''
	import movies_ogv.RSA_fernet_v0.create_enzymes_directory.clique as create_enzymes_directory_clique
	create_enzymes_directory_clique.command ()
'''


"""
	movies_ogv RSA_fernet_v0 create-enzymes-directory --directory "ACC/ENZYMES"
"""

from movies_ogv.RSA_fernet_v0.enzyme_creator import ENZYME_CREATOR
	
import os
import click
from os.path import normpath, join, dirname
import shutil

@click.command	("create-enzymes-directory")
@click.option	('--directory',		required = True)
@click.option	('--rsa-size',		required = False, default = "2048")
@click.option	('--replace',		is_flag = True)
def command (
	directory,
	rsa_size,
	replace
):
	print (
		directory,
		rsa_size,
		replace
	)
	
	CWD = os.getcwd ()
	
	
	FOLDER = normpath (join (CWD, directory))
	HOT__RSA____ENZYME 	= normpath (join (CWD, directory, "HOT.2.ENZYME"))
	COLD_RSA____ENZYME 	= normpath (join (CWD, directory, "COLD.2.ENZYME"))
	COLD_FERNET_ENZYME 	= normpath (join (CWD, directory, "COLD.1.ENZYME"))

	if (not replace):
		try:
			assert (not os.path.exists (HOT__RSA____ENZYME))
			assert (not os.path.exists (COLD_RSA____ENZYME))
			assert (not os.path.exists (COLD_FERNET_ENZYME))
		except Exception as E:
			print (E)
			print ("OUTPUT LOCATIONS WERE NOT EMPTY")
			print ("'--replace' TO REPLACE")
			return;
	else:
		try:
			shutil.rmtree (FOLDER)
		except Exception as E:
			print ("DEALLOCATION EXCEPTION", E)
			#return;
			
	os.makedirs (FOLDER, exist_ok = True)

	
	OUTPUTS = ENZYME_CREATOR (
		RSA_SIZE = int (rsa_size),

		WRITE_OUTPUTS = True,
		OUTPUTS = {
			"RSA_HOT_ENZYME": 	HOT__RSA____ENZYME,
			"RSA_COLD_ENZYME": 	COLD_RSA____ENZYME,
			"FERNET_ENZYME": 	COLD_FERNET_ENZYME
		}
	);
	
	print ()
	print ("-------------------------------------------------")
	print ()
	print ("	~~~~ ENZYMES CREATED ~~~~")
	print ()
	print ("	HOT  RSA  	ENZYME:", HOT__RSA____ENZYME)
	print ("	COLD RSA 	ENZYME:", COLD_RSA____ENZYME)
	print ()
	print ("	COLD FERNET	ENZYME:", COLD_FERNET_ENZYME)
	print ("-------------------------------------------------")
	print ()
	
	return;