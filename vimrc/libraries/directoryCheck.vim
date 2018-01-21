
" EnsureDirExists
"
" Makes a directory if the file to write to is in a directory path
" that does not exist
function! EnsureDirExists ()
    let required_dir = expand("%:h")
    if !isdirectory(required_dir)
        call mkdir( required_dir, 'p' )
    endif
endfunction

" Override NewFile so as well as creating a new file, it creates
" the directory path as well
augroup AutoMkdir
    autocmd!
    autocmd BufNewFile * :call EnsureDirExists()
augroup END
