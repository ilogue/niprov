import unittest
import os, shutil


class ApiTests(unittest.TestCase):

    def setUp(self):
        self.dbpath = os.path.expanduser(os.path.join('~','provenance.json'))
        if os.path.exists(self.dbpath):
            shutil.move(self.dbpath, self.dbpath.replace('.json','.backup.json'))
        os.mkdir('temp')

    def tearDown(self):
        if os.path.exists(self.dbpath):
            shutil.move(self.dbpath, self.dbpath.replace('.json','.test.json'))
        shutil.rmtree('temp')

    def test_Discover(self):
        import niprov
        niprov.discover('testdata')
        img = niprov.ProvenanceContext().get().byLocation(os.path.abspath('testdata/dicom/T1.dcm'))
        self.assertEqual(img.provenance['dimensions'], [80, 80, 10])
        img = niprov.ProvenanceContext().get().byLocation(os.path.abspath('testdata/eeg/stub.cnt'))
        self.assertEqual(img.provenance['subject'], 'Jane Doe')

    def test_Export_terminal(self):
        import niprov
        niprov.discover('testdata')
        pth = os.path.abspath('testdata/dicom/T1.dcm')
        provenance = niprov.ProvenanceContext().get().byLocation(pth)
        niprov.print_(provenance)

    def test_Log(self):
        import niprov
        niprov.discover('testdata')
        newfile = os.path.abspath('temp/smoothed.test')
        self.touch(newfile)
        niprov.log(newfile, 'test', os.path.abspath('testdata/eeg/stub.cnt'))
        img = niprov.ProvenanceContext().get().byLocation(newfile)
        self.assertEqual(img.provenance['subject'], 'Jane Doe')
        self.assertEqual(img.provenance['size'], os.path.getsize(newfile))

    def test_Narrative_file(self):
        import niprov
        niprov.discover('testdata')
        pth = os.path.abspath('testdata/dicom/T1.dcm')
        provenance = niprov.ProvenanceContext().get().byLocation(pth)
        text = niprov.export(provenance, 'direct','narrated')
        self.assertEqual(text, ("This is a T1 image. It was recorded August 5, " 
            "2014. The participant's name is 05aug14test. It is 158KB in size. "))

#    def test_Narrative_pipeline(self):
#        import niprov
#        niprov.discover('testdata')
#        self.touch('temp/smoothed.test')
#        niprov.log('temp/smoothed.test','spatial smoothing',
#            'testdata/parrec/T2.PAR')
#        self.touch('temp/stats.test')
#        niprov.log('temp/stats.test','t-test','temp/smoothed.test')
#        text = niprov.export(format='narrative', forPipeline='temp/stats.test')
#        self.assertEqual(text, ("A T2 image was recorded. A spatial smoothing "
#            "was then applied. A t-test was then applied."))

    def test_Rename(self):
        try:
            import niprov
            files, directory = self.createExtensionlessFiles()
            niprov.renameDicoms(directory)
            assert not os.path.isfile(files[0])
            assert os.path.isfile(files[0]+'.dcm')
        finally:
            self.clearDicomfiles()

    def test_bySubject(self):
        import niprov
        niprov.discover('testdata')
        provenance = niprov.ProvenanceContext().get().bySubject('05aug14test')
        niprov.print_(provenance)

    def createExtensionlessFiles(self):
        if not os.path.exists('dicomdir'):
            os.makedirs('dicomdir')
        files = []
        for n in range(5):
            f = os.path.join('dicomdir',str(n))
            files.append(f)
            with open(f,'w') as fhandle:
                fhandle.write('x')
        return files, 'dicomdir'

    def clearDicomfiles(self):
        shutil.rmtree('dicomdir')

    def touch(self, path):
        with open(path,'w') as tempfile:
            tempfile.write('0')


