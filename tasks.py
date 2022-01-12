import logging
import os
import sys

from invoke import Collection, task  # type: ignore[import]

# mypy: allow-untyped-defs


@task(name="update-latest")
def update_latest(c, accept=False):
    c.run(
        f"""
        dasel select -f pyproject.toml -m 'tool.poetry.dev-dependencies.-' \\
            | sed 's/.*/&@latest/g' \\
            | xargs -n1 {"-t" if accept else "echo"} poetry add --dev
        dasel select -f pyproject.toml -m 'tool.poetry.dependencies.-' \\
            | grep -v '^python' \\
            | sed 's/.*/&@latest/g' \\
            | xargs -n1 {"-t" if accept else "echo"} poetry add
        """
    )


py_source = "./src ./tests tasks.py"


@task
def test(c):
    c.run(
        """
        pytest -rA --cov-config=pyproject.toml --cov=src ./tests || exit
        """
    )


@task(name="validate-static")
def validate_static(c, fix=False):
    c.run(
        f"""
        isort {"" if fix else "--check"} {py_source} || exit
        black {"" if fix else "--check"} {py_source} || exit
        flake8 {py_source} || exit
        mypy --show-error-codes --show-error-context \
            {py_source} || exit
        """
    )


@task(pre=[validate_static, test])
def validate(c, fix=False):
    pass


@task(name="validate-fix")
def validate_fix(c):
    c.run(
        f"""
        isort {py_source} || exit
        black {py_source} || exit
        """
    )


@task(name="install-editable")
def install_editable(c, escaped=False):

    script = r"""
    rm -rv src/*.egg-info/
    ## uninstall in venv
    pip3 uninstall -y "$(poetry version | gawk '{ print $1 }')"

    ## escape venv
    IFS=':' read -r -a PATH_ARRAY <<< "$PATH"
    IFS= readarray -d '' NEW_PATH_ARRAY \
        < <(printf "%s\000" "${PATH_ARRAY[@]}" | sed -z '/.venv[/]bin/d')
    PATH=$(IFS=:;echo "${NEW_PATH_ARRAY[*]}")
    unset VIRTUAL_ENV
    export PATH VIRTUAL_ENV
    ## uninstall global
    pip3 uninstall -y "$(poetry version | gawk '{ print $1 }')"

    ## install
    \\rm -rv dist/
    poetry build --format sdist \
        && tar --wildcards -xvf dist/*.tar.gz -O '*/setup.py' > setup.py \
        && pip3 install --prefix="${HOME}/.local/" --editable . || exit
    """

    c.run(script)


@task(pre=[validate])
def all(c):
    pass


@task
def clean(c):
    build_dir = c["build_dir"]
    os.path.exists(build_dir) and c.run(f"rm -rfv {build_dir}")


ns = Collection.from_module(sys.modules[__name__], name="")

ns.configure({"build_dir": "build"})
logging.debug("ns.task_names = %s", ns.task_names)
