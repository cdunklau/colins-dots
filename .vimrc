set nocompatible
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
"specifics for html, xml, and css, 2-space tabs
au BufNewFile,BufRead *.html,*.htm,*.xml,*.xsd,*.css call DoHTMLCommands()
function DoHTMLCommands()
set softtabstop=2
set shiftwidth=2
endfunction
