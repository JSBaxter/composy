from midiutil import MIDIFile
import pygame
import re

CHORD_SHORTHANDS = {
    "M": [0, 4, 7],  # Major chord
    "m": [0, 3, 7],  # Minor chord
    "7": [0, 4, 7, 10],  # Dominant 7th chord
    "M7": [0, 4, 7, 11],  # Major 7th chord
    "m7": [0, 3, 7, 10],  # Minor 7th chord
    "dim": [0, 3, 6],  # Diminished chord
    "aug": [0, 4, 8],  # Augmented chord
}

def play_midi_file(midi_file):
    pygame.mixer.init()
    pygame.mixer.music.load(midi_file)
    pygame.mixer.music.play()

    # Keep the script running while the music is playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def note_to_pitch(note):
    pitch_map = {
        "C": 0,
        "D": 2,
        "E": 4,
        "F": 5,
        "G": 7,
        "A": 9,
        "B": 11,
    }
    accidental_map = {
        "+": 1,
        "-": -1,
    }

    accidental = 0
    if note[1] in accidental_map:
        accidental = accidental_map[note[1]]
        octave = int(note[2])
    else:
        octave = int(note[1])

    return pitch_map[note[0]] + accidental + 12 * (octave + 1)

def note_to_pitch_and_shorthand(note_str, default_octave=4):
    note_parts = re.match(r"([A-Ga-g])([#b]?)(\d*)(\w*)", note_str)
    if note_parts:
        note, accidental, octave, shorthand = note_parts.groups()
        if not octave:
            octave = default_octave
        else:
            octave = int(octave)

        pitch = note_to_pitch(note.upper() + accidental + str(octave))
        return pitch, shorthand
    else:
        raise ValueError(f"Invalid note string: {note_str}")
    

def pseudocode_to_midi(pseudocode, output_file, tempo=120, instruments=None, default_duration=1, default_rest_duration=1, default_octave=4):
    if instruments is None:
        instruments = [0]  # Default to Acoustic Grand Piano
    
    num_tracks = max([int(line.split()[0][1]) for line in pseudocode.splitlines() if line.startswith("T")]) + 1
    midi = MIDIFile(num_tracks, adjust_origin=True)

    for track in range(num_tracks):
        midi.addTempo(track, 0, tempo)
        midi.addProgramChange(track, 0, 0, instruments[track] if track < len(instruments) else 0)

    track_times = [0] * num_tracks
    current_track = 0

    for line in pseudocode.splitlines():
        parts = line.split()
        if not parts:  # Skip empty lines
            continue

        if parts[0].startswith("T"):
            current_track = int(parts[0][1])
        else:
            idx = 0
            while idx < len(parts):
                part = parts[idx]

                if part.startswith("r"):
                    duration = float(parts[idx + 1]) if idx + 1 < len(parts) and not parts[idx + 1][0].isalpha() else default_rest_duration
                    track_times[current_track] += duration
                    idx += 2 if idx + 1 < len(parts) and not parts[idx + 1][0].isalpha() else 1
                elif part[0].isalpha():
                    root_pitch, shorthand = note_to_pitch_and_shorthand(part, default_octave=default_octave)
                    idx += 1
                    intervals = []

                    # Check for chord shorthand
                    if shorthand in CHORD_SHORTHANDS:
                        intervals = CHORD_SHORTHANDS[shorthand]
                    else:
                        while idx < len(parts) and parts[idx].startswith("+"):
                            intervals.append(int(parts[idx][1:]))
                            idx += 1

                    duration = float(parts[idx]) if idx < len(parts) and not parts[idx][0].isalpha() else default_duration
                    idx += 1 if idx < len(parts) and not parts[idx][0].isalpha() else 0

                    for interval in [0] + intervals:
                        pitch = root_pitch + interval
                        midi.addNote(current_track, 0, pitch, track_times[current_track], duration, 100)

                    track_times[current_track] += duration

    with open(output_file, "wb") as output:
        midi.writeFile(output)
    
    def save_and_play(pseudocode, midi_file):
        output_file = "pseudocode_melody_chords_multitrack_simplified.mid"
        instruments = [0, 32, 16]  # Use instrument number 0 (Acoustic Grand Piano) and 32 (Acoustic Bass) for the two tracks
        pseudocode_to_midi(pseudocode, output_file, instruments=instruments, default_duration=0.5, default_rest_duration=0.5)
        print(f"Music file '{output_file}' created.")
        play_midi_file(output_file)

