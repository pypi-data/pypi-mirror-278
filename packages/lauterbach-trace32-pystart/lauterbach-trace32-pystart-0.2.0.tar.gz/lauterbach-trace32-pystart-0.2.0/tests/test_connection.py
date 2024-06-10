import unittest
from pathlib import Path

import lauterbach.trace32.pystart as pystart


class TestCreateConnection(unittest.TestCase):
    def testMCDConnectionWithStrParameter(self):
        con = pystart.MCDConnection("some/string/path")
        con._get_config_string(None)

    def testMCDConnectionWithPathParameter(self):
        con = pystart.MCDConnection(Path("some/other/path"))
        con._get_config_string(None)

    def testCADIConnectionWithStrParameter(self):
        con = pystart.CADIConnection("some/string/path")
        con._get_config_string(None)

    def testCADIConnectionWithPathParameter(self):
        con = pystart.CADIConnection(Path("some/other/path"))
        con._get_config_string(None)

    def testIRISConnectionWithStrParameter(self):
        con = pystart.IRISConnection("some/string/path")
        con._get_config_string(None)

    def testIRISConnectionWithPathParameter(self):
        con = pystart.IRISConnection(Path("some/other/path"))
        con._get_config_string(None)

    def testGDIConnectionWithStrParameter(self):
        con = pystart.GDIConnection("some/string/path")
        con._get_config_string(None)

    def testGDIConnectionWithPathParameter(self):
        con = pystart.GDIConnection(Path("some/other/path"))
        con._get_config_string(None)


if __name__ == "__main__":
    unittest.main()
