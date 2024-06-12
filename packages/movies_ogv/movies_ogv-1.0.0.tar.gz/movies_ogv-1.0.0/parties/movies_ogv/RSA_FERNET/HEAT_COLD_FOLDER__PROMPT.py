

"""
EQUALIZE FROM ONE ACC TO ANOTHER:

PM rsa-fernet--heat-cold-folder \
--cold-folder "ACC/COLD_FOLDER" \
--cold-eph-folder "ACC/COLD_EPH_FOLDER" \
--hot-folder "AMYGDALA/HOT_FOLDER" \
--enzymes "ACC/ENZYMES"
"""

import click
@click.command	("rsa-fernet--heat-cold-folder")

@click.option	('--cold-folder',		required = True)
@click.option	('--cold-eph-folder',	required = True)	# EPHEMERAL
@click.option	('--hot-folder',			required = True)
@click.option	('--enzymes',			required = True)

def RSA_FERNET__HEAT_COLD_FOLDER (
	cold_folder,
	cold_eph_folder,
	hot_folder,
	enzymes
):
	import os
	from os.path import normpath, join, dirname
	HERE = CWD = os.getcwd ()
	
	COLD_FOLDER_LOCATION 			= normpath (join (HERE, cold_folder))
	COLD_EPH_FOLDER_LOCATION 		= normpath (join (HERE, cold_eph_folder))
	HOT_FOLDER_LOCATION				= normpath (join (HERE, hot_folder))	
	ENZYMES_LOCATION				= normpath (join (HERE, enzymes))
	
	COLD_FERNET_ENZYME_LOCATION 	= normpath (join (ENZYMES_LOCATION, "COLD.1.ENZYME"))
	COLD_RSA_ENZYME_LOCATION		= normpath (join (ENZYMES_LOCATION, "COLD.2.ENZYME"))
	HOT_RSA_ENZYME_LOCATION 		= normpath (join (ENZYMES_LOCATION, "HOT.2.ENZYME"))
	
	#---------------------------------------------------------------------------
	
	COLD_FOLDER_ZIP_LOCATION		= normpath (join (COLD_EPH_FOLDER_LOCATION, "COLD_ZIP_FOLDER"))

	HOT_ZIP_FILE_LOCATION			= normpath (join (HOT_FOLDER_LOCATION, "HOT_ZIP_FILE"))	
	HOT_FERNET_ENZYME_LOCATION		= normpath (join (HOT_FOLDER_LOCATION, "HOT.1.ENZYME"))	

	#---------------------------------------------------------------------------
	
	COLD_EQ_FOLDER_ZIP_LOCATION		= normpath (join (COLD_EPH_FOLDER_LOCATION, "COLD_EQ_ZIP_FOLDER"))
	COLD_EQ_FOLDER					= normpath (join (COLD_EPH_FOLDER_LOCATION, "COLD_EQ_FOLDER"))

	#---------------------------------------------------------------------------

	os.makedirs (COLD_FOLDER_ZIP_LOCATION, exist_ok = True)
	
	import shutil
	try:
		shutil.rmtree (COLD_EPH_FOLDER_LOCATION)
	except Exception as E:
		print ("DEALLOCATION EXCEPTION", E)
		#return;
		
	import shutil
	try:
		shutil.rmtree (HOT_FOLDER_LOCATION)
	except Exception as E:
		print ("DEALLOCATION EXCEPTION", E)
		#return;
			
	#---------------------------------------------------------------------------

	INPUTS = {
		"COLD_FOLDER_LOCATION": 		COLD_FOLDER_LOCATION,
		"COLD_FERNET_ENZYME_LOCATION": 	COLD_FERNET_ENZYME_LOCATION,
		"HOT_RSA_ENZYME_LOCATION": 		HOT_RSA_ENZYME_LOCATION,
		
		#	
		#	EQUALITY CHECK
		#
		"COLD_RSA_ENZYME_LOCATION": 	COLD_RSA_ENZYME_LOCATION
	}
	
	OUTPUTS = {
		"COLD_FOLDER_ZIP_LOCATION": 	COLD_FOLDER_ZIP_LOCATION, # WITHOUT ".zip"
		"HOT_FILE_LOCATION": 			HOT_ZIP_FILE_LOCATION,
		"HOT_FERNET_ENZYME_LOCATION": 	HOT_FERNET_ENZYME_LOCATION,
		
		#	
		#	EQUALITY CHECK
		#
		"COLD_EQ_FOLDER_ZIP_LOCATION": 	COLD_EQ_FOLDER_ZIP_LOCATION, # WITHOUT ".zip"
		"COLD_EQ_FOLDER_LOCATION":		COLD_EQ_FOLDER # WITHOUT ".zip"
	}

	import json
	print ("INPUTS:", json.dumps (INPUTS, indent = 2))
	print ("OUTPUTS:", json.dumps (OUTPUTS, indent = 2))
	
	from .HEAT_FOLDER import HEAT_FOLDER
	HEAT_FOLDER (
		EQUALITY_CHECK = True,
		INPUTS = INPUTS,
		OUTPUTS = OUTPUTS
	)
	
	import shutil
	shutil.rmtree (COLD_EPH_FOLDER_LOCATION)

	return;
