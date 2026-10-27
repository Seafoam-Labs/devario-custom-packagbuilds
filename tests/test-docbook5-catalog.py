#!/usr/bin/env python3
"""Exercise target-root XML catalog registration without changing host catalogs."""
from pathlib import Path
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

HOOK = Path(__file__).resolve().parents[1] / 'devario-core/docbook5-xml/docbook5-xml.install'


class CatalogTests(unittest.TestCase):
    def test_clean_install_reinstall_upgrade_and_removal_preserve_other_catalogs(self):
        with tempfile.TemporaryDirectory(prefix='devario-docbook-catalog-') as temporary:
            root = Path(temporary)
            catalog = root / 'etc/xml/catalog'
            for phase in ('post_install', 'post_install', 'post_upgrade', 'post_remove'):
                subprocess.run(['bash', '-euc', 'source "$1"; "$2"',
                                'catalog-hook', str(HOOK), phase], cwd=root, check=True)
                entries = list(ET.parse(catalog).getroot())
                managed = [entry for entry in entries
                           if entry.attrib.get('catalog', '').startswith('file:///etc/xml/docbook-')]
                self.assertEqual(len(managed), 0 if phase == 'post_remove' else 10)
                self.assertEqual(len({tuple(sorted(entry.attrib.items())) for entry in managed}),
                                 0 if phase == 'post_remove' else 10)
                if phase == 'post_install' and len(entries) == 10:
                    subprocess.run(['xmlcatalog', '--noout', '--add', 'uri',
                                    'urn:unrelated', 'file:///unrelated.xml', str(catalog)], check=True)
                else:
                    self.assertTrue(any(entry.attrib.get('name') == 'urn:unrelated'
                                        for entry in entries))


if __name__ == '__main__':
    unittest.main()
