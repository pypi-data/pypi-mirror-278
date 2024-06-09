<div align="center">
  <img src="https://github.com/vhsenna/melodica-notes/blob/main/docs/assets/logo.png" width="150" alt="logo">
</div>

# Melodica Notes

[![Documentation](https://readthedocs.org/projects/melodica-notes/badge/?version=latest)](https://melodica-notes.readthedocs.io)
[![Pipeline](https://github.com/vhsenna/melodica-notes/actions/workflows/pipeline.yaml/badge.svg)](https://github.com/vhsenna/melodica-notes/actions/workflows/pipeline.yaml)
[![codecov](https://codecov.io/gh/vhsenna/melodica-notes/graph/badge.svg?token=75K7TA74BI)](https://codecov.io/gh/vhsenna/melodica-notes)
[![PyPI version](https://badge.fury.io/py/melodica-notes.svg)](https://badge.fury.io/py/melodica-notes)

Melodica Notes is a CLI tool to assist melodica players with musical scales, chords, and harmonics.

## How to Install

For the best experience, we recommend installing the project's CLI using `pipx`:

```bash
pipx install melodica-notes
```

However, this is just a recommendation. You can also install the project using your preferred package manager, such as `pip`:

```bash
pip install melodica-notes
```

## How to Use

The core of the application revolves around a command called `melodica-notes`.

Melodica Notes offers three subcommands: `scale`, `chord`, and `harmonic`.

## Scale

The `scale` subcommand followed by a musical note, displays the scale for that specific note.

By default, if called without any parameters, it returns the C major scale.

At present, Melodica Notes supports `major` and `minor` scale modes.

### Major Scale

```bash
melodica-notes scale C
```

```bash
┏━━━┳━━━━┳━━━━━┳━━━━┳━━━┳━━━━┳━━━━━┓
┃ I ┃ II ┃ III ┃ IV ┃ V ┃ VI ┃ VII ┃
┡━━━╇━━━━╇━━━━━╇━━━━╇━━━╇━━━━╇━━━━━┩
│ C │ D  │ E   │ F  │ G │ A  │ B   │
└───┴────┴─────┴────┴───┴────┴─────┘
```

### Minor Scale

```bash
melodica-notes scales F# minor
```

```bash
┏━━━━┳━━━━┳━━━━━┳━━━━┳━━━━┳━━━━┳━━━━━┓
┃ I  ┃ II ┃ III ┃ IV ┃ V  ┃ VI ┃ VII ┃
┡━━━━╇━━━━╇━━━━━╇━━━━╇━━━━╇━━━━╇━━━━━┩
│ F# │ G# │ A#  │ B  │ C# │ D  │ E   │
└────┴────┴─────┴────┴────┴────┴─────┘
```

## Chord

The `chord` subcommand operates by identifying the degrees associated within the major scale. When you input a chord, it determines the notes comprising that chord and their corresponding degrees within the scale.

Melodica Notes supports the following chord types: major (default), `m` (minor), `dim` (diminished), `+` (augmented) and `m+` (minor augmented). For example:

### Major Chord

```bash
melodica-notes chord A
```

```bash
┏━━━┳━━━━━┳━━━┓
┃ I ┃ III ┃ V ┃
┡━━━╇━━━━━╇━━━┩
│ A │ C#  │ E │
└───┴─────┴───┘
```

### Minor Chord

```bash
melodica-notes chord Em
```

```bash
┏━━━┳━━━━━━┳━━━┓
┃ I ┃ III- ┃ V ┃
┡━━━╇━━━━━━╇━━━┩
│ E │ G    │ B │
└───┴──────┴───┘
```

### Diminished Chord

```bash
melodica-notes chord Fdim
```

```bash
┏━━━┳━━━━━━┳━━━━┓
┃ I ┃ III- ┃ V- ┃
┡━━━╇━━━━━━╇━━━━┩
│ F │ G#   │ B  │
└───┴──────┴────┘
```

### Minor Augmented Chord

```bash
melodica-notes chord Gm+
```

```bash
┏━━━┳━━━━━━┳━━━━┓
┃ I ┃ III- ┃ V+ ┃
┡━━━╇━━━━━━╇━━━━┩
│ G │ A#   │ D# │
└───┴──────┴────┘
```

The `-` symbolizes a decrease of one semitone, indicating that to form the major chord, `F` would need to be `F#`.

The `+` symbolizes an increase of one semitone, suggesting that to form the major chord, `A#` would need to be `A`.

## Harmonic

The harmonic represent scales using chords.

You can access the harmonic using the `harmonic` subcommand followed by a musical note.

Melodica Notes supports `major` (default) and `minor` harmonic modes. For example:

### Harmonic Major

```bash
melodica-notes harmonic E
```

```bash
┏━━━┳━━━━━┳━━━━━┳━━━━┳━━━┳━━━━━┳━━━━━━━┓
┃ I ┃ ii  ┃ iii ┃ IV ┃ V ┃ vi  ┃ vii°  ┃
┡━━━╇━━━━━╇━━━━━╇━━━━╇━━━╇━━━━━╇━━━━━━━┩
│ E │ F#m │ G#m │ A  │ B │ C#m │ D#dim │
└───┴─────┴─────┴────┴───┴─────┴───────┘
```

### Harmonic Minor

```bash
melodica-notes harmonic F# minor
```

```bash
┏━━━━━┳━━━━━━━┳━━━━━┳━━━━┳━━━━━┳━━━━┳━━━━━┓
┃ i   ┃ ii°   ┃ III ┃ iv ┃ v   ┃ VI ┃ VII ┃
┡━━━━━╇━━━━━━━╇━━━━━╇━━━━╇━━━━━╇━━━━╇━━━━━┩
│ F#m │ G#dim │ A   │ Bm │ C#m │ D  │ E   │
└─────┴───────┴─────┴────┴─────┴────┴─────┘
```

## Additional Information

For additional options and help, use the `--help` flag with any command:

```bash
melodica-notes [COMMANDS] --help

╭─ Commands ─────────────────────────────────────────────────────╮
│ chord                                                          │
│ harmonic                                                       │
│ scale                                                          │
╰────────────────────────────────────────────────────────────────╯
```

This will provide you with detailed information on available commands and options.

Enjoy exploring different musical scales and chords effortlessly with Melodica Notes!

## How to Contribute

To contribute to the project, follow these steps and create a pull request.

### Clone the Repository

Clone the project repository to your local machine using the following command:

```bash
git clone https://github.com/vhsenna/melodica-notes.git
```

### Install Poetry

Ensure you have Poetry installed by running the following command:

```bash
pipx install poetry
```

### Install Dependencies

Navigate to the project directory and install the required dependencies with Poetry:

```bash
cd melodica-notes
poetry install
```

### Run the CLI

Execute the CLI by running the following command, replacing `[subcommand]` with the desired subcommand:

```bash
melodica-notes [subcommand]
```

### Run Tests

Run the tests to ensure everything is functioning correctly:

```bash
task test
```

### Run Documentation

Generate the project documentation using the following command:

```bash
task docs
```

## Upcoming Features

- [ ] Add support for [additional scales](https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes)
- [ ] Develop a feature for [harmonic progressions](https://en.wikipedia.org/wiki/Chord_progression)
- [ ] Add support for [suspended chords](https://en.wikipedia.org/wiki/Suspended_chord)
- [ ] Implement a feature for [tetrads](https://en.wikipedia.org/wiki/Tetrad_(music)), including:
  - [ ] 7th chords (dominant, major, minor)
  - [ ] 9th chords (dominant, major, minor)
- [ ] Develop a feature for [harmonic functions](https://en.wikipedia.org/wiki/Function_(music))
- [ ] Implement custom error classes for improved error handling and clarity
