all:
	zhixin -c qtcreator run

# regenerate project files to reflect zhixin.ini changes
project-update:
	@echo "This will overwrite project metadata files.  Are you sure? [y/N] " \
	    && read ans && [ $${ans:-'N'} = 'y' ]
	zhixin project init --ide qtcreator

# forward any other target (clean, build, etc.) to zx run
{{'%'}}:
	zhixin -c qtcreator run --target $*
