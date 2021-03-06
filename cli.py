import argparse
import codecs
from tracklistcut import cut

parser = argparse.ArgumentParser(description='cut an MP3 file into multiple files')
parser.add_argument("audio_file", type=str, help="MP3 audio file")
parser.add_argument("tracklist_file", type=str, help='file with the list of songs')

parser.add_argument("-a", "--artist", type=str, help='artist')
parser.add_argument("-A", "--album", type=str, help='album')
parser.add_argument("-y", "--year", type=int, help='year')

parser.add_argument("-v", "--verbose", action="store_true", help='prints the progress of the operation')
parser.add_argument("-q", "--quiet", action="store_true", help='does not print the progress of the operation')


if __name__ == '__main__':
    args = parser.parse_args()
    verbose = True
    if args.quiet:
        verbose = False
    cut(
        args.audio_file,
        codecs.open(args.tracklist_file, 'r', 'utf-8').readlines(),
        verbose=verbose,
        artist=args.artist if args.artist else None,
        album=args.album if args.album else None,
        year=args.year if args.year else None,
    )
