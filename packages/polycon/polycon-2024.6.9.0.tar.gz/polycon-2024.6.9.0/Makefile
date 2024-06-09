PYTHON = python

all: link_install

compile:
	${PYTHON} -m cppimport build

build: compile
	# sudo apt install python3-venv
	# ${PYTHON} -m pip install hatch hatch-cython
	hatch build

clean:
	# rm -rf ~/.micromamba/envs/*/lib/python*/site-packages/polycon ~/.micromamba/envs/*/lib/python*/site-packages/polycon-*
	rm -rf dist/ polycon.egg-info/ 

pip_upload: build
	# ${PYTHON} -m pip install twine 
	${PYTHON} -m twine upload --repository pypi --verbose dist/*

link_install:
	${PYTHON} -m pip install -e .


.PHONY: all \
	build \
	clean \
	compile \
	pip_upload \
	link_install