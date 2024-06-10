import click
import os
import sys
import base64
import difflib
import datetime
import subprocess
import yaml
import toml
from typing import Optional
from logging import getLogger
from .util import find_files

_log = getLogger(__name__)


def make_diff(name: str, new_file: str, old_file: Optional[str] = None):
    newstat = os.stat(new_file)
    new_ts = datetime.datetime.fromtimestamp(newstat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    if old_file:
        oldstat = os.stat(old_file)
        old_ts = datetime.datetime.fromtimestamp(oldstat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    else:
        old_ts = datetime.datetime.fromtimestamp(0).strftime("%Y-%m-%d %H:%M:%S")
    try:
        # text file
        with open(new_file) as ifp:
            new_lines = ifp.readlines()
        if old_file is None:
            old_lines = []
            old_name = "/dev/null"
        else:
            old_name = name + ".orig"
            with open(old_file) as ifp:
                old_lines = ifp.readlines()
        yield from difflib.unified_diff(old_lines, new_lines, old_name, name, old_ts, new_ts)
    except UnicodeDecodeError:
        # binary file
        name2 = name + ".base64"
        with open(new_file, 'rb') as ifp:
            new_bin = ifp.read()
        if old_file is None:
            old_bin = b''
            old_name = "/dev/null"
        else:
            old_name = name2 + ".orig"
            with open(old_file, 'rb') as ifp:
                old_bin = ifp.read()
        new_lines = base64.encodebytes(new_bin).decode('utf-8').splitlines(keepends=True)
        old_lines = base64.encodebytes(old_bin).decode('utf-8').splitlines(keepends=True)
        yield from difflib.unified_diff(old_lines, new_lines, old_name, name2, old_ts, new_ts)


@click.option("--theme")
@click.argument("hugodir", type=click.Path(dir_okay=True, exists=True, file_okay=False),
                default=".")
def hugo_diff_from_theme(hugodir, theme):
    """hugo: diff from theme"""
    ignore_dirs = [".git"]
    ignore_files = [".DS_Store"]
    dirnames = ["archetypes", "assets", "data", "layouts", "resources", "static"]
    paths = [os.path.join(hugodir, x) for x in dirnames]
    themedir = os.path.join(hugodir, "themes", theme)
    if not os.path.isdir(themedir):
        raise click.Abort(f"{themedir} is not directory")
    for dirname, i in find_files(paths, ignore_dirs, ignore_files, ["*"]):
        filename = os.path.join(dirname, i)
        relpath = os.path.relpath(filename, hugodir)
        themepath = os.path.join(themedir, relpath)
        if os.path.exists(themepath):
            # make diff
            _log.info("exists(make diff): filename=%s, relpath=%s, themepath=%s",
                      filename, relpath, themepath)
            for line in make_diff(relpath, filename, themepath):
                if not line.endswith("\n"):
                    click.echo(line)
                    click.echo("\\ No newline at end of file")
                else:
                    click.echo(line, nl=False)
        else:
            # make diff from /dev/null
            _log.info("not exists(make all): filename=%s, relpath=%s, themepath=%s",
                      filename, relpath, themepath)
            for line in make_diff(relpath, filename):
                if not line.endswith("\n"):
                    click.echo(line)
                    click.echo("\\ No newline at end of file")
                else:
                    click.echo(line, nl=False)


@click.option("--theme")
@click.argument("hugodir", type=click.Path(dir_okay=True, exists=True, file_okay=False),
                default=".")
@click.argument("patch", type=click.File("r"), default=sys.stdin)
def hugo_patch_to_theme(hugodir, theme, patch):
    """hugo: patch to theme"""
    import shutil
    proc = subprocess.Popen(["patch", "-p0"], stdin=subprocess.PIPE, cwd=hugodir,
                            encoding='utf-8', text=True)
    out = proc.stdin
    themedir = os.path.join(hugodir, "themes", theme)
    postprocs = []
    for line in patch:
        if line.startswith("+++ "):
            basename = line[4:].split()[0]
            if basename.endswith(".base64"):
                postprocs.append((basename, basename[-7:]))
            filename = os.path.join(hugodir, basename)
            themefname = os.path.join(themedir, basename)
            if os.path.exists(themefname):
                _log.info("copy from theme: %s", basename)
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                shutil.copy(themefname, filename)
            else:
                _log.info("create new(remove): %s", basename)
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                os.unlink(filename)
                # open(filename, 'w').close()
        print(line, file=out, end='')
    out.close()
    proc.wait()
    for b64name, binname in postprocs:
        _log.info("fix b64: %s", binname)
        with open(os.path.join(hugodir, b64name), "rb") as ifp, \
                open(os.path.join(hugodir, binname), "wb") as ofp:
            data = base64.decodebytes(ifp.read())
            ofp.write(data)
        os.unlink(os.path.join(hugodir, b64name))


def parse_dict(lines: list[str]) -> tuple[dict, list[str]]:
    toml_idx = [x for x in range(len(lines)) if lines[x] == '+++\n']
    yaml_idx = [x for x in range(len(lines)) if lines[x] == '---\n']
    format = None
    preamble = None
    content = None
    if len(toml_idx) < 2 and len(yaml_idx) >= 2:
        # yaml preamble + content
        format = 'yaml'
        preamble = lines[yaml_idx[0]+1:yaml_idx[1]]
        content = lines[yaml_idx[1]+1:]
    elif len(yaml_idx) < 2 and len(toml_idx) >= 2:
        # toml preamble + content
        format = 'toml'
        preamble = lines[toml_idx[0]+1:toml_idx[1]]
        content = lines[toml_idx[1]+1:]
    elif len(yaml_idx) >= 2 and len(toml_idx) >= 2:
        # both preamble?
        if yaml_idx[0] < toml_idx[0]:
            # yaml preamble + content
            format = 'yaml'
            preamble = lines[yaml_idx[0]+1:yaml_idx[1]]
            content = lines[yaml_idx[1]+1:]
        else:
            # toml preamble + content
            format = 'toml'
            preamble = lines[toml_idx[0]+1:toml_idx[1]]
            content = lines[toml_idx[1]+1:]
    else:
        # no content
        try:
            data = toml.loads("".join(lines))
            return data, []
        except toml.decoder.TomlDecodeError:
            data = yaml.safe_load("".join(lines))
            return data, []
    if format == 'toml':
        data = toml.loads("".join(preamble))
        return data, content
    if format == 'yaml':
        data = yaml.safe_load("".join(preamble))
        return data, content
    raise Exception("cannot detect format")


@click.option("--format", type=click.Choice(["yaml", "toml"]), default="toml", show_default=True)
@click.argument("input", type=click.File('r'), default=sys.stdin)
@click.argument("output", type=click.File('w'), default=sys.stdout)
def hugo_yamltoml(format, input, output):
    """hugo: yaml <-> toml converter"""
    input_lines = input.readlines()
    data, content = parse_dict(input_lines)
    if format == 'yaml':
        if content:
            print("---", file=output)
        yaml.dump(data, stream=output, encoding='utf-8', allow_unicode=True, sort_keys=False)
        if content:
            print("---", file=output)
            print("".join(content), file=output)
    if format == 'toml':
        if content:
            print("+++", file=output)
        toml.dump(data, f=output)
        if content:
            print("+++", file=output)
            print("".join(content), file=output)
