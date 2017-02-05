set nocompatible
set incsearch
set ruler
set syntax=on
syntax on
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
set tw=79
set formatoptions+=t
endfunction
"Apply Django syntax to .jinja2 files
au BufNewFile,BufRead *.jinja2 set filetype=django
