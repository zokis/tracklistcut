import re
import sys
from pydub import AudioSegment


REGEX = [
    '\d\d:\d\d:\d\d',
    '\d:\d\d:\d\d',
    '\d\d:\d\d',
    '\d:\d\d'
]


def sysout(string, verbose=True):
    if verbose:
        sys.stdout.write(string)


def get_human_time(time):
    return str((time / (1000 * 60)) % 60).zfill(2) + ':' + str((time / 1000) % 60).zfill(2)


def get_better_regex(line):
    for _regex in REGEX:
        m = re.search(_regex, line)
        if m:
            return _regex


def clean_lines(lines):
    _lines = []
    for line in lines:
        if get_better_regex(line):
            _lines.append(line)
    return _lines


def get_time_trackname(line, _regex):
    m = re.search(_regex, line)
    time = m.group(0)
    _trackstart = map(int, time.split(':'))
    if len(time) == 3:
        _trackstart[0] = _trackstart[0] * 60 * 60
        _trackstart[1] = _trackstart[1] * 60
        _trackstart[2] = _trackstart[2]
    else:
        _trackstart[0] = _trackstart[0] * 60
        _trackstart[1] = _trackstart[1]

    trackstart_ms = sum(_trackstart) * 1000
    trackname = line.replace(time, '').replace('-', '').strip()
    return trackstart_ms, trackname


def get_times_and_names(tracklist, verbose):
    sysout('Preparing times list', verbose=verbose)
    _times = []
    _names = []
    for n, line in enumerate(map(unicode.strip, map(unicode, tracklist))):
        sysout('.', verbose=verbose)
        time, trackname = get_time_trackname(line, get_better_regex(line))
        _times.append(time)
        _names.append(unicode(n).zfill(3) + ' ' + trackname)
    return _times, _names


def cut(file, tracklist, verbose=True, artist='Various artists', album='None', year='2016'):
    if not isinstance(tracklist, (list, tuple)):
        tracklist = tracklist.split('\n')
    tracklist = clean_lines(tracklist)

    sysout('Cutting the %s Album\n' % album, verbose=verbose)
    sysout('Artist %s\n' % artist, verbose=verbose)
    sysout('year %s\n' % year, verbose=verbose)

    sysout('Starting tracklistcut...\n', verbose=verbose)
    sysout('Getting sound from mp3 file with AudioSegment...', verbose=verbose)
    sound = AudioSegment.from_mp3(file)
    sysout('...Done.\n', verbose=verbose)
    _times, _names = get_times_and_names(
        tracklist,
        verbose
    )
    _names = iter(_names)
    _times.append(len(sound))
    sysout('...Done.\n', verbose=verbose)
    for n, _ in enumerate(_times):
        if n == 0:
            continue
        strat_time = _times[n - 1]
        end_time = _times[n]
        trackname = next(_names) or 'track_%s' % n
        sysout('\nCutting song #%s (%s.mp3) [<{%s - %s}>]\n' % (
            n,
            trackname,
            get_human_time(strat_time),
            get_human_time(end_time)
        ), verbose=verbose)
        sound[strat_time:end_time].export(
            "%s.mp3" % trackname,
            format="mp3",
            bitrate="192k",
            tags={'artist': artist, 'album': album, 'year': year}
        )
        sysout('Song #%s (%s.mp3) saved.\n' % (n, trackname), verbose=verbose)
