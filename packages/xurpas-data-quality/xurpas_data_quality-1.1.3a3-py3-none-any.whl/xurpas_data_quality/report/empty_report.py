import pandas as pd
from xurpas_data_quality.render.renderer import HTMLBase, HTMLContainer, HTMLTable

def get_empty_report(df: pd.DataFrame, name:str)-> HTMLBase:
    """
    Generates an empty report
    """

    content = [
        HTMLContainer(
            type="box",
            name="Sample",
            container_items=[
                HTMLTable(
                    id = "sample",
                    data=df.to_html(classes="table table-sm", border=0)
                )
            ]
        )
    ]
    body = HTMLContainer(type="sections",
                         container_items = content)

    if name is not None:
        return HTMLBase(
            body=body,
            name=name
        )
    
    else:
        return HTMLBase(
            body=body
        )