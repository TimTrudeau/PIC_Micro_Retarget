import pytest
from main import Remapper, Class688
from parse_target import ClassTarget


def test_construction():
    assert Remapper()
    map = Remapper("test688.txt", "testtarget.txt")
    assert hasattr(map, 'file688')
    assert hasattr(map, 'targetfile')


def test_readfile():
    regmap = Remapper()
    inlist = regmap.readfile("test688.txt")
    assert inlist is not None

    regmap = Remapper()
    inlist = regmap.readfile("testtarget.txt")
    assert inlist is not None

    regmap = Remapper()
    with pytest.raises(Exception):
        inlist = regmap.readfile()


def test_parse_688inc_file():
    mapped = Remapper()
    inlist = mapped.readfile("test688.txt")
    assert inlist is not None
    regmap = Class688()
    regmap.parse(inlist)
    assert len(regmap.registerdict) == 47
    assert regmap.registerdict['ADCON1'][0] == "H'009F'"
    assert len(regmap.registerdict['ADCON1']) == 7


def test_parse_target_inc_file():
    mapped = Remapper()
    inlist = mapped.readfile("testtarget.txt")
    assert inlist is not None
    regmap = ClassTarget()
    regmap.parse(inlist)
    assert len(regmap.registerdict) == 276
    assert regmap.registerdict['TOSH'][0] == '0FEFh'
    assert len(regmap.registerdict['TOSH']) == 11

def test_doRemapping():
    assert False

def test_parse_source_Files():
    assert False