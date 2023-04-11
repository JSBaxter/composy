![00024-1949998484](https://user-images.githubusercontent.com/13378695/231194387-26a05a5f-f52a-4f81-ae79-1b5eefa92104.png)
# Composy
The composy music language is a simple text-based language designed for composing music using a concise and human-readable format. The language can be used to create melodies, chord progressions, and multi-track compositions.

## Syntax
### Tracks
A track represents a sequence of notes or chords to be played sequentially. Each track should begin with a track identifier followed by the note or chord elements. A track identifier starts with the letter "T" followed by the track number (e.g., T0, T1, T2).

Example:

```
T0
C4 0.5 D4 0.5 E4 0.5
```

### Notes
A note is represented by its name, accidental (if any), and octave. For example, C4 represents middle C, and D\#4 represents D sharp in the fourth octave.

Note names: A, B, C, D, E, F, G (case insensitive)

Accidentals: # (sharp) or b (flat)

Octave: An integer representing the octave number.

Example:

```
C4 D4 E4 F4 G4 A4 B4 C5
```

### Durations
To specify the duration of a note, add a space followed by a floating-point number after the note. The number represents the duration of the note in beats.

Example:

```
C4 0.5 D4 1.0 E4 2.0
```

### Rests
To insert a rest (a pause in the music), use the letter 'r' followed by the duration of the rest in beats.

Example:

```
C4 0.5 r0.5 D4 1.0 r1.0 E4 2.0
```
### Chords
A chord consists of a root note followed by a '-' and a shorthand for the chord type. Chord shorthands include:

M: Major
m: Minor
M7: Major 7
m7: Minor 7
7: Dominant 7
Example:

```
C4-M D4-m E4-M7 F4-m7 G4-7 A4-m7
```
### Custom Chords
To create custom chords, specify the root note followed by a series of intervals separated by spaces. Intervals should be preceded by a '+' sign and represent the number of semitones above the root note.

Example:

```
C4 +4 +7 D4 +3 +7
```
Example
Here's an example of a simple melody with two tracks:

```
T0
C4 0.5 D4 0.5 E4 0.5 F4 0.5 G4 0.5 A4 0.5 B4 0.5 C5 0.5
T1
C3-M 1.0 F3-M 1.0 G3-7 1.0 C3-M 1.0
```
This example includes a melody on track 0 and a chord progression on track 1.
