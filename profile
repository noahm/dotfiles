PATH="$(python -c "from sys import prefix; print prefix")/bin:$HOME/.homebrew/bin:$HOME/.homebrew/sbin:$HOME/.pear/bin:$HOME/.toolbox/bin:$HOME/.bin:$PATH"
export EDITOR='code -w'
export GIT_EDITOR='code -nw'
export LESSEDIT='mate -l %lm %f'
export NODE_PATH='/Users/noah/.homebrew/lib/node_modules'

[ -s /usr/libexec/java_home ] && export JAVA_HOME=$(/usr/libexec/java_home)

### For keybase ###
export GPG_TTY=$(tty)

[ -f "${HOME}/.bash_aliases" ] && source "${HOME}/.bash_aliases"

### Auto completion support ###
source $HOME/.homebrew/etc/bash_completion

export NVM_DIR="$HOME/.nvm"
# Load nvm
[ -s "${HOME}/.homebrew/opt/nvm/nvm.sh" ] && . "${HOME}/.homebrew/opt/nvm/nvm.sh"
# Load nvm bash_completion
[ -s "${HOME}/.homebrew/opt/nvm/etc/bash_completion.d/nvm" ] && . "${HOME}/.homebrew/opt/nvm/etc/bash_completion.d/nvm"

### convenience stuff ###

# Dev SSH Shell: shortcut to open a remote tmux session
function dsh {
  scp -q ~/.tmux.conf $1: # copy the local config file up
  ssh $1 -t "tmux attach || tmux" # start ssh by connecting to an existing tmux sesson or creating a new one if none exist
}

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.bin" ] ; then
  PATH="$HOME/.bin:$PATH"
fi

### Custom prompt stuff ###
function __git_dirty {
  git diff --quiet HEAD &>/dev/null
  [ $? == 1 ] && echo "✗"
}

function __git_branch {
  __git_ps1 " %s"
}

function __my_rvm_ruby_version {
  local gemset=$(echo $GEM_HOME | awk -F'@' '{print $2}')
  [ "$gemset" != "" ] && gemset="@$gemset"
  local version=$(echo $MY_RUBY_HOME | awk -F'-' '{print $2}')
  [ "$version" == "1.9.2" ] && version=""
  local full="$version$gemset"
  [ "$full" != "" ] && echo "$full "
}

bash_prompt() {
  local NONE="\[\033[0m\]"    # unsets color to term's fg color

  # regular colors
  local K="\[\033[0;30m\]"    # black
  local R="\[\033[0;31m\]"    # red
  local G="\[\033[0;32m\]"    # green
  local Y="\[\033[0;33m\]"    # yellow
  local B="\[\033[0;34m\]"    # blue
  local M="\[\033[0;35m\]"    # magenta
  local C="\[\033[0;36m\]"    # cyan
  local W="\[\033[0;37m\]"    # white
  local PB="\[\033[38;5;75m\]"   # pale blue
  local DB="\[\033[38;5;33m\]"   # darker blue

  # emphasized (bolded) colors
  local EMK="\[\033[1;30m\]"
  local EMR="\[\033[1;31m\]"
  local EMG="\[\033[1;32m\]"
  local EMY="\[\033[1;33m\]"
  local EMB="\[\033[1;34m\]"
  local EMM="\[\033[1;35m\]"
  local EMC="\[\033[1;36m\]"
  local EMW="\[\033[1;37m\]"

  # background colors
  local BGK="\[\033[40m\]"
  local BGR="\[\033[41m\]"
  local BGG="\[\033[42m\]"
  local BGY="\[\033[43m\]"
  local BGB="\[\033[44m\]"
  local BGM="\[\033[45m\]"
  local BGC="\[\033[46m\]"
  local BGW="\[\033[47m\]"

  local UC=$W                 # user's color
  [ $UID -eq "0" ] && UC=$R   # root's color

  # PS1="$EMB\$(__my_rvm_ruby_version)$PB\h$EMW:$DB\w$W\$(__git_branch)$EMR\$(__git_dirty)$W ➜$NONE "
  PS1="$PB\h$EMW:$DB\w$W\$(__git_branch)$EMR\$(__git_dirty)$W ➜$NONE "
}

bash_prompt
unset bash_prompt

# if [ -f "$(brew --prefix bash-git-prompt)/share/gitprompt.sh" ]; then
#   GIT_PROMPT_THEME=Default
#   source "$(brew --prefix bash-git-prompt)/share/gitprompt.sh"
# fi

# [[ -s "/Users/noah/.rvm/scripts/rvm" ]] && source "/Users/noah/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*
export JAVA_TOOLS_OPTIONS="-DLog4j2.formatMsgNoLookups=true"
