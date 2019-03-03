from pydub import AudioSegment

files = ['hit.mp3', 'bullet.mp3']
for file in files:
    base = file.split('.')[0]
    sound = AudioSegment.from_mp3(file)
    sound.export(f'{base}.wav', format='wav')
    print(base)