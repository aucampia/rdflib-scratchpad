# https://www.gnu.org/software/make/manual/make.html
SHELL=bash
.SHELLFLAGS=-ec -o pipefail
current_makefile:=$(lastword $(MAKEFILE_LIST))
current_makefile_dir:=$(dir $(abspath $(current_makefile)))

.PHONY: all
all: ## do everything (default target)

########################################################################
# variables
########################################################################

py_source=./src ./tests
venv_dir=.venv


ifneq ($(filter all targets,$(VERBOSE)),)
__ORIGINAL_SHELL:=$(SHELL)
SHELL=$(warning Building $@$(if $<, (from $<))$(if $?, ($? newer)))$(TIME) $(__ORIGINAL_SHELL)
endif


poetry=python -m poetry

########################################################################
# targets ...
########################################################################

.PHONY: configure
configure: $(venv_dir) ## comfigure the project
poetry-install $(venv_dir): ## installs the project dependencies
	$(poetry) install

.PHONY: test
test: configure ## run the project's tests
	$(poetry) run pytest --cov-report term --cov-report xml ./tests

.PHONY: test-verbose
test-verbose: configure ## run the project's tests with verbose output
	$(poetry) run pytest -rA --log-level DEBUG --cov-report term --cov-report xml ./tests

.PHONY: validate-static
validate-static: configure ## perform static validation
	$(poetry) run mypy --show-error-codes --show-error-context \
		$(py_source)
	$(poetry) run codespell $(py_source)
	$(poetry) run isort --check $(py_source)
	$(poetry) run black --check $(py_source)
	$(poetry) run flake8 $(py_source)
	$(poetry) export --without-hashes --dev --format requirements.txt | $(poetry) run safety check --full-report --stdin

.PHONY: validate
validate: validate-static test ## validate
all: validate

.PHONY: validate-fix
validate-fix: configure ## fix auto-fixable validation errors
	$(poetry) run pycln --expand-stars --all $(py_source)
	$(poetry) run isort $(py_source)
	$(poetry) run black $(py_source)

.PHONY: clean
clean: clean-dist/ ## clean

.PHONY: distclean
distclean: clean clean-.venv/ ## clean everything

.PHONY: install-editable
install-editable: configure ## install as editable
	rm -rv src/*.egg-info/ || :
	## uninstall
	python -m pip uninstall -y "$$($(poetry) version | gawk '{ print $$1 }')"
	## install
	rm -rv dist/ || :
	$(poetry) build --format sdist \
		&& tar --wildcards -xvf dist/*.tar.gz -O '*/setup.py' > setup.py \
		&& python -m pip install --user --prefix="$${HOME}/.local/" --editable .

.PHONY: install-user
install-user: configure ## install as user package
	rm -rv src/*.egg-info/ || :
	## uninstall
	python -m pip uninstall -y "$$($(poetry) version | gawk '{ print $$1 }')"
	## install
	rm -rv dist/ || :
	$(poetry) build --format sdist \
		&& python -m pip install --user --prefix="$${HOME}/.local/" dist/*.tar.gz

################################################################################
# poetry
################################################################################

pip_compile=pipx run --python python3.6 --spec=pip-tools pip-compile

requirements-poetry.txt: requirements-poetry.in
	$(pip_compile) --quiet --generate-hashes --annotate --emit-options --output-file $(@) $(<)

.PHONY: install-poetry
toolchain: install-poetry
install-poetry: requirements-poetry.txt ## install poetry
	python -m pip install --require-hashes -r requirements-poetry.txt

.PHONY: update-latest
update-latest: ## update dependencies to latests
	dasel select -f pyproject.toml -m 'tool.poetry.dev-dependencies.-' \
		| sed 's/.*/&@latest/g' \
		| xargs -n1 echo $(poetry) add --dev
	dasel select -f pyproject.toml -m 'tool.poetry.dependencies.-' \
		| grep -v '^python' \
		| sed 's/.*/&@latest/g' \
		| xargs -n1 echo $(poetry) add


########################################################################
# toolchain
########################################################################

.PHONY: toolchain
toolchain: ## install toolchain
	go install github.com/tomwright/dasel/cmd/dasel@v1.20.0

########################################################################
# utility
########################################################################

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


## clean directories
.PHONY: clean-%/
clean-%/:
	@{ test -d $(*) && { set -x; rm -vr $(*); set +x; } } || echo "directory $(*) does not exist ... nothing to clean"

## create directories
.PRECIOUS: %/
%/:
	mkdir -vp $(@)
