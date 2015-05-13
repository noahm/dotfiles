# Pacman alias examples
alias pacup='pacman -Syu'		# Synchronize with repositories and then upgrade packages that are out of date on the local system.
# alias pacdl='pacman -Sw'		# Download specified package(s) as .tar.xz ball
alias pacin='pacman -S'		# Install specific package(s) from the repositories
# alias pacins='pacman -U'		# Install specific package not from the repositories but from a file 
alias pacrm='pacman -R'		# Remove the specified package(s), retaining its configuration(s) and required dependencies
alias pacrmrf='pacman -Rns'		# Remove the specified package(s), its configuration(s) and unneeded dependencies
alias pacinfo='pacman -Si'		# Display information about a given package in the repositories
alias pacfind='pacman -Ss'		# Search for package(s) in the repositories
alias pacloc='pacman -Qi'		# Display information about a given package in the local database
alias paclocs='pacman -Qs'		# Search for package(s) in the local database
alias paclo="pacman -Qdt"		# List all packages which are orphaned
alias pacc="pacman -Scc"		# Clean cache - delete all the package files in the cache
alias paclf="pacman -Ql"		# List all files installed by a given package
alias pacown="pacman -Qo"		# Show package(s) owning the specified file(s)
alias pacexpl="pacman -D --asexp"	# Mark one or more installed packages as explicitly installed 
alias pacimpl="pacman -D --asdep"	# Mark one or more installed packages as non explicitly installed
