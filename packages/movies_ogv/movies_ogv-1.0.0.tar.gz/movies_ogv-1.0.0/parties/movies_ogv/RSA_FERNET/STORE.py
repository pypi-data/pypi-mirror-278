
'''
	from movies_ogv.RSA_FERNET.STORE import STORE

	STORE (
		DATA = "",
		PATH = ""
	);
'''
def STORE (
	DATA = "",
	PATH = ""
):
	with open (PATH, 'wb') as f:
		f.write (DATA)
	
	return;