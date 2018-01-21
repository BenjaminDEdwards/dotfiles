" templates.vim
"
" Templating for the vim editor
"
" This module is designed to load standardised lumps of code from
" template files.
"
" COMMANDS

" UnitTest
"   Turn the current file into a unit test class
"   :UnitTest
"
" NewTest
"   Write a new test
"
" LogFunc
"   Write a log message (Venda Specific)
"
" Template arg
"   Looks for the file arg and reads it into the current buffer
"   at the current position


function! DeclarePackage ()
    let  fpath = substitute( expand("%") , ".pm", "", "")
    let  dir = split( fpath ,'/' )
    call remove( dir, 0 )

    return join(dir,"::")

endfunction

function! TemplateUnitTestClass(class)
    read ~/.vim/templates/unitTestClass.txt
    1delete
    let classpath = DeclarePackage()
    execute '%s/' . 'CLASSPATH' . '/' . classpath . '/g'
    execute '%/TODO'
endfunction

command! -nargs=? UnitTest call TemplateUnitTestClass(<q-args>)

function! s:NewUnitTest(class)
    let line = getline(1)
    let line = substitute(line, 'package ','','')
    let classname = matchstr(line, '[a-zA-Z:]*')
    echo line
endfunction

command! -nargs=1 Newtest call TemplateTest(<q-args>)
function! TemplateTest(name)
    read ~/.vim/templates/test.txt
    execute '%s/' . 'NAME' . '/' . a:name . '/g'
    /CODE
    return "Done"
endfunction

command! -nargs=1 LogFunc call TemplateLogFunc(<q-args>)
function! TemplateLogFunc(name)
    read ~/.vim/templates/logfunc.txt
    execute '%s/' . 'MSG' . '/' . a:name . '/g'
    /dumper
    return "Done"
endfunction



command! -nargs=1 Template call LoadTemplate(<q-args>)
function! LoadTemplate(filename)
    perl <<EOF

    # Get the row and culumn of the current buffer.
    my ($row,$col) = $curwin->Cursor();

    my $file_name = $ENV{"HOME"} . "/.vim/templates/" . VIM::Eval('a:filename');

    my $file = $file_name;
    open(F, "<", $file );
    my @lines = (<F>);

    foreach my $line ( @lines ) {
        chomp $line;
    }

    $curbuf->Append($row,@lines);

EOF
    return "Done"
endfunction
