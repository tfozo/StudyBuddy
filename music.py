import board
import simpleio
import gc
# Define the melody and durations, adding the frequency values for each note and 0 for REST
memories_melody = [
    0, 659, 587, 523, 494, 440, 392, 440, 494,  # E5, D5, C5, B4, etc.
    784, 659, 698, 784, 659, 698, 784, 0,       # G5, E5, F5, G5, etc.
    659, 523, 587, 659, 523, 587, 659, 523, 587, 659, 587, 523,
    440, 440, 0, 440, 440, 392, 440, 392, 392, 0, 392,
    440, 440, 440, 440, 523, 494,
    784, 659, 698, 784, 659, 698, 784,
    659, 523, 587, 659, 523, 587, 659, 523, 587, 659, 587, 523,
    440, 440, 0, 440, 440, 392, 440, 392, 392, 0, 392, 392,
    440, 440, 440, 0, 440, 523, 494, 494, 494, 494, 523, 0,
    0
]

memories_durations = [
    4, 2, 2, 2, 2, 2, 2, 2, 4,
    4, 8, 8, 4, 8, 8, 2, 2,
    4, 8, 8, 4, 8, 8, 4, 8, 8, 4, 8, 8,
    4, 8, 8, 4, 8, 8, 8, 8, 2, 8, 8,
    8, 8, 4, 4, 4, 1,
    4, 8, 8, 4, 8, 8, 1,
    4, 8, 8, 4, 8, 8, 4, 8, 8, 4, 8, 8,
    4, 8, 8, 4, 8, 8, 8, 8, 4, 4, 8, 8,
    8, 8, 8, 8, 4, 4, 8, 8, 4, 4, 8, 8,
    1
]


#HBD

panther_melody = [
    0, 0, 0, 311,  # D#4, E4
    330, 0, 370, 392, 0, 311,  # F#4, G4
    330, 370, 392, 523, 494, 330, 392, 494,  # C5, B4, E4, G4, B4
    466, 440, 392, 330, 294,  # A#4, A4, G4, E4, D4
    330, 0, 0, 311,
    
    330, 0, 370, 392, 0, 311,
    330, 370, 392, 523, 494, 392, 494, 659,  # E5, D#5
    587,  # D5
    0, 0, 311, 
    330, 0, 370, 392, 0, 311,
    330, 370, 392, 523, 494, 330, 392, 494,
    
    466, 440, 392, 330, 294,
    330, 0,
    0, 659, 587, 494, 440, 392, 330,  # E5, D5, B4, A4, G4, E4
    466, 440, 466, 440, 466, 440, 466, 440,
    392, 330, 294, 330, 330, 330
]

# Define the duration of each note in milliseconds:
panther_durations = [
    2, 4, 8, 8,
    4, 8, 8, 4, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8,
    2, 16, 16, 16, 16,
    2, 4, 8, 4,
    
    4, 8, 8, 4, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8,
    1,
    2, 4, 8, 8,
    4, 8, 8, 4, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8,
    
    2, 16, 16, 16, 16,
    4, 4,
    4, 8, 8, 8, 8, 8, 8,
    16, 8, 16, 8, 16, 8, 16, 8,
    16, 16, 16, 16, 16, 2
]


#shape of you

shape_melody = [
    277, 330, 277, 277, 330, 277, 277, 330, 277, 311, 277, 277, 330, 277, 247, 277, 330,
    277, 277, 330, 277, 311, 277, 330, 247, 330, 330, 330, 330, 330, 330, 330, 330, 330,
    330, 330, 330, 330, 370, 415, 415, 415, 330, 370, 494, 415, 415, 415, 415, 415, 370,
    370, 370, 415, 370, 370, 370, 370, 370, 415, 370, 330, 277, 277, 415, 415, 415, 415,
    415, 415, 415, 415, 415, 415, 415, 494, 415, 415, 370, 370, 330, 415, 370, 330, 330,
    330, 494, 415, 415, 415, 370, 370, 370, 370, 370, 370, 370, 370, 330, 277, 277, 277,
    277, 277, 277, 208, 247, 277, 277, 370, 415, 330, 370, 247, 330, 370, 415, 370, 330,
    277, 330, 415, 370, 330, 370, 277, 494, 415, 415, 370, 370, 330, 277, 330, 370, 415,
    370, 330, 370, 330, 277, 277, 247, 277, 277, 370, 415, 330, 370, 370, 247, 370, 415,
    370, 330, 277, 330, 415, 370, 330, 370, 277, 494, 415, 415, 370, 370, 330, 277, 494,
    415, 415, 370, 370, 330, 277, 277, 208, 247, 330, 370, 415, 370, 330, 330, 330, 370,
    370, 330, 370, 415, 370, 330, 330, 330, 370, 277, 330, 370, 415, 277, 330, 330, 370,
    370, 330, 370, 415, 277, 330, 
]

shape_duration = [2,2,4,2,2,4,2,2,4,2,2,2,2,2,2,2,2,4,2,2,4,2,2,2,2,8,8,4,4,8,8,8,8,8,8,8,2,8,8,4,2,8,8,4,8,8,8,4,4,8,8,8,8,8,4,8,4,8,8,8,8,4,2,8,8,8,8,4,8,8,8,8,8,8,2,8,4,8,8,8,8,8,2,4,8,8,2,4,8,8,8,8,8,8,2,8,8,4,4,4,8,8,2,4,4,2,4,2,2,4,8,8,8,2,2,8,4,8,4,4,4,4,8,8,8,8,2,8,8,4,8,8,4,2,8,4,8,4,4,4,4,2,2,2,2,4,8,8,8,2,2,2,4,8,4,4,4,4,8,8,8,8,2,8,8,4,8,8,4,2,8,8,4,8,8,4,2,2,4,2,8,8,4,8,8,4,8,8,2,8,8,4,8,8,4,8,8,2,8,8,4,4,4,8,8,2,8,8,4,8,8,8,4,8,2,4,4,8,8,4,4,8,2,8,8,4,4,4,8,8,4,8,8,8,8,8,8,4,4,4,4,8,2,8,8,4,8,8,8,4,8,4,4,4,4,4,4,4,2,8,8,4,8,8,8,4,8,4,4,4,4,4,4,4,2,8,8,4,8,8,8,4,8,4,4,4,4,4,4,4,2,8,8,4,8,8,8,4,8,4,8,8,8,8,8,8,4,4,4,4,2]

#tokyo drift
tokyo_melody = [
    415, 0, 415, 0, 415, 0, 415, 0,
    415, 494, 554,
    415, 0, 415, 0,
    415, 494, 554,
    415, 0, 415, 0,
    415, 494, 554,
    415, 0, 415, 0,
    415, 494, 554,
    698, 0, 698, 0,
    831, 740, 698,
    415, 0, 415, 0,
    831, 740, 698,
    415, 0, 415, 0,
    415, 494, 554,
    415, 0, 415, 0,
    415, 494, 554,
    415, 0, 415, 0,
    0
]

# Durations of each note in the melody
tokyo_durations = [
    4, 4, 4, 4, 4, 4, 4, 4,
    3, 3, 4,
    4, 4, 4, 4,
    3, 3, 4,
    4, 4, 4, 4,
    3, 3, 4,
    4, 4, 4, 4,
    3, 3, 4,
    4, 4, 4, 4,
    3, 3, 4,
    4, 4, 4, 4,
    3, 3, 4,
    4, 4, 4, 4,
    3, 3, 4,
    4, 4, 4, 4,
    3, 3, 4,
    4, 4, 4, 4,
    1
]

#imagine_dragons_enemy

# Melody list directly using frequency values for notes
imagine_dragons_melody = [
    494, 0, 370, 370, 494, 370, 330, 0, 247,
    294, 294, 294, 294, 247, 247, 294, 294, 294, 294, 247, 247,
    277, 277, 277, 277, 233, 233, 277, 277, 277, 277, 233, 247,
    294, 294, 294, 294, 247, 247, 294, 294, 294, 294, 247, 247,
    277, 277, 277, 277, 233, 233, 277, 277, 277, 277, 233,
    494, 440, 392, 294, 370, 330, 494,
    494, 440, 392, 294, 370, 466,
    0, 330, 370, 330, 294, 247,
    294, 330, 294, 330, 294, 330, 294, 330, 294, 330, 494,
    0, 330, 370, 330, 294, 247,
    294, 330, 294, 330, 294, 330, 494, 0, 247, 247, 247,
    294, 277, 247, 185, 165, 185, 370, 494, 370, 330,
    0,
]

# Durations list
imagine_dragons_durations = [
    4, 2, 4, 8, 4, 8, 4, 2, 8,
    4, 4, 8, 8, 2, 8, 4, 4, 8, 8, 2, 8,
    4, 4, 8, 8, 2, 8, 4, 4, 8, 8, 2, 8,
    4, 4, 8, 8, 2, 8, 4, 4, 8, 8, 2, 8,
    4, 4, 8, 8, 2, 8, 4, 4, 8, 8, 2,
    2, 2, 2, 4, 1, 1, 8,
    2, 2, 2, 4, 1, 1,
    2, 2, 8, 8, 8, 2,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2,
    2, 2, 8, 8, 8, 2,
    8, 8, 8, 8, 8, 8, 2, 2, 8, 8, 8,
    2, 2, 2, 8, 4, 4, 8, 4, 8, 2,
    1,
]

#G.O.T
# Melody list directly using frequency values for notes
got_melody = [
    330, 349, 392, 659, 523, 587, 523, 523, 494, 494, 294,
    330, 349, 587, 494, 523, 494, 440, 392, 392, 330, 349,
    392, 523, 587, 659, 587, 523, 440, 587, 659, 698, 659,
    587, 392, 698, 659, 587, 523, 523, 0, 523, 0, 523, 659,
    523, 587, 0, 587, 587, 587, 0, 587, 698, 587, 659, 0, 659,
    659, 659, 0, 659, 784, 659, 698, 0, 698, 698, 659, 587, 392,
    494, 523, 523, 0
]

# Durations list
got_durations = [
    8, 8, 4, 4, 4, 8, 8, 4, 4, 4, 8, 8, 4, 4, 4, 8, 8, 4, 4, 4, 8, 8, 4, 8, 8, 4, 8, 8, 4,
    8, 8, 4, 8, 8, 4, 4, 4, 4, 2, 4, 4, 4, 8, 8, 4, 4, 4, 8, 8, 2, 4, 8, 8, 4, 4, 4, 8, 8,
    2, 4, 8, 8, 4, 4, 4, 8, 8, 4, 8, 8, 2, 2, 2, 4, 4
]


#lion_sleeps_tonight
# Melody list
lion_sleeps_melody = [
    349, 392, 440, 392, 440,
    466, 440, 392, 349, 392,
    440, 262, 262, 262, 262,
    262,
    
    349, 392, 440, 392, 440,
    466, 440, 392, 349, 392,
    440, 262, 262, 262, 262,
    262, 0, 440,
    
    440, 440, 440, 440, 440, 440, 440, 440,
    466, 466, 466, 466, 466, 466, 466, 466,
    440, 440, 440, 440, 440, 440, 440, 440,
    392, 392, 392, 392, 392, 392, 392, 392,
    
    440, 440, 440, 440, 440, 440, 440, 440,
    466, 466, 466, 466, 466, 466, 466, 466,
    440, 440, 440, 440, 440, 440, 440, 440,
    392, 392, 392, 392, 392, 392, 392, 392,
    
    349, 392, 440, 392, 440,
    466, 440, 392, 349, 392,
    440, 392, 349, 440,
    392, 523, 440, 392, 440,
    466, 440, 392, 349, 392,
    440, 392, 349, 440,
    392, 523, 440, 392, 440,
    
    466,
    466, 466, 466, 466,
    440, 262, 262, 262, 262,
    262
]

# Durations list
lion_sleeps_durations = [
    4, 4, 8, 4, 8,
    4, 4, 8, 4, 8,
    4, 8, 4, 8, 4,
    1,
    
    4, 4, 8, 4, 8,
    4, 4, 8, 4, 8,
    4, 8, 4, 8, 4,
    2, 8, 16,
    
    8, 16, 8, 16, 8, 16, 8, 16,
    8, 16, 8, 16, 8, 16, 8, 16,
    8, 16, 8, 16, 8, 16, 8, 16,
    8, 16, 8, 16, 8, 16, 8, 16,
    
    8, 16, 8, 16, 8, 16, 8, 16,
    8, 16, 8, 16, 8, 16, 8, 16,
    8, 16, 8, 16, 8, 16, 8, 16,
    8, 16, 8, 16, 8, 16, 8, 16,
    
    4, 4, 8, 4, 8,
    4, 4, 8, 4, 8,
    4, 4, 4, 4,
    1,
    4, 4, 8, 4, 8,
    4, 4, 8, 4, 8,
    4, 4, 4, 4,
    1,
    
    1,
    4, 8, 8, 2,
    4, 8, 4, 8, 4,
    1,
    
    4, 8, 8, 8, 8, 8, 8, 
    1,
    4, 8, 8, 8, 8, 8, 8, 
    1,
    
    4, 4, 8, 4, 8,
    4, 4, 8, 4, 8,
    4, 8, 4, 8, 4,
    1, 
    
    4, 4, 8, 4, 8,
    4, 4, 8, 4, 8,
    4, 4, 4, 4,
    1,
    4, 4, 8, 4, 8,
    4, 4, 8, 4, 8,
    4, 4, 4, 4,
    1,
    
    1,
    4, 8, 8, 2,
    4, 8, 4, 8, 4,
    1,
    
    4, 8, 8, 8, 8, 8, 8, 
    1,
    4, 8, 8, 8, 8, 8, 8, 
    1,
    
    4, 4, 8, 4, 8,
    4, 4, 8, 4, 8,
    4, 8, 4, 8, 4,
    1
]

#the simpsons

# Melody list
simpsons_melody = [
    262, 330, 370, 0, 440,
    392, 330, 262, 220,
    185, 185, 185, 196, 0,
    185, 185, 185, 196, 208,
    247, 0
]

# Durations list
simpsons_durations = [
    2, 4, 4, 32, 8,
    2, 4, 4, 8,
    8, 8, 8, 4, 2,
    8, 8, 8, 4, 2,
    2, 2
]


#nokia
nokia_melody = [
    659, 587, 370, 415, 554, 494, 294, 330, 494, 440, 277, 330, 440
]

nokia_durations = [
    8, 8, 4, 4,
    8, 8, 4, 4,
    8, 8, 4, 4,
    2
]

#pac
pac_melody = [
    494, 988, 740, 622,
    988, 740, 622, 523,
    1047, 1568, 1319, 1047, 1568, 1319,
    494, 988, 740, 622, 988,
    740, 622, 622, 659, 698,
    698, 740, 784, 784, 831, 880, 988
]

pac_durations = [
    16, 16, 16, 16,
    32, 16, 8, 16,
    16, 16, 16, 32, 16, 8,
    16, 16, 16, 16, 32,
    16, 8, 32, 32, 32,
    32, 32, 32, 32, 32, 16, 8
]


#HELLO

hello_melody = [494, 330, 440, 440, 392]
hello_durations = [4, 8, 4, 4, 1]

#study

study_melody = [784, 659, 523, 392, 494]
study_durations = [4, 8, 4, 8, 4]  # Simplistic rhythm, adjust as you see fit

#break

break_melody = [587, 494, 659, 440, 784]
break_durations = [8, 8, 4, 4, 8]  # Feel free to adjust these values

buzzer = board.GP22

def play_melody(melody, durations, duration_scale=1.0, pause_scale=1.30):
    gc.collect()
    for note, duration in zip(melody, durations):
        if note > 0:
            simpleio.tone(buzzer, note, (1.0 / duration) * duration_scale)
        else:
            simpleio.tone(buzzer, 0, ((1.0 / duration) * pause_scale))
    gc.collect()




NOTE_G4 = 392
NOTE_C5 = 523
NOTE_G3 = 196
NOTE_C4 = 262

def play_connected():
    simpleio.tone(buzzer, NOTE_G4, duration=0.1)
    simpleio.tone(buzzer, NOTE_C5, duration=0.1)

def play_failure():
    simpleio.tone(buzzer, NOTE_G3, duration=0.1)
    simpleio.tone(buzzer, NOTE_C4, duration=0.3)


# Define functions for each melody to play them directly.
def play_nokia():
    play_melody(nokia_melody, nokia_durations, duration_scale=1.0, pause_scale=1.30)
    gc.collect()


def play_memories():
    play_melody(memories_melody, memories_durations, duration_scale=1.0, pause_scale=1.30)
    gc.collect()

def play_shape_of_you():
    play_melody(shape_melody, shape_duration, duration_scale=1.0, pause_scale=1.30)
    gc.collect()
    
def play_tokyo():
    play_melody(tokyo_melody, tokyo_durations, duration_scale=1.0, pause_scale=1.30)
    gc.collect()
    
def play_imagine_dragons_enemy():
    play_melody(imagine_dragons_melody, imagine_dragons_durations, duration_scale=1.0, pause_scale=1.30)
    gc.collect()
    
def play_got():
    play_melody(got_melody, got_durations, duration_scale=1.0, pause_scale=1.30)
    gc.collect()
    
def play_lion_sleeps_tonight():
    play_melody(lion_sleeps_melody, lion_sleeps_durations, duration_scale=1.0, pause_scale=1.30)
    gc.collect()
    
def play_simpsons():
    play_melody(simpsons_melody, simpsons_durations, duration_scale=1.0, pause_scale=1.30)
    gc.collect()
    
def play_study():
    play_melody(study_melody, study_durations, duration_scale=2, pause_scale=1.30)
    gc.collect()
    
def play_break():
    play_melody(break_melody, break_durations, duration_scale=2, pause_scale=1.30)
    gc.collect()
    
def play_pac():
    play_melody(pac_melody, pac_durations, duration_scale=1.0, pause_scale=1.30)
    gc.collect()
    
def play_hello():
    play_melody(hello_melody, hello_durations, duration_scale=1.0, pause_scale=1.30)
    gc.collect()


gc.collect()
#play_pac()
#play_break()
#play_study()
#play_connected()
#play_failure()
#play_melody(nokia_melody, nokia_durations, duration_scale=1.0, pause_scale=1.30)   
#play_melody(memories_melody, memories_durations, duration_scale=1.0, pause_scale=1.30)
#play_melody(shape_melody, shape_duration, duration_scale=1.0, pause_scale=1.30)
#play_melody(imagine_dragons_melody, imagine_dragons_durations, duration_scale=1.0, pause_scale=1.30)
#play_melody(got_melody, got_durations, duration_scale=1.0, pause_scale=1.30)
#play_melody(lion_sleeps_melody, lion_sleeps_durations, duration_scale=1.0, pause_scale=1.30)
#play_melody(simpsons_melody, simpsons_durations, duration_scale=1.0, pause_scale=1.30)
