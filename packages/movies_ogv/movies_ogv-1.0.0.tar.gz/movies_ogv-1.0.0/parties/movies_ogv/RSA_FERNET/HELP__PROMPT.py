




"""
	PM rsa-fernet--help
"""

import click
@click.command	("rsa-fernet--help")
def RSA_FERNET__HELP ():
	print ("""

#---------------------------------------------------------------------------
#---------------------------------------------------------------------------

	MAKE SURE YOU ENCRYPT, ETC. A BACKUP COPY OF THE "ACC"
	INSTEAD OF THE "MAIN" "ACC"

#---------------------------------------------------------------------------
#---------------------------------------------------------------------------

PM rsa-fernet--create-enzymes-folder --folder "ACC/ENZYMES"

PM rsa-fernet--clone-enzymes --de "ACC/ENZYMES" --to "ENZYMES/1"

#
#	COULD USE "ACC ENZYMES" OR "ENZYMES"
#
PM rsa-fernet--heat-cold-folder \\
--cold-folder "ACC/COLD_FOLDER" \\
--cold-eph-folder "ACC/COLD_EPH_FOLDER" \\
--hot-folder "AMYGDALA_R/HOT_FOLDER" \\
--enzymes "ACC/ENZYMES"


PM rsa-fernet--cool-hot-folder \\
--hot-folder "AMYGDALA_R/HOT_FOLDER" \\
--enzymes "ENZYMES/1" \\
--o-cold-folder "AMYGDALA_L/COLD_FOLDER"

#---------------------------------------------------------------------------
#---------------------------------------------------------------------------

#
#	TO CLEAN UP THE COLD FOLDER
#
PM rsa-fernet--forget-eph-cold-folder --cold-folder "AMYGDALA_L/COLD_FOLDER"


#---------------------------------------------------------------------------
#---------------------------------------------------------------------------


	""")
	
	return;