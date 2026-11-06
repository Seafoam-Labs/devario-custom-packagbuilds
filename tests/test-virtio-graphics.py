#!/usr/bin/env python3
"""Check virtio graphics environment defaults without changing the host."""
import json
import os
from pathlib import Path
import subprocess
import types
import unittest
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1] / 'devario-installer/devario-system-integration'


class VirtioGraphics(unittest.TestCase):
    def test_wrapper_defaults_and_overrides(self):
        graphics = types.ModuleType('graphics_session')
        exec(compile((PACKAGE / 'graphics-session').read_text(), 'graphics-session', 'exec'), graphics.__dict__)
        for virtio, original, expected in (
            (True, {}, {'MESA_LOADER_DRIVER_OVERRIDE': 'zink', 'LIBGL_KOPPER_DRI2': 'true'}),
            (True, {'LIBGL_KOPPER_DRI2': 'false'}, {'MESA_LOADER_DRIVER_OVERRIDE': 'zink', 'LIBGL_KOPPER_DRI2': 'false'}),
            (True, {'MESA_LOADER_DRIVER_OVERRIDE': 'virgl'}, {'MESA_LOADER_DRIVER_OVERRIDE': 'virgl'}),
            (False, {}, {}),
        ):
            with self.subTest(virtio=virtio, original=original), \
                    patch.object(graphics.Path, 'is_file', return_value=False), \
                    patch.object(graphics, 'render_preference', return_value='auto'), \
                    patch.object(graphics, 'virtio_only', return_value=virtio):
                before = dict(original)
                self.assertEqual(graphics.startup_environment(original),
                                 dict(expected, AQUEOUS_RENDER_GPU_PREFERENCE='auto'))
                self.assertEqual(original, before)

    def test_uwsm_defaults_and_overrides(self):
        script = (PACKAGE / '61-devario-virtio.sh').read_text().replace(
            '/usr/lib/devario/graphics-session', 'detect_virtio')
        script = 'detect_virtio() { return "$DETECT_STATUS"; }\n' + script + '''
python3 -c 'import json,os; print(json.dumps({k:os.environ.get(k) for k in ("MESA_LOADER_DRIVER_OVERRIDE","LIBGL_KOPPER_DRI2")}))'
'''
        for status, overrides, expected in (
            ('0', {}, {'MESA_LOADER_DRIVER_OVERRIDE': 'zink', 'LIBGL_KOPPER_DRI2': 'true'}),
            ('0', {'LIBGL_KOPPER_DRI2': 'false'}, {'MESA_LOADER_DRIVER_OVERRIDE': 'zink', 'LIBGL_KOPPER_DRI2': 'false'}),
            ('0', {'MESA_LOADER_DRIVER_OVERRIDE': 'virgl'}, {'MESA_LOADER_DRIVER_OVERRIDE': 'virgl', 'LIBGL_KOPPER_DRI2': None}),
            ('1', {}, {'MESA_LOADER_DRIVER_OVERRIDE': None, 'LIBGL_KOPPER_DRI2': None}),
        ):
            with self.subTest(status=status, overrides=overrides):
                env = dict(overrides, PATH=os.environ['PATH'], DETECT_STATUS=status)
                output = subprocess.check_output(['sh', '-c', script], env=env, text=True, timeout=10)
                self.assertEqual(json.loads(output), expected)


if __name__ == '__main__':
    unittest.main()
