import sys, time
import mido, librosa

#https://github.com/mido/mido
#https://librosa.org/doc/main/generated/librosa.midi_to_note.html

#mfn = 'merryChristmas.mid'
mfn = '3400themerrypheastevenritchie.mid'
mid = mido.MidiFile(mfn)

outport = None
for port in mido.get_output_names():
  outport = port; print("output:", outport)

def currentTime(): return round(time.time() * 1000)

firstTime = currentTime()

port = mido.open_output(outport)
sys.stdout.reconfigure(encoding='utf-8')

for msg in mid.play():
  #port.send(msg)
  #print(msg)
  if msg.time != 0: 
    diffTime = currentTime() - firstTime
    n = librosa.midi_to_note(int(msg.note))
    print(msg.note, diffTime, n, msg.time)

### end ###
