import pytest
from mido import MidiFile
import composy
import os
import tempfile
import textwrap
import pathlib

def test_parse_line_default_duration():
    assert composy.parse_line('C4') == ('note', 60, 1.0)
    assert composy.parse_line('r') == ('rest', 1.0)
    assert composy.parse_line('C4-M') == ('chord', [60, 64, 67], 1.0)
    assert composy.parse_line('C4 +4 +7') == ('custom_chord', [60, 64, 67], 1.0)

def test_parse_line_explicit_duration():
    assert composy.parse_line('C4 0.5') == ('note', 60, 0.5)
    assert composy.parse_line('r 1.5') == ('rest', 1.5)
    assert composy.parse_line('C4-M 2.0') == ('chord', [60, 64, 67], 2.0)
    assert composy.parse_line('C4 +4 +7 0.75') == ('custom_chord', [60, 64, 67], 0.75)

def test_play_midi_file():
    # Create a temporary MIDI file for testing
    
    with tempfile.TemporaryDirectory() as tmpdirname:        
        pseudocode = textwrap.dedent('''
            T0
            C4 0.5
            D4 0.5
            E4 0.5
            F4 0.5 
            G4 0.5 
            A4 0.5 
            B4 0.5 
            C5 0.5
            T1
            C3-M 1.0 
            F3-M 1.0 
            G3-7 1.0 
            C3-M 1.0
        ''')
        
        test_file = pathlib.Path(tmpdirname, 'output.mid')
        composy.pseudocode_to_midi(pseudocode, pathlib.Path(tmpdirname, 'output.mid'))

        try:
            # Call the play_midi_file function and check if it raises an exception
            try:
                composy.play_midi_file(test_file)
            except Exception as e:
                pytest.fail(f"Unexpected exception: {e}")

        except ImportError:
            # pygame.mixer not available, skip the test
            pytest.skip("pygame.mixer not available for testing")

def test_note_to_midi():
    assert composy.note_to_midi('C4') == 60
    assert composy.note_to_midi('A0') == 21
    assert composy.note_to_midi('B4') == 71
    assert composy.note_to_midi('C#4') == 61
    assert composy.note_to_midi('Db4') == 61

def test_chord_to_notes():
    assert composy.chord_to_notes('C4', 'M') == [60, 64, 67]
    assert composy.chord_to_notes('D4', 'm') == [62, 65, 69]
    assert composy.chord_to_notes('G4', 'aug') == [67, 71, 75]
    assert composy.chord_to_notes('A4', 'dim') == [69, 72, 75]
    assert composy.chord_to_notes('F4', 'sus2') == [65, 67, 72]
    assert composy.chord_to_notes('B4', 'sus4') == [71, 76, 78]
    assert composy.chord_to_notes('E4', '6') == [64, 68, 71, 73]

def test_parse_line():
    assert composy.parse_line('C4 0.5') == ('note', 60, 0.5)
    assert composy.parse_line('r 1.0') == ('rest', 1.0)
    assert composy.parse_line('C4-M 1.0') == ('chord', [60, 64, 67], 1.0)
    assert composy.parse_line('C4 +4 +7 1.0') == ('custom_chord', [60, 64, 67], 1.0)

def test_parse_pseudocode():
    pseudocode = '''
T0
C4 0.5
T1
r 1.0
C4-M 1.0
'''
    parsed = composy.parse_pseudocode(pseudocode)
    assert parsed == {0: [('note', 60, 0.5)], 1: [('rest', 1.0), ('chord', [60, 64, 67], 1.0)]}

def test_create_midi_file():
    tracks = {0: [('note', 60, 0.5)]}
    midi = composy.create_midi_file(tracks)
    assert isinstance(midi, MidiFile)
    assert len(midi.tracks) == 1

def test_pseudocode_to_midi(tmp_path):
    pseudocode = 'T0\nC4 0.5\n'
    output_file = tmp_path / 'output.mid'
    composy.pseudocode_to_midi(pseudocode, str(output_file))
    assert output_file.exists()

if __name__ == '__main__':
    pytest.main(['-v', 'test_composy.py'])