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
"execute "set colorcolumn=" . join(range(80, 200), ',')
set colorcolumn=80,81,82
highlight ColorColumn ctermbg=7
"Map F5 to break current line to a max of 76 characters and indent same
nmap <F5> 77<Bar>F r<CR>ddk]p
"Default indentation behavior, 4-space tabs
set tabstop=8
set softtabstop=4
set shiftwidth=4
set expandtab

def SetSpaceIndentation(width: number): void
  if width <= 0
    throw $"EXCEPT:VALUEERROR('width={width} must be > 0!')"
  endif
  execute "setlocal" $"softtabstop={width}" $"shiftwidth={width}"
enddef

augroup myvimrc
  " Remove all myvimrc autocommands, so I can just source this
  autocmd!

  "make that annoying conceal thing stop in Vim help, see *01.1*
  au FileType help {
    setlocal conceallevel=0
    hi link HelpBar Normal
    hi link HelpStar Normal
  }

  "Python gets an 88-character line length
  "au BufNewFile,BufRead *.py call DoPythonCommands()
  au FileType python setlocal colorcolumn=89,90,91

  "3-space tabs for php
  au FileType php call SetSpaceIndentation(3)

  "2-space tabs and tag closing for html, xml, xsd
  au FileType html,xml,xsd {
    call SetSpaceIndentation(2)
    # auto-close HTML and XML tags
    inoremap <buffer> ><Tab> ><Esc>yyppli/<Esc>f<Space>df>A><Esc>kF<df>A<Tab>
  }

  "2-space tabs for js, jsx, ts, tsx, json, and css
  au FileType javascript,javascriptreact,
    \typescript,typescriptreact,
    \json,css call SetSpaceIndentation(2)

  "hard tabs for Makefiles
  au FileType make setlocal
    \ noexpandtab softtabstop=0 shiftwidth=0

  "line wrapping for ReStructuredText
  au FileType rst setlocal
    \ tabstop=8
    \ softtabstop=4
    \ shiftwidth=4
    \ expandtab
    \ tw=79
    \ formatoptions+=t

  "Apply Django syntax to .jinja and .jinja2 files
  au BufNewFile,BufRead *.jinja,*.jinja2 setlocal filetype=django

  "sls files are salt states in yaml format
  au BufNewFile,BufRead *.sls setlocal filetype=yaml

  "2-space tabs for yaml (and sls)
  au FileType yaml call SetSpaceIndentation(2)

augroup END

" vim: ts=8 sw=2 sts=2
