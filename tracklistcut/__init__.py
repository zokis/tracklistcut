import re
import sys
from pydub import AudioSegment


def get_human_time(time):
    return str((time / (1000 * 60)) % 60) + ':' + str((time / 1000) % 60)


def cut(file, tracklist, _regex='(\d:\d{2}:\d{2})[\s?](.*)'):
    sys.stdout.write('Starting tracklistcut...\n')
    sys.stdout.write('Getting sound from mp3 file with AudioSegment...')
    sound = AudioSegment.from_mp3(file)
    sys.stdout.write('...Done.\n')
    _times = []
    _names = []
    sys.stdout.write('Preparing times list...')
    for track in map(unicode.strip, map(unicode, tracklist)):
        trackstart, trackname = re.findall(_regex, track)[0]
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
    for n, _ in enumerate(_times):
        if n == 0:
            continue
        A1 = _times[n - 1]
        A2 = _times[n]
        trackname = next(_names)
        sys.stdout.write('\nCutting song #%s (%s.mp3) [<{%s - %s}>]\n' % (
            n,
            trackname,
            get_human_time(A1),
            get_human_time(A2)
        ))
        sound[A1:A2].export("%s.mp3" % trackname, format="mp3", bitrate="192k")
        sys.stdout.write('Song #%s (%s.mp3) saved.\n' % (n, trackname))
