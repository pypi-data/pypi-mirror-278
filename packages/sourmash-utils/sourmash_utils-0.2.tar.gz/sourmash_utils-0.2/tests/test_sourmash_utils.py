from sourmash_utils import *


def test_basic():
    pass


def test_minhash_create_dna():
    # DNA moltype works
    mh = FracMinHash(ksize=31, scaled=1000, moltype='DNA')
    assert mh.moltype == 'DNA'
    assert mh.scaled == 1000
    assert mh.ksize == 31


def test_minhash_create_dna_default():
    # DNA minhashes are default
    mh = FracMinHash(ksize=31, scaled=1000)
    assert mh.moltype == 'DNA'
    assert mh.scaled == 1000
    assert mh.ksize == 31


def test_minhash_create_protein():
    # test moltype protein
    mh = FracMinHash(ksize=7, scaled=100, moltype='protein')
    assert mh.moltype == 'protein'
    assert mh.scaled == 100
    assert mh.ksize == 7


def test_minhash_create_dayhoff():
    # test moltype dayhoff
    mh = FracMinHash(ksize=7, scaled=100, moltype='dayhoff')
    assert mh.moltype == 'dayhoff'
    assert mh.scaled == 100
    assert mh.ksize == 7


def test_minhash_create_hp():
    # test moltype hp
    mh = FracMinHash(ksize=7, scaled=100, moltype='hp')
    assert mh.moltype == 'hp'
    assert mh.scaled == 100
    assert mh.ksize == 7
