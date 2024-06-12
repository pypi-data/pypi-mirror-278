

'''
	from PYTHON_MIST.RSA_FERNET.RSA.ENZYME_CREATOR import CREATE_RSA_ENZYME

	OUTPUTS = CREATE_RSA_ENZYME (
		RSA_SIZE = 2048,

		WRITE_OUTPUTS = True,
		OUTPUTS = {
			"RSA_HOT_ENZYME": 	"",
			"RSA_COLD_ENZYME": 	""
		}
	);
'''
import rsa

def STORE_RSA_COLD_ENZYME (
	PATH,
	RSA_COLD_ENZYME
):
	import os
	from os.path import dirname
	os.makedirs (dirname (PATH), exist_ok = True)

	with open (PATH, 'wb+') as f:
		BINARY_STRING = rsa.PrivateKey.save_pkcs1 (RSA_COLD_ENZYME, format = 'PEM')
		f.write (BINARY_STRING)
		
def STORE_RSA_HOT_ENZYME (
	PATH,
	RSA_HOT_ENZYME
):
	import os
	from os.path import dirname
	os.makedirs (dirname (PATH), exist_ok = True)

	with open (PATH, 'wb+') as f:
		BINARY_STRING = rsa.PublicKey.save_pkcs1 (RSA_HOT_ENZYME, format = 'PEM')
		f.write (BINARY_STRING)

def CREATE_RSA_ENZYME (
	RSA_SIZE = 2048,
	WRITE_OUTPUTS = False,
	OUTPUTS = {}
):
	from cryptography.fernet import Fernet
	from base64 import b64encode, b64decode

	#
	#	STEP 1:
	#		RSA ASYM ENZYME CREATOR
	# 
	RSA_HOT_ENZYME, RSA_COLD_ENZYME = rsa.newkeys (RSA_SIZE)
	
	if (WRITE_OUTPUTS):
		STORE_RSA_HOT_ENZYME (
			OUTPUTS ["RSA_HOT_ENZYME"],
			RSA_HOT_ENZYME
		)
		
		STORE_RSA_COLD_ENZYME (
			OUTPUTS ["RSA_COLD_ENZYME"],
			RSA_COLD_ENZYME
		)

	return [
		RSA_HOT_ENZYME,
		RSA_COLD_ENZYME
	]
	

