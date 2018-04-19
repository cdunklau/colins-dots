set nocompatible
if has('nvim')
    let g:python_host_prog = expand('~/.nvimpython/bin/python')
    let g:python3_host_prog = expand('~/.nvimpython3/bin/python3')
endif

if filereadable(expand('~/.vim/bundle/Vundle.vim'))
    " START Stuff for Vundle https://github.com/VundleVim/Vundle.vim
    filetype off                  " required

    " set the runtime path to include Vundle and initialize
    set rtp+=~/.vim/bundle/Vundle.vim
    call vundle#begin()
    " let Vundle manage Vundle, required
    Plugin 'VundleVim/Vundle.vim'

    " Plugin 'Valloric/YouCompleteMe'

    " All of your Plugins must be added before the following line
    call vundle#end()            " required
    filetype plugin indent on    " required
    " To ignore plugin indent changes, instead use:
    "filetype plugin on
    "
    " Brief help
    " :PluginList          - list configured plugins
    " :PluginInstall(!)    - install (update) plugins
    " :PluginSearch(!) foo - search (or refresh cache first) for foo
    " :PluginClean(!)      - confirm (or auto-approve) removal of unused plugins
    "
    " see :h vundle for more details or wiki for FAQ
    " Put your non-Plugin stuff after this line

    " END Stuff for Vundle

    " YouCompleteMe config
    " Make YCM look for the first python executable in PATH so that pyenv works
    " let g:ycm_server_python_interpreter = 'python'
endif


set incsearch
set ruler
set syntax=on
:syntax on
set backspace=2 " make backspace work like most other apps
set number
set wrap lbr
"Folding settings
set foldmethod=indent
set foldnestmax=10
set nofoldenable
set foldlevel=1
"80 char line limit marker
execute "set colorcolumn=" . join(range(80, 200), ',')
highlight ColorColumn ctermbg=7
"Map F5 to break current line to a max of 76 characters and indent same
nmap <F5> 77<Bar>F r<CR>ddk]p
"Default indentation behavior, 4-space tabs
set tabstop=8
set softtabstop=4
set shiftwidth=4
set expandtab
"specifics for php, 3-space tabs
au BufNewFile,BufRead *.php call DoPHPCommands()
function DoPHPCommands()
set softtabstop=3
set shiftwidth=3
endfunction
"specifics for html, xml, js, json, and css, 2-space tabs
au BufNewFile,BufRead *.html,*.htm,*.xml,*.xsd,*.js,*.json,*.css,*.less call DoHTMLCommands()
function DoHTMLCommands()
set softtabstop=2
set shiftwidth=2
endfunction
"specifics for Makefiles, hard tabs
au BufNewFile,BufRead Makefile call DoMakefileCommands()
function DoMakefileCommands()
set noexpandtab
set tabstop=8
set softtabstop=8
set shiftwidth=8
endfunction
"line wrapping for ReStructuredText
au BufNewFile,BufRead *.rst call DoRSTCommands()
function DoRSTCommands()
set tabstop=8
set softtabstop=4
set shiftwidth=4
set expandtab
set tw=79
set formatoptions+=t
endfunction
"Apply Django syntax to .jinja and .jinja2 files
au BufNewFile,BufRead *.jinja,*.jinja2 set filetype=django
"sls files are salt states in yaml format
au BufNewFile,BufRead *.sls call DoSLSCommands()
function DoSLSCommands()
set softtabstop=2
set shiftwidth=2
set syntax=yaml
endfunction
