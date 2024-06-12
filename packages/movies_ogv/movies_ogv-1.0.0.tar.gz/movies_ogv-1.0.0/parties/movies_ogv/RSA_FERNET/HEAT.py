
'''
	from movies_ogv.RSA_FERNET.HEAT import HEAT

	OUTPUTS = HEAT (
		
		#
		#	COLD FERNET ENZYME (NOT HEATED BY THE "HOT RSA ENZYME")
		#
		FERNET_ENZYME_PATH  = "",
		
		RSA_HOT_ENZYME_PATH = "",
		
		OUTPUT = {
			"BIOLOGY_PATH": "",
			
			#
			#	
			#
			"ENZYME_PATH":  ""
		}
	);
'''

"""
	WITH [ FERNET, RSA HOT ] ENZYMES,
	
		A MISTIFIED "BIOLOGY" & "ENZYME" ARE CREATED
"""

from .RSA.RECALL_ENZYME 		import RECALL_RSA_ENZYME
from .FERNET.RECALL_ENZYME 	import RECALL_FERNET_ENZYME

def READ_BINARY (PATH):
	with open (PATH, mode = 'rb') as FP:
		STRING = FP.read ()
		return STRING;
		
	raise Exception (f"??? { PATH }")
	
def READ (PATH):
	with open (PATH, mode = 'r') as FP:
		STRING = FP.read ()
		return STRING;
		
	raise Exception (f"??? { PATH }")

def WRITE (PATH, DATA):
	import os
	from os.path import dirname
	os.makedirs (dirname (PATH), exist_ok = True)
	
	f = open	(PATH, "wb")
	f.write		(DATA)
	f.close		()

def HEAT (
	FERNET_ENZYME_PATH,
	RSA_HOT_ENZYME_PATH,
	
	BIOLOGY_PATH,
	
	OUTPUT,
	
	# [ 0, 1, 2 ]
	RECORDS = 1
):
	import rsa
	from cryptography.fernet import Fernet
	from base64 import b64encode, b64decode
	
	FERNET_ENZYME 	= READ_BINARY (FERNET_ENZYME_PATH)
	RSA_HOT_ENZYME	= rsa.PublicKey.load_pkcs1 (READ (RSA_HOT_ENZYME_PATH))
	BIOLOGY			= READ_BINARY (BIOLOGY_PATH)
	
	FERNET_ORGANIMS = Fernet (FERNET_ENZYME)
	
	BIOLOGY__UTF8__FERNET 	= FERNET_ORGANIMS.encrypt (BIOLOGY)
	BIOLOGY__FERNET__B64 	= b64encode (BIOLOGY__UTF8__FERNET)
	
	if (RECORDS >= 2):
		print ()
		print ("FERNET_ENZYME:", FERNET_ENZYME)
		print ("RSA_HOT_ENZYME:", RSA_HOT_ENZYME)
		print ()
	
	FERNET_ENZYME__RSA_HOT = rsa.encrypt (
		FERNET_ENZYME, 
		RSA_HOT_ENZYME
	)
	
	FERNET_ENZYME__RSA_HOT__B64 = b64encode (
		FERNET_ENZYME__RSA_HOT
	)
	
	WRITE (OUTPUT["BIOLOGY_PATH"], 	BIOLOGY__FERNET__B64);
	WRITE (OUTPUT["ENZYME_PATH"], 	FERNET_ENZYME__RSA_HOT__B64);
	
	return;
	
	"""
	return { 
		'ENZYME':		FERNET_ENZYME__RSA_HOT__B64, 
		'BIOLOGY':		BIOLOGY__FERNET__B64 
	}
	"""
	
	
	
	
	