import argparse
import importlib
import json
import pathlib
import subprocess
import typing

import rich
import typer

from .change_detection import *

app = typer.Typer()
console = rich.console.Console()


CMD_SEP = "=="  # unfortunately, using -> and => cause problems with the shells...
DB_NAME = ".run-if.json"


def print_version(value: bool):
    if value:
        v = importlib.metadata.version("run_if_changed")
        print(v)
        raise typer.Exit(0)


@app.command()
def run_if(
    arguments: typing.List[str],
    version: typing.Annotated[
        bool,
        typer.Option(
            "--version", help="Print version number and exit.", callback=print_version
        ),
    ] = False,
    run_until_success: typing.Annotated[
        bool,
        typer.Option(
            help="Run command, even if target(s) exists and dependency(ies) have not changed, if it was unsuccessful (returned non-zero exit status) the last time."
        ),
    ] = False,
):
    dependencies_command_targets = [[], [], []]

    # load the database (just a dict)
    DB_PATH = pathlib.Path(DB_NAME)
    if not DB_PATH.exists():
        DB_PATH.write_text("{}")
    db = json.loads(DB_PATH.read_text())
    for section in ["dependency hashes", "exit codes"]:
        if section not in db:
            db[section] = {}

    # sort the arguments
    current_type = 0
    for a in arguments:
        if a.strip() == CMD_SEP:
            current_type += 1
            if current_type > 2:
                print(
                    f"Too many '{CMD_SEP}' found in argument list. There should only be two."
                )
                raise typer.Exit(2)
            continue
        dependencies_command_targets[current_type].append(a)

    # we assume that the command should not be run
    # because it is obviously expensive (if it wasn't you would not need us).
    run_command = False
    # convince us that it _does_ need to run...

    # check for missing targets
    for t in [pathlib.Path(a) for a in dependencies_command_targets[2]]:
        if not t.exists():
            run_command = True
            break

    # check for changed dependencies
    # do determine if a dependency has changed, we compute its hash
    # and compare it to the last time we ran.
    # BUT, we only want to compare to the last time we ran _this_ command,
    # that way we can run several command in a row with the same
    # dependencies and they will all run.
    command_hash = md5sum((" ".join(dependencies_command_targets[1])).encode())
    if command_hash not in db["dependency hashes"]:
        db["dependency hashes"][command_hash] = {}
    dep_hashes = db["dependency hashes"][command_hash]
    for dep in [pathlib.Path(a) for a in dependencies_command_targets[0]]:
        _hash = compute_hash(dep)

        if dep_hashes.get(str(dep), None) != _hash:
            run_command = True
        dep_hashes[str(dep)] = _hash

    # write updated hashes back to disk before we have a chance to crash...
    DB_PATH.write_text(json.dumps(db))

    if run_command == False and run_until_success:
        # if the --run-until-success option has been given, we want to
        # run the command, even if the dependencies have not changes,
        # if it failed the last time we ran it.
        if db["exit codes"].get(command_hash, 1) != 0:
            run_command = True

    # run command if needed
    if run_command:
        try:
            # results = subprocess.run(dependencies_command_targets[1])
            results = subprocess.Popen(
                dependencies_command_targets[1],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            for line in iter(results.stdout.readline, b""):
                print(line.rstrip().decode())
            db["exit codes"][command_hash] = results.returncode
            DB_PATH.write_text(json.dumps(db))
            raise typer.Exit(results.returncode)
        except FileNotFoundError as e:
            print(f"Error running command: {e}")
            raise typer.Exit(127)

    raise typer.Exit(0)
