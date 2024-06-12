


'''
	# from movies_ogv.RSA_fernet_v0.STORE import STORE


	from movies_ogv.RSA_fernet_v0.ENZYME_CREATOR import ENZYME_CREATOR
	OUTPUTS = ENZYME_CREATOR (
		RSA_SIZE = 2048,

		WRITE_OUTPUTS = True,
		OUTPUTS = {
			"RSA_HOT_ENZYME": 	"",
			"RSA_COLD_ENZYME": 	"",
			"FERNET_ENZYME": "	""
		}
	);
'''
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import rsa

def STORE_RSA_COLD_ENZYME (
	PATH,
	RSA_COLD_ENZYME
):
	with open (PATH, 'wb+') as f:
		BINARY_STRING = rsa.PrivateKey.save_pkcs1 (RSA_COLD_ENZYME, format = 'PEM')
		f.write (BINARY_STRING)
		
def STORE_RSA_HOT_ENZYME (
	PATH,
	RSA_HOT_ENZYME
):
	with open (PATH, 'wb+') as f:
		BINARY_STRING = rsa.PublicKey.save_pkcs1 (RSA_HOT_ENZYME, format = 'PEM')
		f.write (BINARY_STRING)
	
	
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


def ENZYME_CREATOR (
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

	#
	#	STEP 2:
	#		FERNET SYM ENZYME CREATOR
	#
	#FERNET_ENZYME = GENERATE_FERNET_ENZYME_O2 ()
	FERNET_ENZYME = GENERATE_FERNET_ENZYME_O1 ()

	if (WRITE_OUTPUTS):
		STORE_RSA_HOT_ENZYME (
			OUTPUTS ["RSA_HOT_ENZYME"],
			RSA_HOT_ENZYME
		)
		
		STORE_RSA_COLD_ENZYME (
			OUTPUTS ["RSA_COLD_ENZYME"],
			RSA_COLD_ENZYME
		)
		
		with open (OUTPUTS ["FERNET_ENZYME"], 'wb') as FP:
			FP.write (FERNET_ENZYME)
	
	return [
		RSA_HOT_ENZYME,
		RSA_COLD_ENZYME,
		
		FERNET_ENZYME
	]