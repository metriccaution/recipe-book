import argparse
from pathlib import Path

from housekeeping.commands.export_json import export_json
from housekeeping.commands.export_json_ld import json_ld_export
from housekeeping.commands.export_typst import typst_export
from housekeeping.commands.normalise import normalise

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "task",
        choices=[
            "normalise",
            "export_json",
            "json_ld_export",
            "typst_export",
        ],
    )
    parser.add_argument("source", default="recipes", nargs="?", type=str)
    parser.add_argument("export", default="export", nargs="?", type=str)
    args = parser.parse_args()

    source_dir = Path(args.source)
    if not source_dir.exists():
        raise ValueError(f"{source_dir.absolute()} doesn't exist")

    export_dir = Path(args.export)

    match args.task:
        case "normalise":
            normalise(source_dir)
        case "export_json":
            export_json(source_dir, export_dir / "full" / "repo.json")
        case "json_ld_export":
            json_ld_export(source_dir, export_dir / "json_ld")
        case "typst_export":
            typst_export(source_dir, export_dir / "pdf")
        case _:
            raise ValueError("Unexpected task argument")
