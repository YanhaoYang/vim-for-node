source ~/.vim/plugins

let g:vim_json_syntax_conceal = 0

set encoding=utf-8
set t_Co=256

" Source support_function.vim to support snipmate-snippets.
if filereadable(expand("~/.vim/bundle/snipmate-snippets/snippets/support_functions.vim"))
  source ~/.vim/bundle/snipmate-snippets/snippets/support_functions.vim
endif

filetype on
filetype plugin indent on   " Automatically detect file types.
syntax on                   " syntax highlighting

let g:seoul256_background = 233
colo seoul256

"The default leader is '\', but many people prefer ',' as it's in a standard
"location
let mapleader = ','

map <C-q> :q<CR>
map <C-x> :qa<CR>
set wrap
set showbreak=...
set spell                       " spell checking on
set hidden                      " allow buffer switching without saving

" UI

set showmode                    " display the current mode

if has('cmdline_info')
  set ruler                   " show the ruler
  set rulerformat=%30(%=\:b%n%y%m%r%w\ %l,%c%V\ %P%) " a ruler on steroids
  set showcmd                 " show partial commands in status line and
  " selected characters/lines in visual mode
endif

if has('statusline')
  set laststatus=2

  " Broken down into easily includeable segments
  set statusline=%<%f\    " Filename
  set statusline+=%w%h%m%r " Options
  set statusline+=\ [%{&ff}/%Y]            " filetype
  set statusline+=%{fugitive#statusline()} "  Git Hotness
  "set statusline+=\ [%{getcwd()}]          " current dir
  set statusline+=%=%-14.(%l,%c%V%)\ %p%%  " Right aligned file nav info
endif

" Remove trailing whitespaces and ^M chars
""autocmd FileType c,cpp,java,php,javascript,python,twig,xml,yml,ruby,eruby autocmd BufWritePre <buffer> :call setline(1,map(getline(1,"$"),'substitute(v:val,"\\s\\+$","","")'))
autocmd BufWritePre * :%s/\s\+$//e

set backspace=indent,eol,start  " backspace for dummies
set linespace=0                 " No extra spaces between rows
set nu                          " Line numbers on
set showmatch                   " show matching brackets/parenthesis
set incsearch                   " find as you type search
set hlsearch                    " highlight search terms
set winminheight=0              " windows can be 0 line high
set ignorecase                  " case insensitive search
set smartcase                   " case sensitive when uc present
set whichwrap=b,s,h,l,<,>,[,]   " backspace and cursor keys wrap to
set scrolljump=5                " lines to scroll when cursor leaves screen
set scrolloff=3                 " minimum lines to keep above and below cursor
set foldenable                  " auto fold code
set foldmethod=indent
set foldcolumn=2
set foldlevel=1
set list
set listchars=tab:\|\ ,trail:.,extends:#,nbsp:. " Highlight problematic whitespace

set wildmenu                    " show list instead of just completing
set wildmode=list:longest,full  " command <Tab> completion, list matches, then longest common part, then all.
set wildignore=*.o,*.obj,*~     "stuff to ignore when tab completing
set wildignore+=*.so,*.swp,*.zip

"jump to last cursor position when opening a file
"dont do it when writing a commit log entry
autocmd BufReadPost * call SetCursorPosition()
function! SetCursorPosition()
  if &filetype !~ 'commit\c'
    if line("'\"") > 0 && line("'\"") <= line("$")
      exe "normal! g`\""
      normal! zz
    endif
  end
endfunction

set autowrite
augroup AutoWrite
  autocmd! BufLeave * :update
augroup END

let g:snipMate = {}
let g:snipMate.scope_aliases = {}
let g:snipMate.scope_aliases['ruby'] = 'ruby,ruby-rails,ruby-rspec,ruby-rspec3,ruby-factorygirl'
imap <C-J> <Plug>snipMateTrigger
smap <C-J> <Plug>snipMateTrigger

nmap <leader>b :Gblame<CR>
nmap <leader>f :Buffers<CR>
nmap <leader>m :Marks<CR>

" ctrlp {
let g:ctrlp_working_path_mode = 'ra'
nnoremap <silent> <D-t> :CtrlP<CR>
nnoremap <silent> <D-r> :CtrlPMRU<CR>
let g:ctrlp_custom_ignore = {
      \ 'dir':  '\.git$\|\.hg$\|\.svn$',
      \ 'file': '\.exe$\|\.so$\|\.dll$' }
"}
" indent_guides {
if !exists('g:spf13_no_indent_guides_autocolor')
  let g:indent_guides_auto_colors = 1
else
  " for some colorscheme ,autocolor will not work,like 'desert','ir_black'.
  autocmd VimEnter,Colorscheme * :hi IndentGuidesOdd  guibg=#212121   ctermbg=3
  autocmd VimEnter,Colorscheme * :hi IndentGuidesEven guibg=#404040 ctermbg=4
endif
set ts=4 sw=4 et
let g:indent_guides_start_level = 2
let g:indent_guides_guide_size = 1
let g:indent_guides_enable_on_vim_startup = 1
" }

function! InitializeDirectories()
  let separator = "."
  let parent = $HOME
  let prefix = '.vim'
  let dir_list = {
        \ 'backup': 'backupdir',
        \ 'views': 'viewdir',
        \ 'swap': 'directory' }

  if has('persistent_undo')
    let dir_list['undo'] = 'undodir'
  endif

  for [dirname, settingname] in items(dir_list)
    let directory = parent . '/' . prefix . dirname . "/"
    if exists("*mkdir")
      if !isdirectory(directory)
        call mkdir(directory)
      endif
    endif
    if !isdirectory(directory)
      echo "Warning: Unable to create backup directory: " . directory
      echo "Try: mkdir -p " . directory
    else
      let directory = substitute(directory, " ", "\\\\ ", "g")
      exec "set " . settingname . "=" . directory
    endif
  endfor
endfunction
call InitializeDirectories()

let g:rubycomplete_buffer_loading = 1
let g:rubycomplete_rails = 1
"set clipboard+=unnamed

set autoindent                  " indent at the same level of the previous line
set shiftwidth=2                " use indents of 4 spaces
set noexpandtab                   " tabs are spaces, not tabs
set tabstop=2                   " an indentation every four columns
set softtabstop=2               " let backspace delete indent
set pastetoggle=<F8>       " pastetoggle (sane indentation on pastes)

au BufNewFile,BufRead Gemfile*			set filetype=ruby
au BufNewFile,BufRead Gemfile*.lock			set filetype=

au BufNewFile,BufRead *.rdoc			set filetype=rdoc
au BufNewFile,BufRead *.textile   set filetype=textile
au BufNewFile,BufRead *.{md,mkdn,markdown} set filetype=markdown

nmap <Leader>pm :PreviewMarkdown<CR>
nmap <Leader>pt :PreviewTextile<CR>
nmap <Leader>pr :PreviewRdoc<CR>
nmap <Leader>ph :PreviewHtml<CR>

map <F9> :cn<CR>
map <F10> @a<CR>
highlight ColorColumn ctermbg=235 guibg=#2c2d27
let &colorcolumn="80,100,".join(range(120,999),",")

" fix crontab: temp file must be edited in place
set backupskip=/tmp/*,/private/tmp/*

" The Silver Searcher
if executable('ag')
  " Use ag over grep
  set grepprg=ag\ --nogroup\ --nocolor

  " Use ag in CtrlP for listing files. Lightning fast and respects .gitignore
  let g:ctrlp_user_command = 'ag %s -l --nocolor -g ""'

  " ag is fast enough that CtrlP doesn't need to cache
  let g:ctrlp_use_caching = 0
endif

" Python
"
"au BufNewFile,BufRead *.py
    "\ set tabstop=4
    "\ set softtabstop=4
    "\ set shiftwidth=4
    "\ set textwidth=79
    "\ set expandtab
    "\ set autoindent
    "\ set fileformat=unix

nnoremap gr :grep <cword> *<CR>
nnoremap Gr :grep <cword> %:p:h/*<CR>
nnoremap gR :grep '\b<cword>\b' *<CR>
nnoremap GR :grep '\b<cword>\b' %:p:h/*<CR>

nnoremap gb :Gblame<CR>
nnoremap gl :%!xmllint --format -<CR>
nnoremap gp :PreviewMarkdown<CR>

let g:pymode_rope_goto_definition_cmd = 'vnew' " Values are (`e`, `new`, `vnew`)
let g:python_host_prog = '/usr/local/bin/python'

" Allow to copy/paste between VIM instances
"copy the current visual selection to ~/.vbuf
vmap <leader>y :w! ~/.vbuf<cr>

"copy the current line to the buffer file if no visual selection
nmap <leader>y :.w! ~/.vbuf<cr>

"paste the contents of the buffer file
nmap <leader>p :r ~/.vbuf<cr>

if !exists("g:ycm_semantic_triggers")
  let g:ycm_semantic_triggers = {}
endif
let g:ycm_semantic_triggers['typescript'] = ['.']
let g:tsuquyomi_disable_default_mappings = 1

" make YCM compatible with UltiSnips (using supertab)
let g:ycm_key_list_select_completion = ['<C-n>', '<Down>']
let g:ycm_key_list_previous_completion = ['<C-p>', '<Up>']
let g:SuperTabDefaultCompletionType = '<C-n>'

" better key bindings for UltiSnipsExpandTrigger
let g:UltiSnipsExpandTrigger="<c-y>"
let g:UltiSnipsJumpForwardTrigger="<c-j>"
let g:UltiSnipsJumpBackwardTrigger="<c-k>"

"------------------------------------------------------------------------------
" NERDTree
"------------------------------------------------------------------------------

" General properties
let NERDTreeDirArrows=1
let NERDTreeMinimalUI=1
let NERDTreeIgnore=['\.pyc', '\~$', '\.swo$', '\.swp$', '\.git', '\.hg', '\.svn', '\.bzr', '\.DS_Store']
let NERDTreeWinSize = 35
let NERDTreeShowBookmarks=1
let NERDTreeShowHidden=1

" Make sure that when NT root is changed, Vim's pwd is also updated
let NERDTreeChDirMode = 2
let NERDTreeShowLineNumbers = 1
let NERDTreeAutoCenter = 1

let NERDTreeQuitOnOpen=1

" Open NERDTree on startup, when no file has been specified
autocmd VimEnter * if !argc() | NERDTree | endif

" Locate file in hierarchy quickly
map <C-f> :NERDTreeFind<CR>

" Toogle on/off
map <C-e> :NERDTreeToggle<CR>:NERDTreeMirror<CR>
