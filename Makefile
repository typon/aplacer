MAINDIR = placer
EASYGLFILES = $(MAINDIR)/easygl/graphics.cpp $(MAINDIR)/easygl/easygl.cpp $(MAINDIR)/easygl/easygl.pyx
EASYGL_OJBS = $(MAINDIR)/easygl/*.so

SRC_FILES = $(EASYGLFILES) setup.py
OBJ_FILES = $(EASYGL_OJBS)


all: build run
test: build runtest

build: $(OBJ_FILES)

$(OBJ_FILES): $(SRC_FILES)
	python3 setup.py build_ext --inplace ${ARGS}

run:
	python3 main.py

runtest:
	pytest -s tests/test_htoolz.py

clean:
	rm $(OBJ_FILES)
