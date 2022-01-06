function __add_to_path --argument path
    if test -d "$path"; and not contains $path $PATH
        set -gx PATH $path $PATH
    end
end