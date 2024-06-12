




import movies_ogv.RSA_fernet_v0.create_enzymes_directory.clique as create_enzymes_directory_clique
import movies_ogv.RSA_fernet_v0.clone_enzymes.clique as clone_enzymes_clique

def clique ():
	import click
	@click.group ("RSA_fernet_v0")
	def group ():
		pass

	import click
	@group.command ("course-1")
	#@click.option ('--example-option', required = True)
	def search (example_option):
		print ("example_option:", example_option)
	
		return;
		
	group.add_command (create_enzymes_directory_clique.command)
	group.add_command (clone_enzymes_clique.command)

	return group




