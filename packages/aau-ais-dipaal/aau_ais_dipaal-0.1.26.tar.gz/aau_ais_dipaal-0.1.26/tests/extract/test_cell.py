from dipaal.extract.grid import GridExtractor
from random import randint


def test_conversion():
    cell_extractor = GridExtractor(engine=None, grid_width=1001)
    cid = randint(0, 1000)
    cell_cord = cell_extractor._cid_to_cell_cord(cid)
    assert cell_extractor._cell_cord_to_cid(cell_cord) == cid

