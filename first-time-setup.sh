# install X-code command line tools to make git available first
cd ~

sudo xcodebuild -license

git clone https://github.com/Homebrew/brew.git .homebrew
PATH="$HOME/.homebrew/bin:$PATH" # temp bootstrap for running homebrew ASAP

# brew cask install firefox
brew cask install 1password
brew cask install dropbox

# stop and log in to dropbox, get private key out of 1password and into ~/.ssh/
# update homebrew repo remote to git@github.com:Homebrew/brew.git

git clone git@github.com:noahm/dotfiles.git .dotfiles

ln -s .dotfiles/inputrc .inputrc
ln -s .dotfiles/profile .profile
ln -s .dotfiles/screenrc .screenrc
ln -s .dotfiles/tmux.conf .tmux.conf
ln -s .dotfiles/gitignore .gitignore
ln -s .dotfiles/gitconfig .gitconfig

brew install bash-completion git tmux
brew tap caskroom/fonts
brew cask install font-source-code-pro

# Update terminal preferences with font and window size (170x35)

brew cask install visual-studio-code
brew cask install sublime-text
brew cask install slack
brew cask install google-chrome
brew cask install twitch
brew cask install charles
brew cask install obs
brew cask install keybase

# Setup key signing with keybase + gpg, follow:
# https://github.com/pstadler/keybase-gpg-github
brew install gpg # slow!
keybase login
keybase pgp export | gpg --import
keybase pgp export --secret | gpg --allow-secret-key-import --import
brew cask install gpg-suite
brew install pinentry-mac
# add to ~/.gnupg/gpg-agent.conf
echo "pinentry-program /Users/nmannesc/.homebrew/bin/pinentry-mac" >> ~/.gnupg/gpg-agent.conf

# fix subpixel rendering in vs code + mojave
defaults write com.microsoft.VSCode.helper CGFontRenderingFontSmoothingDisabled -bool NO

cat ~/.dotfiles/vscode-settings.json | pbcopy
# open vscode, paste in settings

# TODO automate installation of package control in sublime and preferred packages?
# TODO automate installation of favorite VS Code extensions?
