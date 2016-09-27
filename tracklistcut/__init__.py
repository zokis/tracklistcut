import re
from pydub import AudioSegment


def get_human_time(time):
    return str((time / (1000 * 60)) % 60) + ':' + str((time / 1000) % 60)


def cut(file, tracklist, _regex='(\d:\d{2}:\d{2})[\s?](.*)'):
    print 'Iniciando os trampos'
    print 'AudioSegment...'
    sound = AudioSegment.from_mp3(file)
    _times = []
    _names = []
    print 'preparando os tempos'
    for track in map(unicode.strip, map(unicode, tracklist)):
        trackstart, trackname = re.findall(_regex, track)[0]
        _names.append(trackname)
        _trackstart = map(int, trackstart.split(':'))
        _trackstart[0] = _trackstart[0] * 60 * 60
        _trackstart[1] = _trackstart[1] * 60
        _trackstart[2] = _trackstart[2]
        trackstart_ms = sum(_trackstart) * 1000
        _times.append(trackstart_ms)
    print 'tempos preparados'
    _times.append(len(sound))
    _names = iter(_names)
    print 'tempos: ' + str(_times)
    for n, _ in enumerate(_times):
        if n == 0:
            continue
        A1 = _times[n - 1]
        A2 = _times[n]
        trackname = next(_names)
        print 'cortando musica %s (%s) [<{%s - %s}>]' % (
            n,
            trackname,
            get_human_time(A1),
            get_human_time(A2)
        )
        sound[A1:A2].export("%s.mp3" % trackname, format="mp3", bitrate="192k")
        print 'musica %s cortada' % n
