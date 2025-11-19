import os
import shutil
import polib
import click
from flask.cli import AppGroup
from app.my_translate import translate  # Google Translate wrapper

# Create a CLI group named 'translate'
translate_cli = AppGroup("translate")


@translate_cli.command("autofill")
@click.argument("lang")
@click.option("--src", default="en", help="Source language (default: en)")
def autofill(lang, src):
    """Auto-fill .po file for a given language using Google Translate."""
    print("Registering autofill command...")

    po_path = f"app/translations/{lang}/LC_MESSAGES/messages.po"
    if not os.path.exists(po_path):
        print(f"Error: File not found → {po_path}")
        return

    backup_path = po_path + ".bak"
    shutil.copy(po_path, backup_path)
    print(f"Backup saved to {backup_path}")

    po = polib.pofile(po_path)
    updated = False

    for entry in po.untranslated_entries():
        if entry.msgid.strip():
            try:
                translated_text = translate(entry.msgid, src, lang)
                entry.msgstr = translated_text
                updated = True
                print(f'Translated: "{entry.msgid}" → "{translated_text}"')
            except Exception as e:
                print(f"Error translating '{entry.msgid}': {e}")

    if updated:
        po.save(po_path)
        print(f"Updated .po file saved to {po_path}")
    else:
        print("No untranslated entries found.")


# Register the CLI group with the Flask app
def register(app):
    app.cli.add_command(translate_cli)
