if status is-interactive
    # Commands to run in interactive sessions can go here
end

__add_to_path $HOME/.homebrew/bin
__add_to_path $HOME/.homebrew/sbin
__add_to_path $HOME/.pear/bin
__add_to_path $HOME/.toolbox/bin
__add_to_path $HOME/.bin

set EDITOR 'code -w'
set GIT_EDITOR 'code -nw'
set LESSEDIT 'mate -l %lm %f'
set NODE_PATH '/Users/nmannesc/.homebrew/lib/node_modules'

set GPG_TTY (tty)

set NVM_DIR "$HOME/.nvm"

set JAVA_TOOLS_OPTIONS "-DLog4j2.formatMsgNoLookups=true"

if test -x /usr/libexec/java_home
    set JAVA_HOME (/usr/libexec/java_home)
end

