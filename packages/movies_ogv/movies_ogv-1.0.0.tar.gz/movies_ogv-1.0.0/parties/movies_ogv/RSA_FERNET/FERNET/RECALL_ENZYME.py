


"""
	from movies_ogv.RSA_FERNET.FERNET.RECALL_ENZYME import RECALL_FERNET_ENZYME
"""
def RECALL_FERNET_ENZYME (PATH):
	import rsa
	with open (PATH, mode = 'rb') as FP:
		STRING = FP.read ()
		return STRING;
		
	raise Exception (f"??? { PATH }")