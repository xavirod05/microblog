import os
from flask import Blueprint
import click
import shutil, polib
from app.my_translate import translate  # assumes translate(msgid, src, dest)
bp = Blueprint('cli', __name__, cli_group=None)


@bp.cli.group()
def babel():
    """Translation and localization commands."""
    pass


@babel.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(
            'pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')


@babel.command()
def update():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')


@babel.command()
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')
@babel.command()
@click.argument('lang')
@click.option('--src', default='en', help='Source language (default: en)')
def autofill(lang, src):
    """Auto-fill .po file for a given language using Google Translate."""
    print("This is the autofill from cli.py...")

    po_path = f'app/translations/{lang}/LC_MESSAGES/messages.po'
    if not os.path.exists(po_path):
        print(f"Error: File not found → {po_path}")
        return

    backup_path = po_path + '.bak'
    shutil.copy(po_path, backup_path)
    print(f"Backup saved to {backup_path}")

    po = polib.pofile(po_path)
    updated = False

    for entry in po.untranslated_entries():
        if entry.msgid.strip():
            print(f"translating: {entry.msgid}")
            translated_text = translate(entry.msgid, src, lang)
            entry.msgstr = translated_text
            updated = True
            print(f'Translated: "{entry.msgid}" → "{translated_text}"')

    if updated:
        po.save(po_path)
        print(f'Updated .po file saved to {po_path}')
    else:
        print('No untranslated entries found.')