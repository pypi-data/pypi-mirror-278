import argparse
import os
from .extractor import download_video


def main():
    parser = argparse.ArgumentParser(
        description='Download YouTube video and extract as MP3',
    )
    parser.add_argument('youtube_url', help='URL of the YouTube Video')
    parser.add_argument('output_path', help='Output path of the extracted MP3')
    args = parser.parse_args()

    print('Downloading video...')

    download_video(args.youtube_url, args.output_path)

    print(f'Audio extracted {args.output_path}')



if __name__ == '__main__':
    main()
