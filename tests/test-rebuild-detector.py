import importlib.machinery,importlib.util,io,os,tarfile,tempfile,unittest
from contextlib import redirect_stdout
from pathlib import Path
loader=importlib.machinery.SourceFileLoader('query',str(Path(__file__).resolve().parents[1]/'devario-development/rebuild-detector/shelly-query'))
spec=importlib.util.spec_from_loader(loader.name,loader);q=importlib.util.module_from_spec(spec);loader.exec_module(q)
class Queries(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
  (self.root/'local/libfoo-1').mkdir(parents=True);(self.root/'local/app-1').mkdir();(self.root/'sync').mkdir()
  (self.root/'local/libfoo-1/desc').write_text('%NAME%\nlibfoo\n\n%VERSION%\n1-1\n\n%PROVIDES%\nlibfoo.so=1-64\n')
  (self.root/'local/libfoo-1/files').write_text('%FILES%\nusr/lib/\nusr/lib/libfoo.so.1\n')
  (self.root/'local/app-1/desc').write_text('%NAME%\napp\n\n%VERSION%\n2-1\n\n%DEPENDS%\nlibfoo.so=1-64\n')
  (self.root/'local/app-1/files').write_text('%FILES%\nusr/bin/app\nusr/share/a file\n')
  (self.root/'mirror').write_text('Server = file:///srv/repo\n')
  (self.root/'shelly.conf').write_text(f'[options]\nDBPath = {self.root}\n[devario-core]\nInclude = {self.root}/mirror\n')
  with tarfile.open(self.root/'sync/devario-core.db','w:gz') as t:
   b=b'%NAME%\nlibfoo\n\n%VERSION%\n1-1\n';m=tarfile.TarInfo('libfoo-1/desc');m.size=len(b);t.addfile(m,io.BytesIO(b))
  self.old=os.environ.get('DEVARIO_REBUILD_CONFIG');os.environ['DEVARIO_REBUILD_CONFIG']=str(self.root/'shelly.conf')
 def tearDown(self):
  if self.old is None:os.environ.pop('DEVARIO_REBUILD_CONFIG',None)
  else:os.environ['DEVARIO_REBUILD_CONFIG']=self.old
  self.temp.cleanup()
 def query(self,*args):
  out=io.StringIO()
  with redirect_stdout(out):rc=q.main(list(args))
  return rc,out.getvalue().splitlines()
 def test_names(self):self.assertEqual(self.query('-Qq'),(0,['app','libfoo']))
 def test_files_spaces(self):self.assertEqual(self.query('-Qql','app'),(0,['/usr/bin/app','/usr/share/a file']))
 def test_owner(self):self.assertEqual(self.query('-Qqo','/usr/lib/libfoo.so.1'),(0,['libfoo']))
 def test_directory_owner(self):self.assertEqual(self.query('-Qqo','/usr/lib/'),(0,['libfoo']))
 def test_reverse_virtual_dependency(self):self.assertEqual(self.query('tree','-rud1','libfoo'),(0,['libfoo','app']))
 def test_foreign(self):self.assertEqual(self.query('-Qqm'),(0,['app']))
 def test_sync(self):self.assertEqual(self.query('-Sl','__checkrebuild-reserved__','devario-core'),(0,['devario-core libfoo 1-1']))
 def test_config_include(self):self.assertEqual(self.query('config','--repo=devario-core','Server'),(0,['file:///srv/repo']))
 def test_missing_package(self):
  with self.assertRaises(ValueError):self.query('-Qql','absent')
if __name__=='__main__':unittest.main()
