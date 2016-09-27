import argparse
from tracklistcut import cut

parser = argparse.ArgumentParser(description='cut an MP3 file into multiple files')
parser.add_argument("audio_file", type=str, help="MP3 audio file")
parser.add_argument("tracklist_file", type=str, help='file with the list of songs')
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true", help='prints the progress of the operation')
group.add_argument("-q", "--quiet", action="store_true", help='does not print the progress of the operation')


if __name__ == '__main__':
    args = parser.parse_args()
    verbose = True
    if parser.quiet:
        verbose = False
    cut(
        args.audio_file,
        open(args.tracklist_file, 'r').readlines(),
        verbose=verbose
    )