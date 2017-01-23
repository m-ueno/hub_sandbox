import os
import time
from subprocess import check_output
import luigi


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


if __name__ == '__main__':
    luigi.run()
