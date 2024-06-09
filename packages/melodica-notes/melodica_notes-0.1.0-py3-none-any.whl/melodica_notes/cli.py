from rich.console import Console
from rich.table import Table
from typer import Argument, Typer

from melodica_notes.chords import chord as _chord
from melodica_notes.harmonics import harmonic as _harmonic
from melodica_notes.scales import scale as _scale

console = Console()
app = Typer()


@app.command()
def scale(
        tonic_note: str = Argument("C", help="Tonic Note"),
        scale_type: str = Argument("major", help="Scale Mode")
) -> None:
    """
    Display a scale based on a tonic note and scale mode.

    Args:
        tonic_note (str): The tonic note of the scale. Default is "C".
        scale_type (str): The scale mode. Default is "major".

    Returns:
        None
    """
    table = Table()

    notes, degrees = _scale(tonic_note, scale_type).values()

    for degree in degrees:
        table.add_column(degree)

    table.add_row(*notes)

    console.print(table)


@app.command()
def chord(tonic_note: str = Argument("C", help="Tonic Note")) -> None:
    """
    Display a chord based on a tonic note.

    Args:
        tonic_note (str): The tonic note of the chord. Default is "C".

    Returns:
        None
    """
    table = Table()

    notes, degrees = _chord(tonic_note).values()

    for degree in degrees:
        table.add_column(degree)

    table.add_row(*notes)

    console.print(table)


@app.command()
def harmonic(
    tonic_note: str = Argument('C', help='Tonic Note'),
    scale_type: str = Argument('major', help='Scale Mode'),
) -> None:
    """
    Generates a harmonic progression based on the specified tonic note and
        scale mode.

    Args:
        tonic_note (str): The tonic note of the harmonic progression. Defaults
            to 'C'.
        scale_type (str): The scale mode of the harmonic progression. Defaults
            to 'major'.

    Returns:
        None
    """
    table = Table()

    chords, degrees = _harmonic(tonic_note, scale_type).values()

    for degree in degrees:
        table.add_column(degree)

    table.add_row(*chords)

    console.print(table)
