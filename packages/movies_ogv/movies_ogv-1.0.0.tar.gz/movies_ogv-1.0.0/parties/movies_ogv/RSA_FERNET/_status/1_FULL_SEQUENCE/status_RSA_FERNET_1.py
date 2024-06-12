



"""
	./CHECKS start --path "RSA_FERNET/1_FULL_SEQUENCE/test_RSA_FERNET_1.py"
"""

"""
	ASPIRATIONS:
	
		CREATE ENZYMES
			RSA_HOT_ENZYME
			RSA_COLD_ENZYME
			FERNET_ENZYME
		
		HEAT BIOLOGY WITH ENZYMES
			
"""

def DEALLOCATE (PATH):
	import os

	try:
		os.remove (PATH) 
	except Exception as E:
		print ("DEALLOCATION EXCEPTION", E)

def check_1 ():
	from os.path import join, dirname, normpath	

	#oSOEa = normpath (join (dirname (__file__), "../___STASIS/oSÖEa.flac"))

	RSA_HOT_ENZYME 				= normpath (join (dirname (__file__), "RSA_HOT.ENZYME"))
	RSA_COLD_ENZYME 			= normpath (join (dirname (__file__), "RSA_COLD.ENZYME"))
	FERNET_ENZYME 				= normpath (join (dirname (__file__), "FERNET.ENZYME"))
	
	#BIOLOGY						= normpath (join (dirname (__file__), "../../___STASIS/oSÖEa.flac"))
	BIOLOGY						= normpath (join (dirname (__file__), "../../___STASIS/MUSIC.MP3"))

	MISTIFIED_BIOLOGY 			= normpath (join (dirname (__file__), "MISTIFIED_BIOLOGY"))
	MISTIFIED_BIOLOGY_ENZYME 	= normpath (join (dirname (__file__), "MISTIFIED_BIOLOGY.ENZYME"))
	
	BIOLOGY_2			 		= normpath (join (dirname (__file__), "MUSIC.MP3"))

	DEALLOCATE (RSA_HOT_ENZYME)
	DEALLOCATE (RSA_COLD_ENZYME)
	DEALLOCATE (FERNET_ENZYME)
	DEALLOCATE (MISTIFIED_BIOLOGY)
	DEALLOCATE (MISTIFIED_BIOLOGY_ENZYME)
	
	from movies_ogv.RSA_FERNET.ENZYME_CREATOR import ENZYME_CREATOR
	from movies_ogv.RSA_FERNET.STORE import STORE
	OUTPUTS = ENZYME_CREATOR (
		RSA_SIZE = 512,

		WRITE_OUTPUTS = True,
		OUTPUTS = {
			"RSA_HOT_ENZYME": 	RSA_HOT_ENZYME,
			"RSA_COLD_ENZYME": 	RSA_COLD_ENZYME,
			"FERNET_ENZYME": 	FERNET_ENZYME
		}
	);
	
	import os
	assert (os.path.exists (RSA_HOT_ENZYME))
	assert (os.path.exists (RSA_COLD_ENZYME))
	assert (os.path.exists (FERNET_ENZYME))

	#-----------------------------------------------------------
	
	from movies_ogv.RSA_FERNET.HEAT import HEAT
	OUTPUTS = HEAT (
		FERNET_ENZYME_PATH  = FERNET_ENZYME,
		RSA_HOT_ENZYME_PATH = RSA_HOT_ENZYME,
		
		BIOLOGY_PATH = BIOLOGY,
		
		OUTPUT = {
			"BIOLOGY_PATH": MISTIFIED_BIOLOGY,
			"ENZYME_PATH":  MISTIFIED_BIOLOGY_ENZYME
		}
	);
	
	from movies_ogv.RSA_FERNET.COOL import COOL
	OUTPUTS = COOL (
		BIOLOGY_ENZYME_PATH  	= MISTIFIED_BIOLOGY_ENZYME,
		BIOLOGY_PATH 			= MISTIFIED_BIOLOGY,
		
		RSA_COLD_ENZYME_PATH 	= RSA_COLD_ENZYME,
		
		OUTPUT = {
			"BIOLOGY_PATH": BIOLOGY_2
		}
	);
	
	import filecmp
	EQUAL = filecmp.cmp (
		BIOLOGY, 
		BIOLOGY_2, 
		
		shallow = False
	)
	assert (EQUAL == True)
	
	DEALLOCATE (RSA_HOT_ENZYME)
	DEALLOCATE (RSA_COLD_ENZYME)
	DEALLOCATE (FERNET_ENZYME)
	DEALLOCATE (MISTIFIED_BIOLOGY)
	DEALLOCATE (MISTIFIED_BIOLOGY_ENZYME)
	
	
	
checks = {
	'check 1': check_1
}