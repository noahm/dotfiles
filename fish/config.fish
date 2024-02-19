if status is-interactive
    # Commands to run in interactive sessions can go here
end

fish_add_path $HOME/.homebrew/bin
fish_add_path $HOME/.homebrew/sbin
fish_add_path $HOME/.pear/bin
fish_add_path $HOME/.toolbox/bin
fish_add_path $HOME/.local/bin
fish_add_path $HOME/.bin
fish_add_path $HOME/.cargo/bin
fish_add_path $HOME/.deta/bin
fish_add_path $HOME/.fly/bin

# pnpm
if test -d ~/.local/share/pnpm
    set -gx PNPM_HOME "~/.local/share/pnpm"
    fish_add_path $PNPM_HOME
end
# pnpm end

# bun
if test -d ~/.bun
    set --export BUN_INSTALL "$HOME/.bun"
    fish_add_path $BUN_INSTALL/bin
end

set -gx EDITOR 'code -w'
set -gx GIT_EDITOR 'code -nw'
set -gx LESSEDIT 'mate -l %lm %f'

# if test -d ~/.homebrew/lib/node_modules
#     set -gx NODE_PATH ~/.homebrew/lib/node_modules
# end

if test -x ~/.bin/start-ssh-agent-proxy
    start-ssh-agent-proxy
    set -gx SSH_AUTH_SOCK ~/.1password/agent.sock
end

set -gx GPG_TTY (tty)

if test -x /usr/libexec/java_home and /usr/libexec/java_home 2>/dev/null
    set -gx JAVA_HOME (/usr/libexec/java_home)
    set -gx JAVA_TOOLS_OPTIONS "-DLog4j2.formatMsgNoLookups=true"
end

if which mise >/dev/null
  mise activate fish | source
end

starship init fish | source
