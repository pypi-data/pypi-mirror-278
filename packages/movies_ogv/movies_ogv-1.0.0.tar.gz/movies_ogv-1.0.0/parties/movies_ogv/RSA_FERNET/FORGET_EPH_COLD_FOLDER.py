
"""
	wipe -q -Q 3 -r
"""



"""
PM rsa-fernet--forget-eph-cold-folder --cold-folder ""

PM rsa-fernet--forget-eph-cold-folder --cold-folder "" --atp
"""
"""
	DESCRIPTION:
		THE HOT FOLDER HAS A:
		
			HOT ZIP FILE
			HOT FERNET ENZYME (RSA HEATED)
"""

import click

@click.command	("rsa-fernet--forget-eph-cold-folder")
@click.option	('--cold-folder',			required = True)
@click.option	('--atp',			is_flag = True)

# * AMNESIA (FORGET, ..)
def RSA_FERNET__FORGET_EPH_COLD_FOLDER (
	cold_folder,
	atp
):	
	import os, stat
	from os.path import normpath, join, dirname
	CWD = os.getcwd ()

	COLD_FOLDER_LOCATION			= normpath (join (CWD, cold_folder))
	
	
	#------------------------------------------------------------------------
	
	GENOME = f"wipe -f -q -Q 3 -r '{ COLD_FOLDER_LOCATION }'" 
	
	try:
		assert (os.path.exists (COLD_FOLDER_LOCATION))
	except Exception as E:
		print (E)
		print (f"COLD FOLDER NOT FOUND @ '{ COLD_FOLDER_LOCATION }'")
		return;
	
	#------------------------------------------------------------------------

	if (not atp):
		print (GENOME)
		print ()
		print ("INCLUDE '--atp' TO PROCEED WITH THE FORGET.")
		
		return;

	print ()
	print ("wiping:", GENOME)
	print ()
	
	import subprocess
	subprocess.run (GENOME, shell = True, check = True)
	
	
	return;