import warnings
import pandas as pd

from visions import Integer, Float, Date, DateTime

from xurpas_data_quality.data import get_series_descriptions, get_correlations
from xurpas_data_quality.data.describer import TableDescription
from xurpas_data_quality.data import XTypeSet

warnings.filterwarnings('ignore', category=UserWarning)

def get_variable_type_counts(variable_types: dict)-> dict:
    value_counts = {}
    for _, value in variable_types.items():
        if value ==Integer or value==Float:
            value = 'Numerical'
        if value == Date or value==DateTime:
            value = 'Date'
        if value in value_counts:
            value_counts[value] += 1
        else:
            value_counts[value] = 1

    return value_counts
    

def get_overview(df: pd.DataFrame, data_types:dict=None) -> dict:
    """
    Get the overview statistics of the DataFrame.

    Args:
        df: the DataFrame object
    
    Retunr:
        dictionary object containing the table statistics
    """
    num_variables = len(df.columns)
    missing_cells = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()

    if data_types is not None:
        v_types = data_types

        for column in df.columns: # updates the v_types dict with the columns that are not user given data types
            if column not in v_types:
                v_types[column] = XTypeSet.infer_type(df[column])

    else:
        v_types = XTypeSet.infer_type(df)

    dataset_stats = {
        "dataset_statistics": {
            'num_variables': num_variables,
            'missing_cells': missing_cells,
            'missing_cells_perc' : (missing_cells/df.count().sum())*100,
            'duplicate_rows': duplicate_rows,
            'duplicate_rows_perc': (duplicate_rows/len(df))*100,
            'total_memory': df.memory_usage().sum(),
            'ave_memory': df.memory_usage().sum()/len(df)
            },
        'variable_types': get_variable_type_counts(v_types)
    }

    return dataset_stats

def describe(df: pd.DataFrame, data_types:dict=None)-> TableDescription:
    """Gets Description of DataFrame which includes
    an overview, its correlations, and variable descriptions
    
    Args
        df: dataframe to be described

    Returns
        a class containing all the descriptions
    """

    correlation = get_correlations(df)
    if data_types is None:
        overview = get_overview(df)
        variables = get_series_descriptions(df)
    else:
        overview = get_overview(df, data_types)
        variables = get_series_descriptions(df, data_types)

    data = TableDescription(df=df, variables=variables, correlation=correlation, **overview)

    return data