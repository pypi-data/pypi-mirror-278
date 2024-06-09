NOTES = "C C# D D# E F F# G G# A A# B".split()
SCALES = {"major": (0, 2, 4, 5, 7, 9, 11), "minor": (0, 2, 3, 5, 7, 8, 10)}


def scale(tonic_note: str, scale_type: str) -> dict[str, list[str]]:
    """
    Generate a scale based on a tonic and a scale type.

    Args:
        tonic_note (str): The musical note serving as the tonic of the scale.
        scale_type (str): The type of the scale, e.g., major or minor.

    Returns:
        A dictionary containing the notes of the scale and their corresponding degrees.

    Raises:
        ValueError: If the tonic note is invalid.
        KeyError: If the scale mode does not exist or has not been implemented.

    Examples:
        >>> scale("C", "major")
        {'notes': ['C', 'D', 'E', 'F', 'G', 'A', 'B'], 'degrees': ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']}

        >>> scale("A", "minor")
        {'notes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'], 'degrees': ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']}
    """
    tonic_note = tonic_note.upper()

    try:
        intervals = SCALES[scale_type]
        tonic_position = NOTES.index(tonic_note)
    except ValueError:
        raise ValueError(
            f"This musical note does not exist. Please use one of these: {NOTES}")
    except KeyError:
        raise KeyError(
            "This scale mode does not exist or has not been implemented. "
            f"Please use one of these: {list(SCALES.keys())}"
        )

    temp = []

    for interval in intervals:
        note = (tonic_position + interval) % 12
        temp.append(NOTES[note])

    return {"notes": temp, "degrees": ["I", "II", "III", "IV", "V", "VI", "VII"]}
