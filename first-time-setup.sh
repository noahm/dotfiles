# install X-code command line tools to make git available first
cd ~
xcode-select --install
sudo xcodebuild -license

git clone https://github.com/Homebrew/brew.git .homebrew
PATH="$HOME/.homebrew/bin:$PATH" # temp bootstrap for running homebrew ASAP

# brew cask install firefox
brew cask install 1password

# stop and log in to dropbox, get private key out of 1password and into ~/.ssh/
# update homebrew repo remote to git@github.com:Homebrew/brew.git

git clone git@github.com:noahm/dotfiles.git .dotfiles

mkdir .config
mkdir .bin

ln -s .dotfiles/inputrc .inputrc
ln -s .dotfiles/profile .profile
ln -s .dotfiles/screenrc .screenrc
ln -s .dotfiles/tmux.conf .tmux.conf
ln -s .dotfiles/gitignore .gitignore
ln -s .dotfiles/gitconfig .gitconfig
ln -s .dotfiles/fish .config/fish

# switch to fish shell
brew install fish
echo "$HOME/.homebrew/bin/fish" | pbcopy
sudo nano /etc/shells # paste on new line, save, quit (cat to file doesn't work with sudo?)
chsh -s $HOME/.homebrew/bin/fish

# download and install nerdfont version of SCP
# https://github.com/ryanoasis/nerd-fonts/releases

# install starship shell framework
curl -sS https://starship.rs/install.sh | BIN_DIR=~/.bin sh

brew install git asdf
asdf plugin add nodejs https://github.com/asdf-vm/asdf-nodejs.git

# Update terminal preferences with font and window size (170x35)

brew install --cask install visual-studio-code
brew install --cask 1password/tap/1password-cli
brew install --cask install charles
brew install --cask install obs
brew install --cask install keybase # then launch gui once to have cli auto-installed

# Setup key signing with keybase + gpg, follow:
# https://github.com/pstadler/keybase-gpg-github
brew install gpg # slow!
keybase login
keybase pgp export | gpg --import
keybase pgp export --secret | gpg --allow-secret-key-import --import
# brew install --cask gpg-suite
brew install pinentry-mac
# add to ~/.gnupg/gpg-agent.conf
echo "pinentry-program /Users/nmannesc/.homebrew/bin/pinentry-mac" >> ~/.gnupg/gpg-agent.conf

# fix subpixel rendering in vs code + mojave
# defaults write com.microsoft.VSCode.helper CGFontRenderingFontSmoothingDisabled -bool NO

# Solve weird TTY issues with gpg:
#Add this to ~/.gnupg/gpg.conf:
"
use-agent
pinentry-mode loopback
"
# And add this to ~/.gnupg/gpg-agent.conf
"allow-loopback-pinentry"

# Then restart the agent with
echo RELOADAGENT | gpg-connect-agent
