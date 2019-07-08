#!/usr/bin/python3
import click
import shutil
import os
from m2tools.extension import Extension
from m2tools import package, patcher
import tempfile
import json

import datetime

def patch_meta(meta):
    """
    Update composer.json with extra information
    :param meta:
    :return:
    """
    env_support_email = os.getenv('COMPOSER_SUPPORT_EMAIL') or 'support@example.com'
    env_support_docs = os.getenv('COMPOSER_SUPPORT_DOCS') or 'http://docs.example.com'

    s = getattr(meta, 'support', {})
    s.update({
        'email': env_support_email,
        'docs': env_support_docs
    })
    meta.support = s
    return meta


def make_signature():
    d = datetime.datetime.now()
    env_signature = os.getenv('SOURCES_SIGNATURE') or 'Copyright {date.year}. All rights reserved.\nSee LICENSE.txt for license details.'
    return env_signature.format(date=d)


def make_license():

    return "See {url}".format(url=(os.getenv("LICENSE_URL") or "https://example.com/license.txt"))


@click.group()
@click.pass_context
@click.option('--output', envvar="OUTPUT", default="/results", required=True, type=click.Path())
def cli(ctx, output):
    ctx.obj = {
        'OUTPUT': output
    }


@cli.command()
@click.option('--type', default="marketplace", type=click.Choice(["marketplace"]))
@click.argument('path')
@click.argument('output', envvar="OUTPUT", required=True, type=click.Path())
def pack(type, path, output):
    """
    Create marketplace package
    """
    with Extension(path) as e, tempfile.TemporaryDirectory() as tmpdir:

        module_name = e.meta.name.split('/')[1]
        dest_dir = os.path.join(tmpdir, module_name)
        shutil.copytree(e.path, dest_dir)

        with Extension(dest_dir) as patched_ext:
            patched_ext.init_from_path(dest_dir)
            patched_ext.meta = patch_meta(e.meta)

            # Patch composer.json
            with open(os.path.join(patched_ext.path, 'composer.json'), 'w') as cjs:
                json.dump(dict(patched_ext.meta), cjs, indent=4)

            _sign = make_signature()

            p = patcher.Patcher(patched_ext.path)
            p.patch_files(lambda x: patcher.PhpCode(x).sign(_sign),
                                match=lambda x: x.endswith('.php') or x.endswith('.phtml'))
            p.patch_files(lambda x: patcher.JsCode(x).sign(_sign), match=lambda x: x.endswith('.js'))
            p.patch_files(lambda x: patcher.XmlCode(x).sign(_sign), match=lambda x: x.endswith('.xml'))

            with open(os.path.join(patched_ext.path, 'LICENSE.txt'), 'w') as lf:
                lf.write(make_license())

            package.marketplace(patched_ext, output)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.argument('output', envvar="OUTPUT", required=False, type=click.File('w'))
@click.option('--format', default="{meta.name}-{meta.version}", help="Output format")
def info(path, output, format):
    """
    Read extension info from path or zip
    """
    with Extension(path) as e:
        info = format.format(meta=e.meta, path=e.path).replace('\\n', '\n')
    if output:
        output.write(info)
        return
    click.echo(info)

if __name__ == '__main__':
    cli()
