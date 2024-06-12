




'''
	from PYTHON_MIST.RSA_FERNET.FERNET.ENZYME_CREATOR import FERNET_ENZYME_CREATOR

	OUTPUTS = FERNET_ENZYME_CREATOR (
		WRITE_OUTPUTS = True,
		OUTPUTS = {
			"FERNET_ENZYME": "	""
		}
	);
'''
import rsa
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def GENERATE_FERNET_ENZYME_O1 ():
	

	password			= 	"password".encode ()

	#
	#	BETTER IS key from os.urandom (16) ????
	#
	salt				= 	b'salt_'

	kdf = PBKDF2HMAC (
		algorithm		=	hashes.SHA256 (),
		length			=	32,
		salt			=	salt,
		iterations		=	100000,
		backend			=	default_backend ()
	)

	key = base64.urlsafe_b64encode (kdf.derive (password)) 
	
	return key;
	
# OPTION 2
def GENERATE_FERNET_ENZYME_O2 (): 
	from cryptography.fernet import Fernet

	FERNET_ENZYME = Fernet.generate_key ()

	return FERNET_ENZYME


def FERNET_ENZYME_CREATOR (
	WRITE_OUTPUTS = False,
	OUTPUTS = {}
):
	from cryptography.fernet import Fernet
	from base64 import b64encode, b64decode

	#
	#	STEP 2:
	#		FERNET SYM ENZYME CREATOR
	#
	#FERNET_ENZYME = GENERATE_FERNET_ENZYME_O2 ()
	FERNET_ENZYME = GENERATE_FERNET_ENZYME_O1 ()

	if (WRITE_OUTPUTS):
		import os
		from os.path import dirname
		
		
		os.makedirs (dirname (OUTPUTS ["FERNET_ENZYME"]), exist_ok = True)
		
		
		with open (OUTPUTS ["FERNET_ENZYME"], 'wb') as FP:
			FP.write (FERNET_ENZYME)
	
	return [
		FERNET_ENZYME
	]