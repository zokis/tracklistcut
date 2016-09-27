import re
from pydub import AudioSegment


def cut(file, tracklist):
    print 'Iniciando os trampos'
    print 'AudioSegment...'
    sound = AudioSegment.from_mp3(file)
    _times = []
    _names = []
    print 'preparando os tempos'
    for track in map(unicode.strip, map(unicode, tracklist)):
        trackstart, trackname = re.findall('(\d:\d{2}:\d{2})[\s?](.*)', track)[0]
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
    for n, time in enumerate(range(len(_times))):
        if n == 0:
            continue
        A1 = _times[time - 1]
        A2 = _times[time]
        trackname = next(_names)
        print 'cortando musica %s (%s) [<{%s - %s}>]' % (
            n,
            trackname,
            str((A1 / (1000 * 60)) % 60) + ':' + str((A1 / 1000) % 60),
            str((A2 / (1000 * 60)) % 60) + ':' + str((A2 / 1000) % 60)
        )
        sound[A1:A2].export("%s.mp3" % trackname, format="mp3", bitrate="192k")
        print 'musica %s cortada' % n
