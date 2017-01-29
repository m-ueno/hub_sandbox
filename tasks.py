import os
import time
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

if __name__ == '__main__':
    luigi.run()
