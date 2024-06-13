from typing import Optional

import click

from amethyst.amethyst import enumerate


@click.group()
def main():
    pass


@main.command()
@click.argument("core_smi", nargs=1, required=True, type=str)
@click.argument(
    "r_file", nargs=1, required=True, type=click.Path(exists=True, dir_okay=False)
)
@click.option("-d", "--delimiter", default="", show_default=True, type=str)
@click.option("-e", "--enantiomers", is_flag=True, default=False)
@click.option("-o", "--output-file")
def generate(
    core_smi: str,
    r_file: str,
    delimiter: Optional[str] = None,
    enantiomers: bool = False,
    output_file: Optional[str] = None,
) -> None:
    if output_file is None:
        output_file = f"output_{core_smi}.txt"

    output: str = ",".join(
        enumerate(
            core_smi, delimiter=delimiter, subs_path=r_file, enantiomers=enantiomers
        )
    )

    with open(output_file, "x") as f:
        f.write(output)
        f.close()
