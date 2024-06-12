

"""

"""

"""
PM rsa-fernet--cool-hot-folder \
--hot-folder "AMYGDALA_R/HOT_FOLDER" \
--enzymes "ENZYMES/1" \
--o-cold-folder "AMYGDALA_L/COLD_FOLDER"
	
		# --rsa-size
"""
"""
	DESCRIPTION:
		THE HOT FOLDER HAS A:
		
			HOT ZIP FILE
			HOT FERNET ENZYME (RSA HEATED)
"""

import click
@click.command	("rsa-fernet--cool-hot-folder")

@click.option	('--hot-folder',			required = True)
@click.option	('--enzymes',				required = True)
@click.option	('--o-cold-folder',			required = True)

#@click.option	('--replace',		is_flag = True)

def RSA_FERNET__COOL_HOT_FOLDER (
	hot_folder,
	enzymes,
	o_cold_folder
):	
	
	import os, stat
	from os.path import normpath, join, dirname
	CWD = os.getcwd ()
	
	HOT_FOLDER_LOCATION 			= normpath (join (CWD, hot_folder))
	
	HOT_FERNET_ENZYME_LOCATION		= normpath (join (HOT_FOLDER_LOCATION, "HOT.1.ENZYME"))
	HOT_ZIP_LOCATION				= normpath (join (HOT_FOLDER_LOCATION, "HOT_ZIP_FILE"))
	
	RSA_COLD_ENZYME_LOCATION		= normpath (join (CWD, enzymes, "COLD.2.ENZYME"))
	
	O_COLD_FOLDER_LOCATION			= normpath (join (CWD, o_cold_folder))
	
	#assert (stat.S_ISDIR ().st_mode))
	
	try:
		assert (not os.path.exists (O_COLD_FOLDER_LOCATION))
	except Exception as E:
		print (E)
		print ('"--o-cold-folder" ALREADY EXISTS')
		return;
	
	from .COOL import COOL
	OUTPUTS = COOL (
		BIOLOGY_ENZYME_PATH		= 	HOT_FERNET_ENZYME_LOCATION,
		BIOLOGY_PATH 			= 	HOT_ZIP_LOCATION,
		
		RSA_COLD_ENZYME_PATH	= 	RSA_COLD_ENZYME_LOCATION,
		
		OUTPUT = {
			"BIOLOGY_PATH":			O_COLD_FOLDER_LOCATION + ".zip",
		}
	);
	
	import shutil
	shutil.unpack_archive (
		O_COLD_FOLDER_LOCATION + ".zip",
		O_COLD_FOLDER_LOCATION,
		"zip"
	)
	
	# wipe -f -q -Q 3
	
	
	print ('--------------------------------------------------')
	assert (os.path.exists (O_COLD_FOLDER_LOCATION + '.zip'))
	
	GENOME = f"wipe -f -q -Q 3 '{ O_COLD_FOLDER_LOCATION }.zip'"
	
	print ()
	print ("wiping:", GENOME)
	print ()
	
	import subprocess
	subprocess.run (GENOME, shell = True, check = True)
	print ('--------------------------------------------------')

	return;