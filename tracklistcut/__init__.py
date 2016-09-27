import re
import sys
from pydub import AudioSegment


def cut(file, tracklist):
    sys.stdout.write('Starting tracklistcut...\n')
    sys.stdout.write('Getting sound from mp3 file with AudioSegment...')
    sound = AudioSegment.from_mp3(file)
    sys.stdout.write('...Done.\n')
    _times = []
    _names = []
    sys.stdout.write('Preparing times list...')
    for track in map(unicode.strip, map(unicode, tracklist)):
        trackstart, trackname = re.findall('(\d:\d{2}:\d{2})[\s?](.*)', track)[0]
        _names.append(trackname)
        _trackstart = map(int, trackstart.split(':'))
        _trackstart[0] = _trackstart[0] * 60 * 60
        _trackstart[1] = _trackstart[1] * 60
        _trackstart[2] = _trackstart[2]
        trackstart_ms = sum(_trackstart) * 1000
        _times.append(trackstart_ms)
    sys.stdout.write('...Done.\n')
    _times.append(len(sound))
    _names = iter(_names)
    for n, time in enumerate(range(len(_times))):
        if n == 0:
            continue
        A1 = _times[time - 1]
        A2 = _times[time]
        trackname = next(_names)
        sys.stdout.write('\nCutting song #%s (%s.mp3) [<{%s - %s}>]\n' % (
            n,
            trackname,
            str((A1 / (1000 * 60)) % 60) + ':' + str((A1 / 1000) % 60),
            str((A2 / (1000 * 60)) % 60) + ':' + str((A2 / 1000) % 60)
        ))
        sound[A1:A2].export("%s.mp3" % trackname, format="mp3", bitrate="192k")
        sys.stdout.write('Song #%s (%s.mp3) saved.\n' % (n, trackname))
