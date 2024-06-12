





"""
	from movies_ogv.RSA_FERNET.HEAT_FOLDER import HEAT_FOLDER

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
			"COLD_FOLDER_ZIP_LOCATION": 	COLD_FOLDER_ZIP_LOCATION, 
				# WITHOUT ".zip"
				# [EPHEMERAL]
			
			"HOT_FILE_LOCATION": 			HOT_BIOLOGY,
			"HOT_FERNET_ENZYME_LOCATION": 	HOT_FERNET_ENZYME,
			
			#	
			#	EQUALITY CHECK
			#
			"COLD_EQ_FOLDER_ZIP_LOCATION": 	ZIP_EQ, # WITHOUT ".zip"
				# [EPHEMERAL]
				
			"COLD_EQ_FOLDER_LOCATION":		, # WITHOUT ".zip"
				# [EPHEMERAL]
		}
	)
"""

def DEALLOCATE (PATH):
	import shutil

	try:
		shutil.rmtree (PATH)
	except Exception as E:
		print ("DEALLOCATION EXCEPTION", E)
		pass

def HEAT_FOLDER (
	#
	#	POSSIBILITIES: "ABANDON" or False
	#
	#	ASPIRATIONS: "SHRED"???
	#	
	FORGET	 		= "ABANDON",
	EQUALITY_CHECK 	= True,
	RECORDS 		= 1,
	
	INPUTS 			= {},
	OUTPUTS 		= {}
):
	import stat, os
	assert (stat.S_ISDIR (os.stat (INPUTS ["COLD_FOLDER_LOCATION"]).st_mode))
	assert (stat.S_ISREG (os.stat (INPUTS ["COLD_FERNET_ENZYME_LOCATION"]).st_mode))
	assert (stat.S_ISREG (os.stat (INPUTS ["HOT_RSA_ENZYME_LOCATION"]).st_mode))

	assert (not os.path.exists (OUTPUTS ["COLD_FOLDER_ZIP_LOCATION"]))
	assert (not os.path.exists (OUTPUTS ["HOT_FILE_LOCATION"]))
	assert (not os.path.exists (OUTPUTS ["HOT_FERNET_ENZYME_LOCATION"]))

	
	if (EQUALITY_CHECK):
		assert (stat.S_ISREG (os.stat (INPUTS ["COLD_RSA_ENZYME_LOCATION"]).st_mode))
		assert (not os.path.exists (OUTPUTS ["COLD_EQ_FOLDER_ZIP_LOCATION"]))
		
		
	import shutil
	shutil.make_archive (
		OUTPUTS ["COLD_FOLDER_ZIP_LOCATION"], 
		"zip", 
		INPUTS ["COLD_FOLDER_LOCATION"]
	)
	
	COLD_FOLDER_ZIP_LOCATION = OUTPUTS ["COLD_FOLDER_ZIP_LOCATION"] + ".zip"

	from .HEAT import HEAT
	HEAT_OUTPUT = HEAT (
		FERNET_ENZYME_PATH	=	INPUTS ["COLD_FERNET_ENZYME_LOCATION"],
		RSA_HOT_ENZYME_PATH	=	INPUTS ["HOT_RSA_ENZYME_LOCATION"],
		
		BIOLOGY_PATH 		=	COLD_FOLDER_ZIP_LOCATION,
		
		OUTPUT = {
			"BIOLOGY_PATH":		OUTPUTS ["HOT_FILE_LOCATION"],
			"ENZYME_PATH":		OUTPUTS ["HOT_FERNET_ENZYME_LOCATION"]
		}
	);

	if (RECORDS >= 1):
		print ("CREATED:", OUTPUTS ["HOT_FILE_LOCATION"])
		print ("CREATED:", OUTPUTS ["HOT_FERNET_ENZYME_LOCATION"])


	if (EQUALITY_CHECK):
		#___________________________________________________________________________
		#---------------------------------------------------------------------------
		#
		#	EQUALITY CHECK
		#	
		
		#
		#	HOT -> COLD ZIP
		#
		from .COOL import COOL
		COOL_OUTPUT = COOL (
			BIOLOGY_ENZYME_PATH  	=	OUTPUTS ["HOT_FERNET_ENZYME_LOCATION"],
			BIOLOGY_PATH 			=	OUTPUTS ["HOT_FILE_LOCATION"],
			
			RSA_COLD_ENZYME_PATH 	=	INPUTS ["COLD_RSA_ENZYME_LOCATION"],
			
			OUTPUT = {
				"BIOLOGY_PATH": 		OUTPUTS ["COLD_EQ_FOLDER_ZIP_LOCATION"]
			}
		);
		
		#
		#	EQ COLD ZIP -> EQ COLD
		#
		import shutil
		shutil.unpack_archive (
			OUTPUTS ["COLD_EQ_FOLDER_ZIP_LOCATION"], 
			OUTPUTS ["COLD_EQ_FOLDER_LOCATION"],
			"zip"
		)
		
		#
		#	EQ COLD == (ORIGINAL) COLD
		#
		import ships.paths.directory.check_equality as check_equality
		report = check_equality.start (
			INPUTS ["COLD_FOLDER_LOCATION"],
			OUTPUTS ["COLD_EQ_FOLDER_LOCATION"]
		)	
		assert (
			report ==
			{'1': {}, '2': {}}
		)
		
		os.remove (OUTPUTS ["COLD_EQ_FOLDER_ZIP_LOCATION"])
		
		import shutil
		shutil.rmtree (OUTPUTS ["COLD_EQ_FOLDER_LOCATION"])

		#
		#	END OF EQUALITY CHECK
		#	
		#___________________________________________________________________________
		#---------------------------------------------------------------------------
	
		
	
	os.remove (COLD_FOLDER_ZIP_LOCATION)

	return;
	
	
	
	
	
	