import mido

def main ():
    midi_filename = "./IMSLP212667-WIMA.7b20-bwv542-a4-1.mid"

    csv_filename = "./great_fugue.csv"

    convertMidiToCsv ( midi_filename, csv_filename )
    
def convertMidiToCsv ( midi_filename, csv_filename ):
    notes = getNotesFromMidiFile ( midi_filename )

    saveNotesToCsv ( notes, csv_filename )

def getNotesFromMidiFile ( midi_filename ):
    midi_file = mido.MidiFile ( midi_filename, clip=True )

    current = []
    time = 0

    for message in midi_file:
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

def saveNotesToCsv ( notes, csv_filename ):
    notes_list = list ( notes )

    with open ( csv_filename, 'w' ) as csv_file:
        note_vals = [ note [ 0 ] for note in notes_list ]

        metadata = [ max ( note_vals ),
                min ( note_vals ),
                notes_list [ -1 ] [ 1 ] + notes_list [ -1 ] [ 2 ], # duration
                max ( [ note [ 3 ] for note in notes_list ] ) ]

        csv_file.write ( ','.join ( [ str ( val ) for val in metadata ] ) + '\n' )

        for note in notes_list:
            csv_file.write ( ','.join ( [ str ( val ) for val in note ] ) + '\n' )

def readCsvFile ( csv_filename ):
    with open ( csv_filename, 'r' ) as csv_file:
        for line in csv_file:
            yield [ float ( val ) for val in line.split ( ',' ) ]

if __name__ == "__main__":
    main ()
