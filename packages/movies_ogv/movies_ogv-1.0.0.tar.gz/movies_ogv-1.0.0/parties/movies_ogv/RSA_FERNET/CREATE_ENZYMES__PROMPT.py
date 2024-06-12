

"""
	EQUALIZE FROM ONE ACC TO ANOTHER:
	
PM rsa-fernet--create-enzymes \
--o-rsa-hot-enzyme "HOT.2.ENZYME" \
--o-rsa-cold-enzyme "COLD.2.ENZYME" \
--o-fernet-cold-enzyme "COLD.1.ENZYME"
"""

import click
@click.command	("rsa-fernet--create-enzymes")

@click.option	('--o-rsa-hot-enzyme',		required = True)
@click.option	('--o-rsa-cold-enzyme',		required = True)
@click.option	('--o-fernet-cold-enzyme',	required = True)

@click.option	('--rsa-size',				required = False, default = "2048")

def RSA_FERNET__CREATE_ENZYMES (
	o_rsa_hot_enzyme, 
	o_rsa_cold_enzyme,
	o_fernet_cold_enzyme,
	
	rsa_size
):
	print (
		o_rsa_hot_enzyme, 
		o_rsa_cold_enzyme,
		o_fernet_cold_enzyme,
		rsa_size
	)
	
	from os.path import normpath, join, dirname
	HERE = normpath (join (dirname (__file__)))
	
	RSA_HOT 	= normpath (join (dirname (__file__), o_rsa_hot_enzyme))
	RSA_COLD 	= normpath (join (dirname (__file__), o_rsa_cold_enzyme))
	FERNET_COLD = normpath (join (dirname (__file__), o_fernet_cold_enzyme))

	from .ENZYME_CREATOR import ENZYME_CREATOR
	OUTPUTS = ENZYME_CREATOR (
		RSA_SIZE = int (rsa_size),

		WRITE_OUTPUTS = True,
		OUTPUTS = {
			"RSA_HOT_ENZYME": 	o_rsa_hot_enzyme,
			"RSA_COLD_ENZYME": 	o_rsa_cold_enzyme,
			"FERNET_ENZYME": 	o_fernet_cold_enzyme
		}
	);
	
	print ()
	print ("ENZYMES CREATED")
	print ()
	
	return;