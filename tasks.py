import os
import time
from subprocess import check_output
import json
import luigi
from luigi.contrib.esindex import CopyToIndex


class WordCount(luigi.Task):
    path = luigi.Parameter()

    def input(self):
        return self.path

    def output(self):
        return luigi.LocalTarget('{}.count'.format(self.input()))

    def run(self):
        print('{}: {}'.format('WordCount', self.path))

        time.sleep(1)
        count = os.stat(self.input()).st_size

        print('**********')
        print(count)

        with self.output().open('w') as out:
            out.write(str(count))


class PPT2PDF(luigi.Task):
    ppt_path = luigi.Parameter()
    outdir = luigi.Parameter(default=os.path.join(os.getcwd(), 'pdf'))

    def input(self):
        return self.ppt_path

    def output(self):
        basename = os.path.basename(self.ppt_path)
        basename = os.path.splitext(basename)[0]

        return luigi.LocalTarget(os.path.join(self.outdir, '{}.pdf'.format(basename)))

    def run(self):
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)

        cmd = 'libreoffice --headless --convert-to pdf --outdir "{outdir}" "{file}"'.format(
            outdir=self.outdir, file=self.input())

        check_output(cmd, shell=True, universal_newlines=True)


class PDF2TXT(luigi.Task):
    ppt_path = luigi.Parameter()
    outdir = luigi.Parameter(default=os.path.join(os.getcwd(), 'txt'))

    def requires(self):
        return PPT2PDF(ppt_path=self.ppt_path)  # => .pdf

    def output(self):
        basename = os.path.basename(self.input().path)
        basename = os.path.splitext(basename)[0]

        return luigi.LocalTarget(os.path.join(self.outdir, '{}.txt'.format(basename)))

    def run(self):

        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)

        cmd = 'pdftotext -eol unix "{pdf}" "{txt}"'.format(
            pdf=self.input().path,
            txt=self.output().path,
        )

        check_output(cmd, shell=True)


class GenerateThumbnail(luigi.Task):
    ppt_path = luigi.Parameter()
    outdir = luigi.Parameter(default=os.path.join(os.getcwd(), 'thumbnail'))

    def requires(self):
        return PPT2PDF(ppt_path=self.ppt_path)  # => .pdf

    def output(self):
        # how to handle many output per PDF

        basename = os.path.basename(self.input().path)
        self.basename = os.path.splitext(basename)[0]

        return luigi.LocalTarget(os.path.join(self.outdir, '{}-000.png'.format(self.basename)))

    def run(self):
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)

        basename = self.basename

        cmd = 'convert "{pdf}" "{d}/{basename}-%03d.png"'.format(
            pdf=self.input().path,
            basename=basename,
            d=self.outdir,
        )
        check_output(cmd, shell=True)


class Slide():

    def __init__(self, text, filename, page, url):
        self.filename = filename
        self.page = page
        self.text = text
        self.url = url

    def __dict__(self):
        return dict(
            filename=self.filename,
            page=self.page,
            text=self.text,
        )

    @classmethod
    def parse_file(cls, path):
        with open(path) as f:
            buf = f.read()

        pages = buf.split('\f')
        filename = os.path.basename(path)

        return [Slide(text=content.strip(), filename=filename, page=i, url=path)
                for (i, content) in enumerate(pages)]


class parseTxt(luigi.Task):
    ppt_path = luigi.Parameter()
    outdir = luigi.Parameter(default=os.path.join(os.getcwd(), 'json'))

    def requires(self):
        return PDF2TXT(ppt_path=self.ppt_path)  # => .txt

    def output(self):
        basename = os.path.basename(self.input().path)
        self.basename = os.path.splitext(basename)[0]

        return luigi.LocalTarget(os.path.join(self.outdir, '{}.json'.format(basename)))

    def run(self):
        slides = [s.__dict__() for s in Slide.parse_file(self.input().path)]

        with self.output().open('w') as f:
            f.write(json.dumps(slides))


class DBInsert(CopyToIndex):

    index = 'example'
    doc_type = 'pptpage'
    purge_existing_index = False  # True: DROP&CREATE, False: INSERT
    marker_index_hist_size = 1    # GET /update_log/

    ppt_path = luigi.Parameter()

    def requires(self):
        return parseTxt(ppt_path=self.ppt_path)  # => .json

    def docs(self):

        with self.input().open() as f:
            pages = json.loads(f.read())

        return pages


if __name__ == '__main__':
    luigi.run()
