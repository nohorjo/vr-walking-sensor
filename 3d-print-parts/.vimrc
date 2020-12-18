set foldmethod=marker

function! Update()
python3 << EOF
import os
import re

filename = os.path.normpath(vim.eval("bufname('%')"))
importPattern = re.compile("^from \w+ import")

os.system("python3 " + filename)

with open(filename) as f:
    importLines = [ line for line in f if importPattern.match(line) ]
    importLines = map(lambda l: l.split()[1], importLines)

    for imp in importLines:
        if os.path.isfile(imp + ".py"):
            depsfile = ".%s.isdep"% imp
            toAdd = filename + "\n"
            with open(depsfile, 'a+') as df:
                df.seek(0)
                if not toAdd in df:
                    df.write(toAdd)

isdep = ".%s.isdep"% filename[:-3]

try:
    f = open(isdep)
    for line in f:
        if os.path.isfile(line.strip()):
            os.system("python3 " + line)
    f.close()
except FileNotFoundError:
    pass
EOF
endfunction

function! NewPython()
    let i = 0
    call append(i, "from solid import *") | let i = i + 1
    call append(i, "from solid.utils import *") | let i = i + 1
    call append(i, "") | let i = i + 1
    call append(i, "from constants import *") | let i = i + 1
    call append(i, "from moveable_point import *") | let i = i + 1
    call append(i, "from super_hole import *") | let i = i + 1
    call append(i, "") | let i = i + 1
    call append(i, "if __name__ == '__main__':") | let i = i + 1
    call append(i, "    model = None") | let i = i + 1
    call append(i, "    scad_render_to_file(model, '_%s.scad'% __file__[:-3])") | let i = i + 1
    execute i - 1
endfunction

augroup SolidPython
    autocmd!
    autocmd BufWritePost *.py silent! call Update()
    autocmd BufNewFile *.py silent! call NewPython()
augroup END

command! OpenScad execute "vs _".expand("%:r").".scad"

inoremap (( (<ESC>A)<ESC>%i
