from mido import Message, MidiFile, MidiTrack, bpm2tempo, MetaMessage
import pygame
import re

NOTE_NAMES = {'A', 'B', 'C', 'D', 'E', 'F', 'G'}
ACCIDENTALS = {'#': 1, 'b': -1}
CHORDS = {
    'M': [4, 7],
    'm': [3, 7],
    'M7': [4, 7, 11],
    'm7': [3, 7, 10],
    '7': [4, 7, 10],
}

def play_midi_file(midi_file):
    pygame.mixer.init()
    pygame.mixer.music.load(midi_file)
    pygame.mixer.music.play()

    # Keep the script running while the music is playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def chord_shorthand_intervals(shorthand):
    intervals_dict = {
        "M": [0, 4, 7],
        "m": [0, 3, 7],
        '7': [0, 4, 7, 10],
        "M7": [0, 4, 7, 11],
        "m7": [0, 3, 7, 10],
        "dim": [0, 3, 6],
        "aug": [0, 4, 8],
        "sus2": [0, 2, 7],
        "sus4": [0, 5, 7],
        "6": [0, 4, 7, 9],
        "m6": [0, 3, 7, 9],
    }

    if shorthand in intervals_dict:
        return intervals_dict[shorthand]
    else:
        raise ValueError(f"Invalid shorthand: {shorthand}")
    
def note_to_midi(note):
    pitch_class_lookup = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    pitch_class, accidental, octave = re.match(r'([A-Ga-g])([#b]?)(\d)', note).groups()
    pitch_class_number = pitch_class_lookup[pitch_class.upper()]
    octave_number = int(octave)

    if accidental == '#':
        pitch_class_number += 1
    elif accidental == 'b':
        pitch_class_number -= 1

    return 12 * (octave_number + 1) + pitch_class_number

def chord_to_notes(root, shorthand=None):
    if shorthand is None:
        intervals = [0]
    else:
        intervals = chord_shorthand_intervals(shorthand)
    return [note_to_midi(root) + interval for interval in intervals]



def parse_line(line):
    line = line.strip()
    default_duration = 1.0

    note_match = re.match(r'^([A-Ga-g][#b]?\d)(?: (\d+\.\d+))?$', line)
    if note_match:
        duration = float(note_match.group(2)) if note_match.group(2) else default_duration
        return ('note', note_to_midi(note_match.group(1)), duration)

    rest_match = re.match(r'^r(?: (\d+\.\d+))?$', line)
    if rest_match:
        duration = float(rest_match.group(1)) if rest_match.group(1) else default_duration
        return ('rest', duration)

    chord_match = re.match(r'^([A-Ga-g][#b]?\d)-([MmM7m77])(?: (\d+\.\d+))?$', line)
    if chord_match:
        duration = float(chord_match.group(3)) if chord_match.group(3) else default_duration
        return ('chord', chord_to_notes(chord_match.group(1), chord_match.group(2)), duration)

    custom_chord_match = re.match(r'^([A-Ga-g][#b]?\d) (\+\d+)(?: (\+\d+))*(?: (\d+\.\d+))?$', line)
    if custom_chord_match:
        base_note = note_to_midi(custom_chord_match.group(1))
        intervals = [int(i[1:]) for i in custom_chord_match.groups()[1:-1] if i is not None]
        notes = [base_note] + [base_note + interval for interval in intervals]
        duration = float(custom_chord_match.group(4)) if custom_chord_match.group(4) else default_duration
        return ('custom_chord', notes, duration)


    raise ValueError(f"Invalid line: {line}")

def parse_pseudocode(pseudocode):
    lines = pseudocode.strip().split('\n')
    tracks = {}
    current_track = None
    for line in lines:
        if line.startswith('T'):
            current_track = int(line[1:])
            tracks[current_track] = []
        else:
            tracks[current_track].append(parse_line(line))

    return tracks

def create_midi_file(tracks, tempo=120, ticks_per_beat=480):
    midi = MidiFile(ticks_per_beat=ticks_per_beat)
    for track_id, track_data in tracks.items():
        midi_track = MidiTrack()
        midi.tracks.append(midi_track)
        midi_track.append(MetaMessage('set_tempo', tempo=bpm2tempo(tempo)))

        for event in track_data:
            if event[0] == 'rest':
                midi_track.append(Message('note_on', note=0, velocity=0, time=int(ticks_per_beat * event[1])))
            elif event[0] == 'note':
                midi_track.append(Message('note_on', note=event[1], velocity=64, time=0))
                midi_track.append(Message('note_off', note=event[1], velocity=64, time=int(ticks_per_beat * event[2])))
            elif event[0] == 'chord' or event[0] == 'custom_chord':
                for note in event[1]:
                    midi_track.append(Message('note_on', note=note, velocity=64, time=0))
                for note in event[1]:
                    midi_track.append(Message('note_off', note=note, velocity=64, time=int(ticks_per_beat * event[2])))
    return midi
    
def pseudocode_to_midi(pseudocode, output_file, tempo=120, ticks_per_beat=480):
    tracks = parse_pseudocode(pseudocode)
    midi = create_midi_file(tracks, tempo=tempo, ticks_per_beat=ticks_per_beat)
    midi.save(output_file)

if __name__ == '__main__':
    pseudocode = '''
    T0
    C4 0.5 D4 0.5 E4 0.5 F4 0.5 G4 0.5 A4 0.5 B4 0.5 C5 0.5
    T1
    C3-M 1.0 F3-M 1.0 G3-7 1.0 C3-M 1.0
    '''

    pseudocode_to_midi(pseudocode, 'output.mid')
