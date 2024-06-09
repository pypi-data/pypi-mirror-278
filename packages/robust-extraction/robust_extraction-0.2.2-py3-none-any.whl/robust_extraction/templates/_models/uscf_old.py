from ..templates import SheetModel, Template1d

USCF_OLD = SheetModel(
  cols=Template1d(
    offsets=[1, 1, 1, 1, 1],
    a=0, b=5
  ),
  rows=Template1d(
    offsets=[1 for _ in range(36)],
    a=4, b=35
  ),
  block_cols=[0, 2]
)