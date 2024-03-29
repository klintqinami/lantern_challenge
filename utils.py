import argparse
import hashlib


def generate_file_md5(filename):
    md5 = hashlib.md5()
    chunk_size = md5.block_size

    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            md5.update(chunk)

    return str(md5.hexdigest())


def clip_quotations(s):
    return s[1:-1]


def verify_with_etag(etag, filename):
    if not etag:
        print('Warning: no etag provided, cannot verify.')
        return

    if etag[0] == '"' and etag[-1] == '"':
        etag = clip_quotations(etag)

    computed_tag = generate_file_md5(filename)

    if computed_tag == etag:
        print('Successfully verified with etag.')
    else:
        print('Warning: computed md5 tag does not match server etag.')

    print('Computed etag: {}'.format(computed_tag))
    print('Input etag: {}'.format(etag))


def argparser():
    parser = argparse.ArgumentParser(
            description='A multi-source file downloader.'
    )

    parser.add_argument(
        '--url',
        default='https://images-na.ssl-images-amazon.com/images/I/612SNEBDltL.jpg',
        help='URL of the file to download.',
        type=str
    )

    parser.add_argument(
        '--nprocs',
        default=4,
        help='Number of processes used to download file.',
        type=int
    )

    parser.add_argument(
        '--chunk-size',
        default='8912',
        help='Size in bytes to use for requesting file chunks.',
        type=int
    )

    parser.add_argument(
        '--outfile-path',
        default='./test_file',
        help='Path where to save file. Directory will also be used to store '
        'intermediate chunks. Please ensure no name conflicts.',
        type=str
    )

    parser.add_argument(
        '--verify-with-md5',
        action='store_true',
        default=False,
        help='Compute an md5 hash of the downloaded file and compare against '
        ' etag.'
    )

    return parser.parse_args()

