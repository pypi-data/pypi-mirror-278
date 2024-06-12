


"""
"""

import rsa

def RECALL_FERNET_ENZYME (PATH):
	with open (PATH, mode = 'rb') as FP:
		STRING = FP.read ()
		return STRING;
		
	raise Exception (f"??? { PATH }")