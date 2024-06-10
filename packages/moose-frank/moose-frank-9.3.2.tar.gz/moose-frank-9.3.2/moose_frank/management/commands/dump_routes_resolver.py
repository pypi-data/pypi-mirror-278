"""
    Django JS Routes resolver dump command
    ======================================

    This command allows to export a JS module containing the Django URLs that should be exposed on
    the client side as of a resolver helper allowing to perform URL lookups.

"""

from os import path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import translation

from moose_frank.js_routes.serializers import url_patterns_serializer


class Command(BaseCommand):
    """Dumps Django URLs and the resolver helper in a single TS file."""

    help = "Dump Django URLs and the resolver helper to a TS file per language."

    def add_arguments(self, parser):
        parser.add_argument(
            "-o",
            "--output-dir",
            required=True,
            help="Specifies a directory to which the output is written.",
        )

    def _write_resolver_file(self, filename):
        with open(filename, "w") as output:
            output.write(
                render_to_string(
                    "js_routes/_dump/resolver.ts",
                    {"routes": url_patterns_serializer.to_json()},
                )
            )

    def handle(self, *args, **options):
        filename = path.join(options["output_dir"], "index.ts")
        self._write_resolver_file(filename)

        for lang, _ in settings.LANGUAGES:
            with translation.override(lang):
                filename = path.join(options["output_dir"], f"{lang}.ts")
                self._write_resolver_file(filename)
