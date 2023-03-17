if status is-interactive
    # Commands to run in interactive sessions can go here
end

__add_to_path $HOME/.homebrew/bin
__add_to_path $HOME/.homebrew/sbin
__add_to_path $HOME/.pear/bin
__add_to_path $HOME/.toolbox/bin
__add_to_path $HOME/.bin
__add_to_path $HOME/.deta/bin

set -gx EDITOR 'code -w'
set -gx GIT_EDITOR 'code -nw'
set -gx LESSEDIT 'mate -l %lm %f'
set -gx NODE_PATH '/Users/nmannesc/.homebrew/lib/node_modules'

set -gx GPG_TTY (tty)

if test -x /usr/libexec/java_home and /usr/libexec/java_home 2>/dev/null
    set -gx JAVA_HOME (/usr/libexec/java_home)
    set -gx JAVA_TOOLS_OPTIONS "-DLog4j2.formatMsgNoLookups=true"
end

if test -f ~/.asdf/asdf.fish
    source ~/.asdf/asdf.fish
else if which brew >/dev/null
    source (brew --prefix asdf)/libexec/asdf.fish
end

starship init fish | source
