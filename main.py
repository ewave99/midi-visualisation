import mido
import pygame

def main ():
    filename = "./IMSLP212667-WIMA.7b20-bwv542-a4-1.mid"
    notes = list ( getNotes ( filename ) )

    note_values_played = { note [ 0 ] for note in notes }

    min_note = min ( note_values_played )
    max_note = max ( note_values_played )
    note_range = max_note - min_note

    pygame.init ()

    channel_colours = [
        pygame.Color ( 'blue' ),
        pygame.Color ( 'brown3' ),
        pygame.Color ( 'darkcyan' ),
        pygame.Color ( 'chocolate1' ),
        pygame.Color ( 'cyan' )
        ]

    width = 400
    height = 400

    screen = pygame.display.set_mode ( [ width, height ] )

    time_magnify = 50
    note_thickness = height / note_range

    time_offset = notes [ 0 ] [ 1 ]
    y_offset = 0

    speed = 0.003

    num_colours = len ( channel_colours )

    running = True
    while running:
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                running = False

        screen.fill ( ( 255, 255, 255 ) )

        for note in notes:
            pygame.draw.rect ( screen,
                    channel_colours [ note [ 3 ] % num_colours ],
                    ( ( note [ 1 ] - time_offset ) * time_magnify,
                        height - ( note [ 0 ] - min_note ) * note_thickness + y_offset,
                        note [ 2 ] * time_magnify,
                        note_thickness )
                    )

        pygame.display.flip ()

        time_offset += speed


def getNotes ( filename ):
    midi = mido.MidiFile ( filename, clip=True )

    current = []
    time = 0

    for message in midi:
        if time == 0:
            print ( message )
        if hasattr ( message, "note" ):
            time += message.time

            for note in current:
                note [ 2 ] += message.time

            if message.type == "note_on":
                current.append ( [ message.note, time, 0, message.channel ] )
            elif message.type == "note_off":
                i = 0
                while i < len ( current ):
                    if current [ i ] [ 0 ] == message.note:
                        yield current [ i ]
                        
                        current.pop ( i )
                    else:
                        i += 1

#def calculateMidiFileDuration ( midi: mido.MidiFile ):
#    return max ( [ calculateTrackDuration ( track ) for track in midi.tracks ] )
#
#def calculateTrackDuration ( track: mido.MidiTrack ):
#    return sum ( [ msg.time for msg in track ] )

if __name__ == "__main__":
    main ()
