from .. import SheetModel
from .id import ModelID
from .fcde import FCDE
from .llobregat23 import LLOBREGAT23
from .uscf_old import USCF_OLD
from .andorra import ANDORRA

models: dict[ModelID, SheetModel] = {
  'fcde': FCDE,
  'llobregat23': LLOBREGAT23,
  'uscf-old': USCF_OLD,
  'andorra': ANDORRA,
}