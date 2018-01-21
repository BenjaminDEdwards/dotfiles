syntax on
filetype plugin on


set smartindent
set tabstop=4
set shiftwidth=4
set expandtab

set shiftwidth=4
set softtabstop=4

set number

set hlsearch
set incsearch
set smartcase

map   <S-tab>  :tabprevious<cr>:echo @%<cr>
map   <tab>    :tabnext<cr>:echo @%<cr>
imap  <S-tab>    <C-n>

map   <S-f2>   :echo expand('%:p')<cr>

" move with ctrl up or down
nmap <silent> <C-Up> :wincmd k<CR>
nmap <silent> <C-Down> :wincmd j<CR>
nmap <silent> <C-Left> :wincmd h<CR>
nmap <silent> <C-Right> :wincmd l<CR>
" Map f-keys
" f1 Reload the vimrc files
" f2  Display name of current file
" f3  Toggle TagsList code browser - show subroutines.
" f4  Split Screen and open file manager
" f5  New Tab
" f6  Quit
" f7
" f8
" f9  Visual Style code folding
" f10 Highlight whitespace at end of lines
" f11 GIT - substiture 'pick' for 'squash'
" f12 GIT - substiture 'pick' for 'fixup'

map   <f1>  :NERDTree<cr>
map   <f2>  :TlistToggle<cr>
map   <f3>  :GitBlame()<cr>
map   <f4>  :GitLog<cr>
map   <f5>  :Shell source ~/.bashrc; bundle exec rake cucumber<cr><cr>:set nonumber<cr>:res5<cr><S-g>
map   <f6>  :q<cr>
map   <f7>  :GitDiff<cr>
map   <f8>  :bnext<cr>
map   <f9>  zfa}
map   <f10> /\s\+$/
map   <f11> :s/pick/squash/ <cr>
map   <f12> :s/pick/fixup/ <cr>

" Leader commands
map <Leader>b :buffers<cr>:b<Space>
map <Leader>v :vsplit<cr>
map <Leader>s :split<cr>
map <Leader>q :quit<cr>
map <Leader>o :e.<cr>
map <leader>t :ConqueTerm bash<cr>
map <leader>j :%!python -m json.tool<cr>
map <leader>p "*p$i

" map ; to ; so that ;q does the right thing
map ; :

"highlight trailing whitespace
highlight WHITE_ON_RED ctermfg=white ctermbg=red
match WHITE_ON_RED /\s\+$/

let &titlestring = $TITLE
if &term == "screen"
      set t_ts=^[k
      set t_fs=^[\
endif
if &term == "screen" || &term == "xterm"
        set title
endif

" Match angle brackets...
set matchpairs+=<:>

" Give mouse cursor
set mouse=a

" Use an efficient text completion
set iskeyword+=:

" spell checking
" Loads a file with common errors and correcitons
source ~/.vim/spelling.vim

"Directory Check
source ~/.vim/libraries/directoryCheck.vim

"Enter code via templates
source ~/.vim/libraries/templates.vim

"Run shell commands and put the results in a scratch buffer
source ~/.vim/libraries/runshellcommand.vim

"Gvim uses different configurations.
if has("gui_running")
    source ~/.vim/gvimrc
endif
