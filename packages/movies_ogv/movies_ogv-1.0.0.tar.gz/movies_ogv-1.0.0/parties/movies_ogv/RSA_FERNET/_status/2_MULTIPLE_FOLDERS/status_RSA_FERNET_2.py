





"""
	./CHECKS start --path "RSA_FERNET/2_MULTIPLE_FOLDERS/test_RSA_FERNET_2.py"
"""

"""
	ASPIRATIONS:
	
		ACC:
			CREATE RSA ENZYMES
				RSA_HOT_ENZYME
				RSA_COLD_ENZYME
				
			
			FOR EACH * BIOLOGY (CONNECTIVE TISSUE, FOLDER) IN ACC:
				
				#
				#	/ACC					
				#		# [REPLICA SET 1 (x6)] THE LOCATION OF OPEN BIOLOGIES
				#			# KEEP IN MULTIPLE STORAGE LOCATIONS
				#
				#
				#		/_CONNECTIVE_TEMPORARY
				#			/1
				#				/FERNET_ENZYME
				#				/BIOLOGY.zip
				#
				#
				#		/CONNECTIVE
				#			/1
				#
				#
				#
				#		/_EPITHELIAL_TEMPORARY
				#
				#
				#		/EPITHELIAL		(FILES THAT CAN BE DEMISTIFIED IN RAM)
				#
				#
				#		/ENZYMES
				#			RSA_COLD.ENZYME (RSA PRIVATE KEY (DECRYRTER))
				#			RSA_HOT.ENZYME  (RSA PUBLIC  KEY (ENCRYPTER))
				#
				#
				#	/AMYGDALA 				
				# 		# [REPLICA SET (x2)] THE LOCATION OF MISTIFIED BIOLOGIES
				#
				#		/EPITHELIAL
				#			# THESE CAN BE DEMISTIFIED IN RAM
				#			
				#		/CONNECTIVE
				#			
				#
				#
				#	/CORNU_AMMONIS
				#		# [REPLICA SET (x4)] THE NEW UNMISTIFIED BIOLOGIES
				#		# 	THESE ARE COPIED TO THE ACC
				#		#		
				#		#		!!!!!!!!!!!!! [[[[[ NO OVERWRITING ]]]] !!!!!!!!!!!!!
				#		#
				#		#		IF SAME LABEL -> NEED TO UPDATE THE LABEL OF THE
				#		#		OF THE CORNU_AMMONIS BIOLOGIES
				#	
				#
				#		/BIOLOGIES
				#			
				#
				#
				#
				#	/ENZYMES				
				#	 	# [REPLICA SET (x2)] THE LOCATION OF THE DEMISTIFIACTION ENZYME
				#
				#		/BIOLOGIES
				#			/1
				#				"ENZYME" 			~ (RSA OF FERNET ENZYME)
				#				"ZIP.SHA" 			~ SHA OF (COMPRESSED) ZIP ARCHIVE
				#				"BIOLOGY.HOT"		~ ENCRYPTED VERSION OF THE BIOLOGY
				#

				
				~ CREATE FERNET_ENZYME
				
				~ ZIP THE FOLDER WITH SUBPROCESS INTO ACC/_TEMPORARY
				
				~ 
		
		HEAT BIOLOGY WITH ENZYMES
		
		
		###########################################################
		
			[ ] INDEX????
			
"""

def DEALLOCATE (PATH):
	import os

	try:
		os.remove (PATH) 
	except Exception as E:
		#print ("DEALLOCATION EXCEPTION", E)
		pass

def check_1 ():
	from os.path import join, dirname, normpath	

	RSA_HOT_ENZYME 				= normpath (join (dirname (__file__), "ACC/ENZYMES/RSA_HOT.ENZYME"))
	RSA_COLD_ENZYME 			= normpath (join (dirname (__file__), "ACC/ENZYMES/RSA_COLD.ENZYME"))

	ACC			 				= normpath (join (dirname (__file__), "ACC"))
	ACC_BIOLOGIES 				= normpath (join (dirname (__file__), "ACC/BIOLOGIES"))
	ACC_TEMPORARY 				= normpath (join (dirname (__file__), "ACC/_TEMPORARY"))

	MISTIFIED_BIOLOGY 			= normpath (join (dirname (__file__), "BIOLOGY.HOT"))
	MISTIFIED_BIOLOGY_ENZYME 	= normpath (join (dirname (__file__), "BIOLOGY.HOT.ENZYME"))
	
	AMYGDALA_BIOLOGIES			= normpath (join (dirname (__file__), "AMYGDALA/BIOLOGIES"))
	
	CORNU_AMMONIS				= normpath (join (dirname (__file__), "CORNU_AMMONIS"))
	
	CORTISOL					= normpath (join (dirname (__file__), "CORTISOL"))

	BIOLOGY_2			 		= normpath (join (dirname (__file__), "MUSIC.MP3"))

	DEALLOCATE (ACC_TEMPORARY)
	
	#DEALLOCATE (RSA_HOT_ENZYME)
	#DEALLOCATE (RSA_COLD_ENZYME)
	#DEALLOCATE (FERNET_ENZYME)
	#DEALLOCATE (MISTIFIED_BIOLOGY)
	#DEALLOCATE (MISTIFIED_BIOLOGY_ENZYME)

	from movies_ogv.RSA_FERNET.RSA.ENZYME_CREATOR import CREATE_RSA_ENZYME
	OUTPUTS = CREATE_RSA_ENZYME (
		RSA_SIZE = 512,

		WRITE_OUTPUTS = True,
		OUTPUTS = {
			"RSA_HOT_ENZYME": 	RSA_HOT_ENZYME,
			"RSA_COLD_ENZYME": 	RSA_COLD_ENZYME
		}
	);
	
	import os
	assert (os.path.exists (RSA_HOT_ENZYME))
	assert (os.path.exists (RSA_COLD_ENZYME))
	
	import os
	BIOLOGIES = os.listdir (path = ACC_BIOLOGIES)
	for BIOLOGY in BIOLOGIES:
		FULL_PATH = normpath (join (ACC_BIOLOGIES, BIOLOGY))
		ZIP_LOCATION = normpath (join (ACC, '_TEMPORARY', BIOLOGY, "BIOLOGY"))

		print ("BIOLOGY:", FULL_PATH)
		
		import stat, os
		IS_DIR = stat.S_ISDIR (os.stat (FULL_PATH).st_mode)
		
		if (IS_DIR != True):
			print ("FOUND A NON_DIRECTORY", FULL_PATH)
			continue;
		
		#
		#	FERNET ENZYME CREATION
		#
		FERNET_ENZYME_LOCATION = normpath (join (dirname (__file__), "ACC/_TEMPORARY", BIOLOGY, "FERNET_ENZYME"))
		#		
		from movies_ogv.RSA_FERNET.FERNET.ENZYME_CREATOR import FERNET_ENZYME_CREATOR
		OUTPUTS = FERNET_ENZYME_CREATOR (
			WRITE_OUTPUTS = True,
			OUTPUTS = {
				"FERNET_ENZYME": FERNET_ENZYME_LOCATION
			}
		);
		
		import os
		assert (os.path.exists (FERNET_ENZYME_LOCATION))
		
		#
		#	ZIP OF BIOLOGY
		#
		#from RSA_FERNET.CONCEPT import CREATE as CREATE_CONCEPT
		#CREATE_CONCEPT ("zip")
		
		import shutil
		shutil.make_archive (ZIP_LOCATION, "zip", FULL_PATH)
		
		
		#------------------------------------------------------------------------------
		#------------------------------------------------------------------------------
		
		#
		#	MISTIFY THE BIOLOGY
		#
		HOT_BIOLOGY			= normpath (join (ACC, '_TEMPORARY', BIOLOGY, "HOT/BIOLOGY.HOT"))
		HOT_BIOLOGY_ENZYME  = normpath (join (ACC, '_TEMPORARY', BIOLOGY, "HOT/BIOLOGY.HOT.ENZYME"))		
		#
		from movies_ogv.RSA_FERNET.HEAT import HEAT
		OUTPUTS = HEAT (
			FERNET_ENZYME_PATH  = FERNET_ENZYME_LOCATION,
			RSA_HOT_ENZYME_PATH = RSA_HOT_ENZYME,
			
			BIOLOGY_PATH = ZIP_LOCATION + ".zip",
			
			OUTPUT = {
				"BIOLOGY_PATH": HOT_BIOLOGY,
				"ENZYME_PATH":  HOT_BIOLOGY_ENZYME
			}
		);
		
		#------------------------------------------------------------------------------
		#------------------------------------------------------------------------------
		
		#
		#	DEMISTIFY THE BIOLOGY	-> 	ZIP
		#
		COLD_2_ZIP_LOCATION = normpath (join (ACC, '_TEMPORARY', BIOLOGY, "COLD_2/BIOLOGY.zip"))
		from movies_ogv.RSA_FERNET.COOL import COOL
		OUTPUTS = COOL (
			BIOLOGY_ENZYME_PATH  	= HOT_BIOLOGY_ENZYME,
			BIOLOGY_PATH 			= HOT_BIOLOGY,
			
			RSA_COLD_ENZYME_PATH 	= RSA_COLD_ENZYME,
			
			OUTPUT = {
				"BIOLOGY_PATH": COLD_2_ZIP_LOCATION
			}
		);
		
		
		COLD_2_EXTRACTION_LOCATION = normpath (join (ACC, '_TEMPORARY', BIOLOGY, "COLD_2/BIOLOGY"))
		
		import shutil
		shutil.unpack_archive (COLD_2_ZIP_LOCATION, COLD_2_EXTRACTION_LOCATION)
		
		
		#
		#	CHECK THAT THE DEMISTIFIED BIOLOGY == THE ORIGINAL BIOLOGY
		#
		import ships.paths.directory.check_equality as check_equality
		report = check_equality.start (
			FULL_PATH,
			COLD_2_EXTRACTION_LOCATION
		)	
		assert (
			report ==
			{'1': {}, '2': {}}
		)
		
		'''
		from WOMA_BIOLOGY.TISSUES.CONNECTIVE.EQUALITY import EQUALITY
		IS_EQUAL = EQUALITY (
			FULL_PATH,
			COLD_2_EXTRACTION_LOCATION,
			
			ENUMERATE_UNIQUE_DIRECTORIES = False
		);
		assert (IS_EQUAL == True)
		print (IS_EQUAL)
		'''
		
		import os
		from os.path import dirname
		os.makedirs (
			normpath (
				join (
					AMYGDALA_BIOLOGIES, 
					BIOLOGY
				)
			), 
			exist_ok = True
		)
		from shutil import copyfile
		copyfile (
			HOT_BIOLOGY, 
			normpath (join (
				AMYGDALA_BIOLOGIES, 
				BIOLOGY, 
				"BIOLOGY.HOT"
			))
		)
		copyfile (
			HOT_BIOLOGY_ENZYME, 
			normpath (join (
				AMYGDALA_BIOLOGIES, 
				BIOLOGY, 
				"BIOLOGY.HOT.ENZYME"
			))
		)
		
		
		CORTISOL_COLD_ENZYME = normpath (join (
			CORTISOL, 
			"ENZYMES", 
			"COLD_ENZYME"
		))
		import os
		from os.path import dirname
		os.makedirs (dirname (CORTISOL_COLD_ENZYME), exist_ok = True)
		copyfile (
			RSA_COLD_ENZYME, 
			CORTISOL_COLD_ENZYME
		)
		
		
		
		
		
	return;


checks = {
	'check 1': check_1
}