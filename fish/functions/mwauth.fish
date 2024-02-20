function mwauth --wraps='op read "op://personal/Amazon Midway/password" | mwinit' --description 'Auth to midway, automatically sourcing the PIN from 1Password'
  op read "op://personal/Amazon Midway/password" | mwinit $argv;
end
