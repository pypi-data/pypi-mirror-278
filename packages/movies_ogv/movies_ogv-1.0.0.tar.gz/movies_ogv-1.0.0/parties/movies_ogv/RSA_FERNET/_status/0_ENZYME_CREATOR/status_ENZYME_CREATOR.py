
"""	
	python3 status.proc.py "RSA_FERNET/_status/0_ENZYME_CREATOR/status_ENZYME_CREATOR.py"
"""

def DEALLOCATE (PATH):
	import os
	try:
		os.remove (PATH) 
	except Exception as E:
		print ("DEALLOCATION EXCEPTION", E)

def check_1 ():
	from os.path import join, dirname, normpath	
	RSA_HOT_ENZYME = normpath (join (dirname (__file__), "RSA_HOT_ENZYME"))
	RSA_COLD_ENZYME = normpath (join (dirname (__file__), "RSA_COLD_ENZYME"))
	FERNET_ENZYME = normpath (join (dirname (__file__), "FERNET_ENZYME"))
	
	DEALLOCATE (RSA_HOT_ENZYME)
	DEALLOCATE (RSA_COLD_ENZYME)
	DEALLOCATE (FERNET_ENZYME)
	
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

	#assert (OUTPUTS[0])
	print ()
	print (OUTPUTS[0])
	print ()
	print (OUTPUTS[1])
	print ()
	print (OUTPUTS[2])
	print ()
	
	DEALLOCATE (RSA_HOT_ENZYME)
	DEALLOCATE (RSA_COLD_ENZYME)
	DEALLOCATE (FERNET_ENZYME)
	
checks = {
	'check 1': check_1
}