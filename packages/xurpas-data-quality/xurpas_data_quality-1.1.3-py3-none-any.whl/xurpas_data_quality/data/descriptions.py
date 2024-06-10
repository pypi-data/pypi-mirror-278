from dataclasses import dataclass
from typing import Any, Dict, Optional

import pandas as pd

@dataclass
class TableDescription:
    df: pd.DataFrame
    df_statistics: Dict
    var_types: Dict
    variables: Dict