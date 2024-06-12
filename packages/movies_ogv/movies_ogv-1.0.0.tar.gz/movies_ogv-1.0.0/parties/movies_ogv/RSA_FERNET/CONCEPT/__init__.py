





"""
	from RSA_FERNET.CONCEPT import CREATE as CREATE_CONCEPT
	CREATE_CONCEPT ("zip")
"""
def CREATE (LINE):
	import shlex
	import subprocess
	import sys
	
	from os.path import normpath, join, dirname
	
	CONCEPT = subprocess.Popen (
		shlex.split (LINE), 
		
		cwd = normpath (join (dirname (__file__))), 	
		
		bufsize 			= - 1,
		executable 			= None, 
		
		stdin 				= None, 
		
		#stdout 			= None, 
		#stderr 			= None, 
		
		stdout 				= sys.stdout,
		stderr 				= sys.stderr,
		
		preexec_fn 			= None, 
		close_fds  			= True, 
		shell				= False, 
		
		env					= None, 
		
		universal_newlines	= None, 
		startupinfo			= None, 
		creationflags		= 0, 
		restore_signals		= True, 
		start_new_session	= False, 
		pass_fds			= (), 
		
		#*, 
		
		group				= None, 
		extra_groups		= None, 
		
		user				= None, 
		umask				= - 1, 
		encoding			= None,
		errors				= None, 
		text				= None, 
		pipesize			= - 1, 
		
		#process_group		= None
	)
	
	CONCEPT.wait ()
	