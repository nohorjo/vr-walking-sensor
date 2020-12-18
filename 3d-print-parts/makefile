SHELL:=/bin/bash

SOURCES=$(shell grep -l scad_render_to_file *.py)

define GEN_DEPS
import os
import re
import sys

filename = sys.argv[1]
importPattern = re.compile("^from \w+ import")

with open(filename) as f:
    importLines = [ line for line in f if importPattern.match(line) ]
    importLines = map(lambda l: l.split()[1] + ".py", importLines)
    importLines = [ imp for imp in importLines if os.path.isfile(imp) ]

    with open(".%s.dep"% filename[:-3], "w") as f:
        f.write("%s: %s"% (filename, " ".join(importLines)))

endef
export GEN_DEPS

.PHONY: all clean scad

all: $(patsubst %.py,stl/%.stl,$(SOURCES))

scad: $(patsubst %.py,_%.scad,$(SOURCES))

.%.dep: %.py
	python -c "$$GEN_DEPS" $<

-include $(patsubst %.py,.%.dep,$(SOURCES))

_%.scad: %.py
	python $<

stl/%.stl: _%.scad
	openscad -D '$$fn=100' -m make -o $@ $< || echo -e "\033[1;41mFAIL\033[0m $@"

clean:
	rm stl/* *.scad .*.scad .*.dep .*.isdep

