

"""
	INCOMPLETE TEST
"""



"""
	./CHECKS start --path "RSA_FERNET/4_ONE_FOLDER/test_RSA_FERNET_4.py"
"""

"""

"""

from movies_ogv.RSA_FERNET.ENZYME_CREATOR import ENZYME_CREATOR
from movies_ogv.RSA_FERNET.STORE import STORE
from movies_ogv.RSA_FERNET.HEAT_FOLDER import HEAT_FOLDER

import shutil
from os.path import join, dirname, normpath	
from distutils.dir_util import copy_tree
from shutil import copyfile

def DEALLOCATE (PATH):
	try:
		#os.remove (PATH) 
		shutil.rmtree (PATH)
	except Exception as E:
		print ("DEALLOCATION EXCEPTION", E)
		pass



def check_1 ():
	STEM 						= normpath (join (dirname (__file__), "STEM"))
	CLONE 						= normpath (join (dirname (__file__), "CLONE"))
	DEALLOCATE (CLONE)
	#return;
	
	
	copy_tree (STEM, CLONE)
	
	HOT__RSA_ENZYME 			= normpath (join (CLONE, "ACC/ENZYMES/HOT_RSA.ENZYME"))
	COLD_RSA_ENZYME 			= normpath (join (CLONE, "ACC/ENZYMES/COLD_RSA.ENZYME"))
	COLD_FERNET_ENZYME 			= normpath (join (CLONE, "ACC/ENZYMES/COLD_FERNET.ENZYME"))
	
	ACC			 				= normpath (join (CLONE, "ACC"))
	ACC_COLD 					= normpath (join (CLONE, "ACC/COLD"))
	ACC_EPHEMERAL				= normpath (join (CLONE, "ACC/_EPHEMERAL"))
	COLD_FOLDER_ZIP_LOCATION	= normpath (join (CLONE, "ACC/_EPHEMERAL/ZIP"))
	COLD_EQ_FOLDER_ZIP_LOCATION	= normpath (join (CLONE, "ACC/_EPHEMERAL/ZIP_EQ"))
	COLD_EQ_FOLDER_LOCATION		= normpath (join (CLONE, "ACC/_EPHEMERAL/EQ_FOLDER"))

	HOT_BIOLOGY					= normpath (join (CLONE, "AMYGDALA/HOT"))
	HOT_FERNET_ENZYME		 	= normpath (join (CLONE, "AMYGDALA/HOT.FER.ENZYME"))

	COLD_RSA_ENZYME_DEST 		= normpath (join (CLONE, "ENZYMES/COLD.ASMR.ENZYME"))

	
	
	ENZYME_CREATOR (
		RSA_SIZE = 512,

		WRITE_OUTPUTS = True,
		OUTPUTS = {
			"RSA_HOT_ENZYME":	HOT__RSA_ENZYME,
			"RSA_COLD_ENZYME": 	COLD_RSA_ENZYME,
			"FERNET_ENZYME":	COLD_FERNET_ENZYME
		}
	);
	
	
	
	HEAT_FOLDER (
		EQUALITY_CHECK = True,
		
		INPUTS = {
			"COLD_FOLDER_LOCATION": 		ACC_COLD,
			"COLD_FERNET_ENZYME_LOCATION": 	COLD_FERNET_ENZYME,
			"HOT_RSA_ENZYME_LOCATION": 		HOT__RSA_ENZYME,
			
			#	
			#	EQUALITY CHECK
			#
			"COLD_RSA_ENZYME_LOCATION": 	COLD_RSA_ENZYME
		},
		
		OUTPUTS = {
			"COLD_FOLDER_ZIP_LOCATION": 	COLD_FOLDER_ZIP_LOCATION, # WITHOUT ".zip"
			"HOT_FILE_LOCATION": 			HOT_BIOLOGY,
			"HOT_FERNET_ENZYME_LOCATION": 	HOT_FERNET_ENZYME,

			#	
			#	EQUALITY CHECK
			#
			"COLD_EQ_FOLDER_ZIP_LOCATION": 	COLD_EQ_FOLDER_ZIP_LOCATION, # WITHOUT ".zip"
			"COLD_EQ_FOLDER_LOCATION": 		COLD_EQ_FOLDER_LOCATION
		}
	)
	
	
	copyfile (
		COLD_RSA_ENZYME, 
		COLD_RSA_ENZYME_DEST
	)


	
	
checks = {
	'check 1': check_1
}
