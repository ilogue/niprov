import unittest
from mock import Mock
from datetime import datetime
from tests.test_basefile import BaseFileTests


class CNTTests(BaseFileTests):

    def setUp(self):
        super(CNTTests, self).setUp()
        self.filesys.open.return_value = MockFile()
        from niprov.cnt import NeuroscanFile
        self.constructor = NeuroscanFile
        self.file = NeuroscanFile(self.path, dependencies=self.dependencies)

    def test_Inspect_parses_experimental_basics(self):
        out = self.file.inspect()
        self.assertEqual(out['subject'], 'Jane Doe')
        self.assertEqual(out['dimensions'], [32, 2080])
        self.assertEqual(out['acquired'], datetime(2015,3,9,13,7,3))
        self.assertEqual(out['sampling-frequency'], 1000)
        self.assertEqual(out['duration'], 2080/1000.)

    def test_Determines_modality(self):
        out = self.file.inspect()
        self.assertEqual(out['modality'], 'EEG')

    def test_Preserves_modality_if_inherited(self):
        pass # Doesn't have to preserve


class MockFile(object):

    def __init__(self):
        self.cursor = -1

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def read(self, nbytes):
        self.cursor = self.cursor + 1
        return _data[self.cursor]


_data = [
None,   #h.rev               = self._fread(fid,12,'char')
None,   #h.nextfile          = self._fread(fid,1,'long')
None,   #h.prevfile          = self._fread(fid,1,'ulong')
None,   #h.type              = self._fread(fid,1,'char')
None,   #h.id                = self._fread(fid,20,'char')
None,   #h.oper              = self._fread(fid,20,'char')
None,   #h.doctor            = self._fread(fid,20,'char')
None,   #h.referral          = self._fread(fid,20,'char')
None,   #h.hospital          = self._fread(fid,20,'char')
#h.patient = self._fread(fid,20,'char')
b'Jane Doe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
None,   #h.age               = self._fread(fid,1,'short')
None,   #h.sex               = self._fread(fid,1,'char')
None,   #h.hand              = self._fread(fid,1,'char')
None,   #h.med               = self._fread(fid,20, 'char')
None,   #h.category          = self._fread(fid,20, 'char')
None,   #h.state             = self._fread(fid,20, 'char')
None,   #h.label             = self._fread(fid,20, 'char')
b'09/03/15' ,   #h.date              = self._fread(fid,10, 'char')
b'13:07:03',   #h.time              = self._fread(fid,12, 'char')
None,   #h.mean_age          = self._fread(fid,1,'float')
None,   #h.stdev             = self._fread(fid,1,'float')
None,   #h.n                 = self._fread(fid,1,'short')
None,   #h.compfile          = self._fread(fid,38,'char')
None,   #h.spectwincomp      = self._fread(fid,1,'float')
None,   #h.meanaccuracy      = self._fread(fid,1,'float')
None,   #h.meanlatency       = self._fread(fid,1,'float')
None,   #h.sortfile          = self._fread(fid,46,'char')
None,   #h.numevents         = self._fread(fid,1,'int')
None,   #h.compoper          = self._fread(fid,1,'char')
None,   #h.avgmode           = self._fread(fid,1,'char')
None,   #h.review            = self._fread(fid,1,'char')
None,   #h.nsweeps           = self._fread(fid,1,'ushort')
None,   #h.compsweeps        = self._fread(fid,1,'ushort')
None,   #h.acceptcnt         = self._fread(fid,1,'ushort')
None,   #h.rejectcnt         = self._fread(fid,1,'ushort')
None,   #h.pnts              = self._fread(fid,1,'ushort')
b' \x00',   #h.nchannels         = self._fread(fid,1,'ushort')
None,   #h.avgupdate         = self._fread(fid,1,'ushort')
None,   #h.domain            = self._fread(fid,1,'char')
None,   #h.variance          = self._fread(fid,1,'char')
b'\xe8\x03',   #h.rate              = self._fread(fid,1,'ushort')
None,   #h.scale             = self._fread(fid,1,'double')
None,   #h.veogcorrect       = self._fread(fid,1,'char')
None,   #h.heogcorrect       = self._fread(fid,1,'char')
None,   #h.aux1correct       = self._fread(fid,1,'char')
None,   #h.aux2correct       = self._fread(fid,1,'char')
None,   #h.veogtrig          = self._fread(fid,1,'float')
None,   #h.heogtrig          = self._fread(fid,1,'float')
None,   #h.aux1trig          = self._fread(fid,1,'float')
None,   #h.aux2trig          = self._fread(fid,1,'float')
None,   #h.heogchnl          = self._fread(fid,1,'short')
None,   #h.veogchnl          = self._fread(fid,1,'short')
None,   #h.aux1chnl          = self._fread(fid,1,'short')
None,   #h.aux2chnl          = self._fread(fid,1,'short')
None,   #h.veogdir           = self._fread(fid,1,'char')
None,   #h.heogdir           = self._fread(fid,1,'char')
None,   #h.aux1dir           = self._fread(fid,1,'char')
None,   #h.aux2dir           = self._fread(fid,1,'char')
None,   #h.veog_n            = self._fread(fid,1,'short')
None,   #h.heog_n            = self._fread(fid,1,'short')
None,   #h.aux1_n            = self._fread(fid,1,'short')
None,   #h.aux2_n            = self._fread(fid,1,'short')
None,   #h.veogmaxcnt        = self._fread(fid,1,'short')
None,   #h.heogmaxcnt        = self._fread(fid,1,'short')
None,   #h.aux1maxcnt        = self._fread(fid,1,'short')
None,   #h.aux2maxcnt        = self._fread(fid,1,'short')
None,   #h.veogmethod        = self._fread(fid,1,'char')
None,   #h.heogmethod        = self._fread(fid,1,'char')
None,   #h.aux1method        = self._fread(fid,1,'char')
None,   #h.aux2method        = self._fread(fid,1,'char')
None,   #h.ampsensitivity    = self._fread(fid,1,'float')
None,   #h.lowpass           = self._fread(fid,1,'char')
None,   #h.highpass          = self._fread(fid,1,'char')
None,   #h.notch             = self._fread(fid,1,'char')
None,   #h.autoclipadd       = self._fread(fid,1,'char')
None,   #h.baseline          = self._fread(fid,1,'char')
None,   #h.offstart          = self._fread(fid,1,'float')
None,   #h.offstop           = self._fread(fid,1,'float')
None,   #h.reject            = self._fread(fid,1,'char')
None,   #h.rejstart          = self._fread(fid,1,'float')
None,   #h.rejstop           = self._fread(fid,1,'float')
None,   #h.rejmin            = self._fread(fid,1,'float')
None,   #h.rejmax            = self._fread(fid,1,'float')
None,   #h.trigtype          = self._fread(fid,1,'char')
None,   #h.trigval           = self._fread(fid,1,'float')
None,   #h.trigchnl          = self._fread(fid,1,'char')
None,   #h.trigmask          = self._fread(fid,1,'short')
None,   #h.trigisi           = self._fread(fid,1,'float')
None,   #h.trigmin           = self._fread(fid,1,'float')
None,   #h.trigmax           = self._fread(fid,1,'float')
None,   #h.trigdir           = self._fread(fid,1,'char')
None,   #h.autoscale         = self._fread(fid,1,'char')
None,   #h.n2                = self._fread(fid,1,'short')
None,   #h.dir               = self._fread(fid,1,'char')
None,   #h.dispmin           = self._fread(fid,1,'float')
None,   #h.dispmax           = self._fread(fid,1,'float')
None,   #h.xmin              = self._fread(fid,1,'float')
None,   #h.xmax              = self._fread(fid,1,'float')
None,   #h.automin           = self._fread(fid,1,'float')
None,   #h.automax           = self._fread(fid,1,'float')
None,   #h.zmin              = self._fread(fid,1,'float')
None,   #h.zmax              = self._fread(fid,1,'float')
None,   #h.lowcut            = self._fread(fid,1,'float')
None,   #h.highcut           = self._fread(fid,1,'float')
None,   #h.common            = self._fread(fid,1,'char')
None,   #h.savemode          = self._fread(fid,1,'char')
None,   #h.manmode           = self._fread(fid,1,'char')
None,   #h.ref               = self._fread(fid,10,'char')
None,   #h.rectify           = self._fread(fid,1,'char')
None,   #h.displayxmin       = self._fread(fid,1,'float')
None,   #h.displayxmax       = self._fread(fid,1,'float')
None,   #h.phase             = self._fread(fid,1,'char')
None,   #h.screen            = self._fread(fid,16,'char')
None,   #h.calmode           = self._fread(fid,1,'short')
None,   #h.calmethod         = self._fread(fid,1,'short')
None,   #h.calupdate         = self._fread(fid,1,'short')
None,   #h.calbaseline       = self._fread(fid,1,'short')
None,   #h.calsweeps         = self._fread(fid,1,'short')
None,   #h.calattenuator     = self._fread(fid,1,'float')
None,   #h.calpulsevolt      = self._fread(fid,1,'float')
None,   #h.calpulsestart     = self._fread(fid,1,'float')
None,   #h.calpulsestop      = self._fread(fid,1,'float')
None,   #h.calfreq           = self._fread(fid,1,'float')
None,   #h.taskfile          = self._fread(fid,34,'char')
None,   #h.seqfile           = self._fread(fid,34,'char')
None,   #h.spectmethod       = self._fread(fid,1,'char')
None,   #h.spectscaling      = self._fread(fid,1,'char')
None,   #h.spectwindow       = self._fread(fid,1,'char')
None,   #h.spectwinlength    = self._fread(fid,1,'float')
None,   #h.spectorder        = self._fread(fid,1,'char')
None,   #h.notchfilter       = self._fread(fid,1,'char')
None,   #h.headgain          = self._fread(fid,1,'short')
None,   #h.additionalfiles   = self._fread(fid,1,'int')
None,   #h.unused            = self._fread(fid,5,'char')
None,   #h.fspstopmethod     = self._fread(fid,1,'short')
None,   #h.fspstopmode       = self._fread(fid,1,'short')
None,   #h.fspfvalue         = self._fread(fid,1,'float')
None,   #h.fsppoint          = self._fread(fid,1,'short')
None,   #h.fspblocksize      = self._fread(fid,1,'short')
None,   #h.fspp1             = self._fread(fid,1,'ushort')
None,   #h.fspp2             = self._fread(fid,1,'ushort')
None,   #h.fspalpha          = self._fread(fid,1,'float')
None,   #h.fspnoise          = self._fread(fid,1,'float')
None,   #h.fspv1             = self._fread(fid,1,'short')
None,   #h.montage           = self._fread(fid,40,'char')
None,   #h.eventfile         = self._fread(fid,40,'char')
None,   #h.fratio            = self._fread(fid,1,'float')
None,   #h.minor_rev         = self._fread(fid,1,'char')
None,   #h.eegupdate         = self._fread(fid,1,'short')
None,   #h.compressed        = self._fread(fid,1,'char')
None,   #h.xscale            = self._fread(fid,1,'float')
None,   #h.yscale            = self._fread(fid,1,'float')
None,   #h.xsize             = self._fread(fid,1,'float')
None,   #h.ysize             = self._fread(fid,1,'float')
None,   #h.acmode            = self._fread(fid,1,'char')
None,   #h.commonchnl        = self._fread(fid,1,'uchar')
None,   #h.xtics             = self._fread(fid,1,'char')
None,   #h.xrange            = self._fread(fid,1,'char')
None,   #h.ytics             = self._fread(fid,1,'char')
None,   #h.yrange            = self._fread(fid,1,'char')
None,   #h.xscalevalue       = self._fread(fid,1,'float')
None,   #h.xscaleinterval    = self._fread(fid,1,'float')
None,   #h.yscalevalue       = self._fread(fid,1,'float')
None,   #h.yscaleinterval    = self._fread(fid,1,'float')
None,   #h.scaletoolx1       = self._fread(fid,1,'float')
None,   #h.scaletooly1       = self._fread(fid,1,'float')
None,   #h.scaletoolx2       = self._fread(fid,1,'float')
None,   #h.scaletooly2       = self._fread(fid,1,'float')
None,   #h.port              = self._fread(fid,1,'short')
b' \x08\x00\x00',   #h.numsamples        = self._fread(fid,1,'ulong')
None,   #h.filterflag        = self._fread(fid,1,'char')
None,   #h.lowcutoff         = self._fread(fid,1,'float')
None,   #h.lowpoles          = self._fread(fid,1,'short')
None,   #h.highcutoff        = self._fread(fid,1,'float')
None,   #h.highpoles         = self._fread(fid,1,'short')
None,   #h.filtertype        = self._fread(fid,1,'char')
None,   #h.filterdomain      = self._fread(fid,1,'char')
None,   #h.snrflag           = self._fread(fid,1,'char')
None,   #h.coherenceflag     = self._fread(fid,1,'char')
None,   #h.continuoustype    = self._fread(fid,1,'char')
None,   #h.eventtablepos     = self._fread(fid,1,'ulong')
None,   #h.continuousseconds = self._fread(fid,1,'float')
None,   #h.channeloffset     = self._fread(fid,1,'long')
None,   #h.autocorrectflag   = self._fread(fid,1,'char')
None,   #h.dcthreshold       = self._fread(fid,1,'uchar')
]