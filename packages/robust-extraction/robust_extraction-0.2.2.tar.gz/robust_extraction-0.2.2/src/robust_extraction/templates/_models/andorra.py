from ..templates import SheetModel, Template1d

NUM_W = 0.022
BOX_W = 0.06
SPACE_W = 0.008

ANDORRA = SheetModel(
    cols=Template1d(
        offsets=[NUM_W, BOX_W, BOX_W, SPACE_W, NUM_W, BOX_W, BOX_W, SPACE_W, NUM_W, BOX_W, BOX_W],
        a=1, b=12
    ),
    rows=Template1d(
        offsets=[1] * 21, # type: ignore
        a=1, b=22
    ),
    block_cols=[0, 4, 8]
)