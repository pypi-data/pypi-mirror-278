

'''
	from PYTHON_MIST.RSA_FERNET.COOL import COOL

	OUTPUTS = COOL (
		BIOLOGY_ENZYME_PATH  = "",
		BIOLOGY_PATH = "",
		
		RSA_COLD_ENZYME_PATH = "",
		
		OUTPUT = {
			"BIOLOGY_PATH": "",
		}
	);
'''
import rsa
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode


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
	
	with open (PATH, mode = 'wb') as FP:
		STRING = FP.write (DATA)
		return STRING;
		
	raise Exception (f"??? { PATH }")
	
def COOL (
	BIOLOGY_ENZYME_PATH = "",
	BIOLOGY_PATH = "",
	
	RSA_COLD_ENZYME_PATH = "",
	
	WRITE_OUTPUT = True,
	OUTPUT = {}
):
	enc_symmetricKey 	= b64decode (READ_BINARY (BIOLOGY_ENZYME_PATH))
	enc_data 			= b64decode (READ_BINARY (BIOLOGY_PATH))
	
	privateKey			= rsa.PrivateKey.load_pkcs1 (READ_BINARY (RSA_COLD_ENZYME_PATH))
	
	symmetricKey 		= rsa.decrypt (enc_symmetricKey, privateKey)

	f = Fernet (symmetricKey)
	data = f.decrypt (enc_data)

	if (WRITE_OUTPUT):
		WRITE (OUTPUT ["BIOLOGY_PATH"], data)
	
	return data