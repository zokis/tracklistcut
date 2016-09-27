import re
import sys
from pydub import AudioSegment


def sysout(string, verbose=True):
    if verbose:
        sys.stdout.write(string)


def get_human_time(time):
    return str((time / (1000 * 60)) % 60).zfill(2) + ':' + str((time / 1000) % 60).zfill(2)


def get_times_and_names(tracklist, sound, verbose, _regex):
    sysout('Preparing times list...', verbose=verbose)
    _times = []
    _names = []
    for track in map(unicode.strip, map(unicode, tracklist)):
        trackstart, trackname = re.findall(_regex, track)[0]
        _names.append(trackname)
        _trackstart = map(int, trackstart.split(':'))
        _trackstart[0] = _trackstart[0] * 60 * 60
        _trackstart[1] = _trackstart[1] * 60
        _trackstart[2] = _trackstart[2]
        trackstart_ms = sum(_trackstart) * 1000
        _times.append(trackstart_ms)
    return _times, _names


def cut(file, tracklist, _regex='(\d:\d{2}:\d{2})[\s?](.*)', verbose=True):
    if not isinstance(tracklist, (list, tuple)):
        tracklist = tracklist.split('\n')
    sysout('Starting tracklistcut...\n', verbose=verbose)
    sysout('Getting sound from mp3 file with AudioSegment...', verbose=verbose)
    sound = AudioSegment.from_mp3(file)
    sysout('...Done.\n', verbose=verbose)

    _times, _names = get_times_and_names(tracklist, sound, verbose, _regex)

    sysout('...Done.\n', verbose=verbose)
    _times.append(len(sound))
    _names = iter(_names)
    for n, _ in enumerate(_times):
        if n == 0:
            continue
        strat_time = _times[n - 1]
        end_time = _times[n]
        trackname = next(_names)
        sysout('\nCutting song #%s (%s.mp3) [<{%s - %s}>]\n' % (
            n,
            trackname,
            get_human_time(strat_time),
            get_human_time(end_time)
        ), verbose=verbose)
        sound[strat_time:end_time].export("%s.mp3" % trackname, format="mp3", bitrate="192k")
        sysout('Song #%s (%s.mp3) saved.\n' % (n, trackname), verbose=verbose)


if __name__ == '__main__':
    cut(sys.argv[1], open(sys.argv[2], 'w').readlines())
