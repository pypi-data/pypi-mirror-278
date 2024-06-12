
'''
	from movies_ogv.RSA_FERNET.MEMORIZE import MEMORIZE

	DATA = MEMORIZE (
		PATH  = ""
	);
'''
def MEMORIZE (
	PATH = ""
):
	with open (PATH, 'rb') as f:
		f.write (DATA)
	
	return;