


"""
	from PYTHON_MIST.RSA_FERNET.RSA.RECALL_ENZYME import RECALL_RSA_ENZYME
	
	RSA_COLD_ENZYME = RECALL_RSA_ENZYME (PATH)
	
	RSA_HOT_ENZYME = RECALL_RSA_ENZYME (PATH)
"""
def RECALL_RSA_ENZYME (PATH):
	import rsa
	with open (PATH, mode = 'rb') as FP:
		STRING = FP.read ()
		return STRING;
		
	raise Exception (f"??? { PATH }")