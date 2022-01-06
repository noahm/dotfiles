function fish_nvm_prompt --description 'Show active nvm environment'
  if set -q NVM_BIN
    printf "%s(node: %s)%s" (set_color brblack) (node -v) (set_color normal)
  end
end
