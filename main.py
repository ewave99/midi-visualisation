import mido
#import pygame

def main ():
    #pygame.init ()
    #screen = pygame.display.set_mode ( [ 400, 400 ] )
    filename = "./IMSLP212667-WIMA.7b20-bwv542-a4-1.mid"

    notes = getNotes ( filename )

    for i in range ( 100 ):
        print ( next ( notes ) )

def getNotes ( filename ):
    midi = mido.MidiFile ( filename, clip=True )

    current = []
    time = 0

    for message in midi:
        if hasattr ( message, "note" ):
            time += message.time

            for note in current:
                note [ 2 ] += message.time

            if message.type == "note_on":
                current.append ( [ message.note, time, 0 ] )
            elif message.type == "note_off":
                i = 0
                while i < len ( current ):
                    if current [ i ] [ 0 ] == message.note:
                        yield current [ i ]
                        
                        current.pop ( i )
                    else:
                        i += 1

    yield None

#def calculateMidiFileDuration ( midi: mido.MidiFile ):
#    return max ( [ calculateTrackDuration ( track ) for track in midi.tracks ] )
#
#def calculateTrackDuration ( track: mido.MidiTrack ):
#    return sum ( [ msg.time for msg in track ] )

if __name__ == "__main__":
    main ()
