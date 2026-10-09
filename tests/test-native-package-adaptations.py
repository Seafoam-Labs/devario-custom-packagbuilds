"""Native adaptation fixtures. Set DEVARIO_REFLECTOR_ARCHIVE to reflector-2023.tar.xz."""
import copy,hashlib,importlib.util,json,os,subprocess,tarfile,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'audits/application-expansion-2026-10-08'
class Java(unittest.TestCase):
 def test_selection_and_compatibility_alias(self):
  recipe=ROOT/'devario-libs/java-common'
  with tempfile.TemporaryDirectory() as tmp:
   stage=Path(tmp)
   subprocess.run(['bash','-c','source "$1"; srcdir="$2"; pkgdir="$3"; cd "$srcdir"; package_java-runtime-common','fixture',str(recipe/'PKGBUILD'),str(recipe),tmp],check=True,capture_output=True,text=True)
   self.assertEqual(os.readlink(stage/'usr/bin/archlinux-java'),'devario-java')
   jvm=stage/'usr/lib/jvm'
   for name in ('java-17-openjdk','java-21-openjdk'):
    binary=jvm/name/'bin/java';binary.parent.mkdir(parents=True);binary.write_text('#!/bin/sh\nexit 0\n');binary.chmod(0o755)
   code='''helper=$1; fixture=$2; set -- help
source "$helper" >/dev/null
JVM_DIR=$fixture; DEFAULT_PATH=$fixture/default; DEFAULT_PATH_JRE=$fixture/default-runtime
cd "$fixture"
do_set java-21-openjdk
do_get
do_set java-17-openjdk
do_get
do_unset
'''
   result=subprocess.run(['bash','-c',code,'fixture',str(stage/'usr/bin/devario-java'),str(jvm)],check=True,capture_output=True,text=True)
   self.assertEqual(result.stdout.splitlines(),['java-21-openjdk','java-17-openjdk'])
   self.assertFalse((jvm/'default').is_symlink())
@unittest.skipUnless(os.environ.get('DEVARIO_REFLECTOR_ARCHIVE'),'Set DEVARIO_REFLECTOR_ARCHIVE')
class Reflector(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();archive=Path(os.environ['DEVARIO_REFLECTOR_ARCHIVE'])
  assert hashlib.sha512(archive.read_bytes()).hexdigest()=='11aec550c15080695525409f11eae6d4b545df8b37a8e0727de939eefec2b2fa6aa95c5c3500a6c8a940b6060cdaf2526430ed47e01a3c6f098e1b77189eb479'
  with tarfile.open(archive) as source:source.extractall(cls.temp.name,filter='data')
  cls.source=Path(cls.temp.name)/'reflector-2023';recipe=ROOT/'devario-utilities/reflector'
  for patch in ('mp-fork.patch','devario-catalog.patch'):
   subprocess.run(['patch','--batch','-p1','-i',str(recipe/patch)],cwd=cls.source,check=True,capture_output=True)
  spec=importlib.util.spec_from_file_location('native_reflector',cls.source/'Reflector.py');cls.module=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.module)
  cls.catalog=json.loads((AUDIT/'repository-catalog.json').read_text())
 @classmethod
 def tearDownClass(cls):cls.temp.cleanup()
 def test_catalog_to_native_mirrorlist(self):
  status=self.module.devario_catalog_status(self.catalog);mirrors=list(self.module.MirrorStatusFilter().filter_mirrors(status['urls']))
  self.assertEqual(len(mirrors),1);status['urls']=mirrors;text=self.module.format_mirrorlist(status,0)
  self.assertIn('Server = https://mirrors.seafoam-labs.org/$repo/$arch',text);self.assertNotIn('/os/',text);self.assertNotIn('Arch Linux',text)
 def test_rejects_foreign_status_format(self):
  with self.assertRaises(self.module.MirrorStatusError):self.module.devario_catalog_status({'urls':[]})
 def test_rejects_incomplete_shared_root(self):
  catalog=copy.deepcopy(self.catalog);next(e for e in catalog if e['syncPrefix']=='devario-core')['serverUrl']='https://other.example/devario-core/$arch'
  with self.assertRaises(self.module.MirrorStatusError):self.module.devario_catalog_status(catalog)
 def test_rejects_insecure_servers(self):
  catalog=copy.deepcopy(self.catalog);entry=next(e for e in catalog if e['syncPrefix']=='devario-core');entry['serverUrl']=entry['serverUrl'].replace('https:','http:')
  with self.assertRaises(self.module.MirrorStatusError):self.module.devario_catalog_status(catalog)
 def test_rejects_unavailable_geographic_measurements(self):
  status=self.module.devario_catalog_status(self.catalog)
  with self.assertRaises(self.module.MirrorStatusError):list(self.module.MirrorStatusFilter(countries=['US']).filter_mirrors(status['urls']))
 def test_service_uses_native_paths(self):
  service=(self.source/'reflector.service').read_text();config=(self.source/'reflector.conf').read_text()
  self.assertIn('ReadWritePaths=/etc/shelly.d',service);self.assertIn('--save /etc/shelly.d/mirrorlist',config);self.assertNotIn('/etc/pacman',service+config)
if __name__=='__main__':unittest.main()
