from pathlib import Path

from housekeeping.models.repository import RecipeRepository


def export_json(source_dir: Path, export_path: Path):
    """Load the repo, then write out a compiled version of the repository into
    a single JSON file, intended for programmatic consumption.
    """

    repo = RecipeRepository.from_directory(source_dir)
    export_path.parent.mkdir(exist_ok=True, parents=True)
    with open(export_path, mode="w") as f:
        f.write(
            repo.model_dump_json(
                exclude_none=True,
                indent=2,
            )
        )
