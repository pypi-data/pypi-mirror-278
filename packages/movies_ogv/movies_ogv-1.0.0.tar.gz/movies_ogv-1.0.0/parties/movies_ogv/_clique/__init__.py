




from .group import clique as clique_group

import movies_ogv.RSA_fernet_v0.clique as RSA_fernet_v0_clique

def clique ():
	import click
	@click.group ()
	def group ():
		pass

	import click
	@click.command ("example")
	def example_command ():	
		print ("example")

	group.add_command (example_command)
	group.add_command (clique_group ())
	group.add_command (RSA_fernet_v0_clique.clique ())
	
	
#
	#	E1
	#
	from movies_ogv.RSA_FERNET.CREATE_ENZYMES__PROMPT import RSA_FERNET__CREATE_ENZYMES
	group.add_command (RSA_FERNET__CREATE_ENZYMES)
	
	
	#
	#	E2
	#
	from movies_ogv.RSA_FERNET.CREATE_ENZYMES_FOLDER__PROMPT import RSA_FERNET__CREATE_ENZYMES_FOLDER
	group.add_command (RSA_FERNET__CREATE_ENZYMES_FOLDER)
	
	from movies_ogv.RSA_FERNET.CLONE_ENZYMES__PROMPT import RSA_FERNET__CLONE_ENZYMES
	group.add_command (RSA_FERNET__CLONE_ENZYMES)

	from movies_ogv.RSA_FERNET.HEAT_COLD_FOLDER__PROMPT import RSA_FERNET__HEAT_COLD_FOLDER
	group.add_command (RSA_FERNET__HEAT_COLD_FOLDER)
	
	from movies_ogv.RSA_FERNET.COOL_HOT_FOLDER__PROMPT import RSA_FERNET__COOL_HOT_FOLDER
	group.add_command (RSA_FERNET__COOL_HOT_FOLDER)
	
	from movies_ogv.RSA_FERNET.FORGET_EPH_COLD_FOLDER import RSA_FERNET__FORGET_EPH_COLD_FOLDER
	group.add_command (RSA_FERNET__FORGET_EPH_COLD_FOLDER)
	
	from movies_ogv.RSA_FERNET.HELP__PROMPT import RSA_FERNET__HELP
	group.add_command (RSA_FERNET__HELP)	
	
	group ()




#
