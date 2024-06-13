import os
import warnings
from pathlib import Path

import pandas as pd

from xurpas_data_quality.report import get_report, get_empty_report
from xurpas_data_quality.data import check_dtypes, describe, load_dataframe,validate_dataframe ,check_col_names

warnings.filterwarnings("ignore", category=UserWarning, module='visions')

class DataReport:
    def __init__(self, file:str=None, 
                 df:pd.DataFrame=None, 
                 report_name:str="Data Report", 
                 file_path:str="report.html",
                 data_types:dict=None,
                 minimal:bool = True):
        """
        Initializes the DataReport object
        Args
            file:        The path of the file you want to analyze. If empty, df parameter must exist.
                         Only supports .csv, .xlsx, .parquet, and .orc file formats
            df:          Pandas DataFrame object of data to be analyzed, If using df, file must be empty.
            report_name: Name of the report. Defaults to 'Data Report'
            file_path:   Path/ directory of where the report is to be saved
            data_types:  A dictionary containing the column names and their corresponding data types.
                         If empty, then the data types will be inferred.
            minimal:     Default is True. Check if you want minimal mode as your data report.
        """

        if file is not None and df is None:
            self.df = df
        elif file is None and df is not None:
            self.df = df
        elif file is not None and df is not None:
            raise KeyError("Only 'file' or 'df' should be used one at a time!")
        elif file is None and df is None:
            raise ValueError("Please provide your data in 'file' or 'df' parameters!")

        self.render_empty = True if not validate_dataframe(df) else False # checks if dataframe is empty
        self.report_name = report_name
        self.minimal = minimal

        if data_types is not None:
            self.data_types = check_dtypes(check_col_names(data_types, df.columns))
        else:
            self.data_types = None

        def has_extension(file_path:str):
            return os.path.splitext(file_path)[1] != '' 
        if has_extension(file_path):
            self.save_path = file_path
        else:
            self.save_path = '/'.join([file_path,"report.html"])
            warnings.warn("File name not provided, saving as {file_path}/report.html")

    def describe_dataframe(self):
        self.description = describe(df=self.df, data_types=self.data_types)

    def get_data_quality_report(self, minimal:bool,report_name=None):
        self.describe_dataframe()
        report = get_report(self.description, minimal=minimal,name=report_name)
        return report.render()
    
    def _render_empty_report(self, name=None):
        report = get_empty_report(self.df, name)
        return report.render()
    
    def to_file(self, report_name:str=None, file_name:str="report.html"):
        output = Path(self.save_path)

        if self.render_empty:
            print(f"saving empty report as {self.save_path}")
            output.write_text(self._render_empty_report(self.report_name), encoding='utf-8')
            print("saved!")

        else:
            print(f"saving as {self.save_path}")
            if self.minimal:
                print("saving minimal version of report!")
                from minify_html import minify
                minified_report = minify(self.get_data_quality_report(self.minimal, self.report_name))
                output.write_text(minified_report, encoding='utf-8')
            else:
                output.write_text(self.get_data_quality_report(self.minimal, self.report_name), encoding='utf-8')
            
            print(f"saved!")