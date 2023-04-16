<p align="center">
  <img src="https://user-images.githubusercontent.com/13378695/231199878-b985e814-5c75-40bc-bb63-718596a46205.png"  width="300" height="300">
</p>

# Composy

Composy is a simple and intuitive text-based music composition language designed to quickly create and edit melodies, chords, and rhythms using a familiar syntax. The language enables composers to specify notes, rests, chords, and custom chords along with their durations. Composers can also create multi-track compositions for more complex arrangements.

## Features

- Text-based composition language
- Simple and easy-to-learn syntax
- Support for notes, rests, chords, and custom chords
- Adjustable note durations
- Multi-track compositions

## Syntax

### Notes

To add a note, specify the note name followed by the octave number and duration. For example, to add a C4 note with a duration of 0.5:

```
C4 0.5
```

### Rests

To add a rest, use the `r` keyword followed by the duration. For example, to add a rest with a duration of 1.0:

```
r 1.0
```

### Chords

To add a chord, specify the root note followed by the chord shorthand and duration. For example, to add a C4 major chord with a duration of 1.0:

```
C4-M 1.0
```


Supported chord shorthands:

- M: Major
- m: Minor
- 7: Dominant 7th
- M7: Major 7th
- m7: Minor 7th
- dim: Diminished
- aug: Augmented
- sus2: Suspended 2nd
- sus4: Suspended 4th
- 6: Major 6th

### Custom Chords

To add a custom chord, specify the root note followed by the desired intervals and duration. For example, to add a C4 chord with intervals of 4 and 7 and a duration of 1.0:

```
C4 +4 +7 1.0
```

### Tracks

To create multi-track compositions, use the `T` keyword followed by the track number:

T0
C4 0.5
T1
r 1.0
C4-M 1.0

In this example, track 0 contains a single C4 note with a duration of 0.5, and track 1 contains a rest followed by a C4 major chord with a duration of 1.0.

## Getting Started

1. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

2. Create a text file with your composition using the Composy syntax.

3. Use the provided parser and player to convert your composition to a MIDI file and play it.

```python
import composy

# Parse your composition file
composition = composy.parse_file('your_composition_file.txt')

# Save the composition as a MIDI file
composy.save_midi(composition, 'your_midi_output.mid')

# Play the MIDI file
composy.play_midi_file('your_midi_output.mid')
```

Now you can create, edit, and play your compositions using Composy's intuitive syntax!