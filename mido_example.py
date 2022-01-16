import svgwrite
import mido
import math

midi_file = mido.MidiFile ( "./IMSLP212667-WIMA.7b20-bwv542-a4-1.mid", clip=True )

track_number = 4

msgs = [ msg for msg in midi_file.tracks [ track_number ] if hasattr ( msg, 'note' ) and msg.time > 0 and msg.time < 400 ] [ :10 ]

notes = [ msg.note for msg in msgs ]
times = [ msg.time for msg in msgs ]

min_note = min ( notes )
max_note = max ( notes )

note_range = max_note - min_note

min_time = min ( times )
max_time = max ( times )

time_range = max_time - min_time

points = []

for msg in msgs:
    x = ( msg.time - min_time ) * 400 / time_range
    y = ( msg.note - min_note ) * 400 / note_range

    points.append ( ( x, y ) )

#points.append ( [ 200, 200 ] )
#
#for msg in msgs:
#    angle = math.radians ( ( msg.note - min_note ) * 360 / note_range )
#    length = ( msg.time - min_time ) * 400 / 2 / time_range
#
#    prev = points [ -1 ]
#    
#    new = [ int ( math.cos ( angle ) * length + prev [ 0 ] ),
#        int ( math.sin ( angle ) * length + prev [ 1 ] ) ]
#
#    if new [ 0 ] < 0 or new [ 0 ] > 400 or new [ 1 ] < 0 or new [ 1 ] > 400:
#        break
#
#    points.append ( new )

drawing = svgwrite.Drawing ( filename='out.svg', height=400, width=100 )

drawing.add ( drawing.polyline ( points=points, stroke='black', fill="none" ) )

drawing.save ()
