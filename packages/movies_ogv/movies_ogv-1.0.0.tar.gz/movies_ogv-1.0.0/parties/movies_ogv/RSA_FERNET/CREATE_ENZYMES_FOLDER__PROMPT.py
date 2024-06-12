

"""
	PM rsa-fernet--create-enzymes-folder --folder ""
	
		# --rsa-size

"""

import click
@click.command	("rsa-fernet--create-enzymes-folder")

@click.option	('--folder',		required = True)
@click.option	('--rsa-size',		required = False, default = "2048")
@click.option	('--replace',		is_flag = True)

def RSA_FERNET__CREATE_ENZYMES_FOLDER (
	folder,
	rsa_size,
	replace
):
	print (
		folder,
		rsa_size,
		replace
	)
	
	import os
	CWD = os.getcwd ()
	
	from os.path import normpath, join, dirname
	FOLDER = normpath (join (CWD, folder))
	HOT__RSA____ENZYME 	= normpath (join (CWD, folder, "HOT.2.ENZYME"))
	COLD_RSA____ENZYME 	= normpath (join (CWD, folder, "COLD.2.ENZYME"))
	COLD_FERNET_ENZYME 	= normpath (join (CWD, folder, "COLD.1.ENZYME"))

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
		import shutil
		try:
			shutil.rmtree (FOLDER)
		except Exception as E:
			print ("DEALLOCATION EXCEPTION", E)
			#return;
			
	os.makedirs (FOLDER, exist_ok = True)

	from .ENZYME_CREATOR import ENZYME_CREATOR
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