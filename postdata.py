import os
import hug
from subprocess import check_output, call
from logging import getLogger, StreamHandler, DEBUG, INFO

from tasks import WordCount

log = getLogger(__name__)
log.setLevel(INFO)
handler = StreamHandler()
handler.setLevel(INFO)
log.addHandler(handler)


def count(path: str):
    """ background job """
    log.info('count method: {}'.format(path))
    return call('python tasks.py WordCount --path={}'.format(path), shell=True, universal_newlines=True)


def post_upload(path: str):
    log.info('post_upload: {}'.format(path))
    count(path)


@hug.post('/upload')
def upload_file(user: hug.directives.user, name, upload_file):
    """Converts multipart form data into native Python objects
    URLを返す
    """

    outfile = os.path.join('uploaded', name.decode('utf-8'))

    with open(outfile, 'wb') as f:
        f.write(upload_file)

    post_upload(path=outfile)

    return {'url': outfile, 'name': name, 'length': len(upload_file)}
