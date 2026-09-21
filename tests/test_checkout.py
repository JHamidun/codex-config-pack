"""Hash integrity must survive a user's global core.autocrlf setting."""
from pathlib import Path
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]

class CheckoutTests(unittest.TestCase):
    def test_release_attributes_preserve_hash_input_bytes(self):
        original = b'first line\nsecond line\n'
        for attributes in (False, True):
            with self.subTest(attributes=attributes), tempfile.TemporaryDirectory() as d:
                root = Path(d)
                repo = root/'repo'
                repo.mkdir()
                (repo/'fixture.txt').write_bytes(original)
                if attributes:
                    (repo/'.gitattributes').write_bytes((REPO/'.gitattributes').read_bytes())
                def git(*args):
                    subprocess.run(['git','-C',str(repo),'-c','core.autocrlf=true',*args],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                git('init')
                git('add','.')
                out = root/'checkout'
                out.mkdir()
                git('checkout-index','--all','--prefix='+out.as_posix()+'/')
                if attributes:
                    self.assertEqual((out/'fixture.txt').read_bytes(),original)
                else:
                    self.assertNotEqual((out/'fixture.txt').read_bytes(),original)
