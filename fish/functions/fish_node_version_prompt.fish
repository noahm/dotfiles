function fish_node_version_prompt --description 'Show active nodejs environment version'
  if which asdf >/dev/null
    set -l node_version (asdf current nodejs 2> /dev/null | awk '{print $2}')
    [ -z "$node_version" -o "$node_version" = "system" ]; and return
    printf "%s(⬢ %s)%s" (set_color green) $node_version (set_color normal)
  end
end
