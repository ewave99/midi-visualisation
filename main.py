from midi import readCsvFile
import pygame
from pygame.locals import *

def main ():
    filename = "./great_fugue.csv"

    # get notes from CSV file
    notes = readCsvFile ( filename )

    # get metadata from CSV file
    max_note, min_note, duration, num_channels = next ( notes )

    # get note range
    note_range = max_note - min_note

    # initialise pygame
    pygame.init ()

    # colours used to differentiate between channels. If there are more
    # channels than colours then colours are reused.
    channel_colours = [
        pygame.Color ( 'blue' ),
        pygame.Color ( 'brown3' ),
        pygame.Color ( 'darkcyan' ),
        pygame.Color ( 'chocolate1' ),
        pygame.Color ( 'cyan' )
        ]

    # width and height of window
    width = 400
    height = 400

    # how much to magnify the time, in pixels per second
    tick_magnify = 50
    # how much 'time' is visible on the screen - i.e. the time duration
    # that the width of the screen represents
    tick_period_on_screen = int ( width / tick_magnify )

    # how thick to draw each note
    note_thickness = height / note_range

    # how far we are through the track/piece/file timewise
    tick_offset = 0

    # beats per minute
    #bpm = 120

    speed = 0.001

    num_colours = len ( channel_colours )

    channels_visible = [ True for i in range ( 9 ) ]

    notes_loaded = []

    screen = pygame.display.set_mode ( [ width, height ] )

    current = next ( notes )

    print ( tick_period_on_screen )

    running = True
    while tick_offset < duration and running == True:
        for event in pygame.event.get ():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if K_0 <= event.key <= K_9:
                    channel = event.key - K_0
                    channels_visible [ channel ] = not channels_visible [ channel ]
                elif event.key == K_ESCAPE:
                    running = False

        if not running:
            break

        if int ( tick_offset ) % tick_period_on_screen == 0:
            # unload notes not on screen
            while notes_loaded and notes_loaded [ 0 ] [ 1 ] < tick_offset - tick_period_on_screen:
                notes_loaded.pop ( 0 )

            # load notes in advance
            while current [ 1 ] < tick_offset + tick_period_on_screen * 3:
                notes_loaded.append ( current )
                current = next ( notes )

        screen.fill ( ( 255, 255, 255 ) )

        for note in notes_loaded:
            if channels_visible [ int ( note [ 3 ] ) ]:
                pygame.draw.rect ( screen,
                        channel_colours [ int ( note [ 3 ] ) % num_colours ],
                        ( ( note [ 1 ] - tick_offset ) * tick_magnify,
                            height - ( note [ 0 ] - min_note ) * note_thickness,
                            note [ 2 ] * tick_magnify,
                            note_thickness )
                        )

        pygame.display.flip ()

        tick_offset += speed

    print ( tick_offset )



#def calculateMidiFileDuration ( midi: mido.MidiFile ):
#    return max ( [ calculateTrackDuration ( track ) for track in midi.tracks ] )
#
#def calculateTrackDuration ( track: mido.MidiTrack ):
#    return sum ( [ msg.time for msg in track ] )

if __name__ == "__main__":
    main ()
