"""Tool to sort emails from a proton-mail-export directory into folders."""

from functools import cached_property
import datetime as dt
import argparse
import json
from pathlib import Path
import re

__version__ = "0.1"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    return parser.parse_args()


class ProtonEmail:
    def __init__(self, export: "Export", eml_file: Path):
        self.eml_file = eml_file
        self.export = export
        self.json_file = eml_file.parent / (eml_file.stem + ".metadata.json")
        if not eml_file.exists():
            raise ValueError(f"{eml_file} does not exists.")
        if not self.json_file.exists():
            raise ValueError(f"{self.json_file} does not exists.")

    @cached_property
    def metadata(self):
        return json.loads(self.json_file.read_text(encoding="UTF-8"))['Payload']

    @property
    def time(self):
        return dt.datetime.fromtimestamp(self.metadata['Time'])

    @property
    def labels(self) -> list[str]:
        return [self.export.labels[label_id] for label_id in self.metadata['LabelIDs']]

    @property
    def label(self) -> str:
        """Try to find "most interesting" label."""
        most_interesting = None
        for label in self.labels:
            if 'All' not in label:
                most_interesting = label
        if most_interesting:
            return most_interesting
        return self.labels[-1]

    def move_to_folder(self) -> str:
        label = self.label
        if label == "Archive":
            label = f"Archive/{self.time.year}"
        dest = self.export.root / label
        dest.mkdir(exist_ok=True, parents=True)
        self.eml_file.rename(dest / self.eml_file.name)
        self.json_file.rename(dest / self.json_file.name)


class Export:
    """Represents a Protonmail export directory.

    It should be full of ".eml", ".metadata.json" files, and with a
    single "labels.json" file.
    """

    def __init__(self, root):
        self.root = root

    def find_mails(self) -> list[ProtonEmail]:
        for file in self.root.rglob("*.eml"):
            yield ProtonEmail(self, file)

    @cached_property
    def labels(self) -> dict[str, str]:
        """Give a dict of labels by ids."""
        return {
                entry["ID"]: entry["Name"]
                for entry in json.loads(
                    (self.root / "labels.json").read_text(encoding="utf-8")
                )['Payload']
            }


def main():
    args = parse_args()
    export = Export(args.root)
    for email in export.find_mails():
        email.move_to_folder()



if __name__ == "__main__":
    main()
