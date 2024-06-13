from xurpas_data_quality.data.descriptions import TableDescription
from xurpas_data_quality.render.renderer import HTMLBase, HTMLContainer, HTMLTable, HTMLVariable, HTMLPlot, HTMLToggle, HTMLCollapse, HTMLDropdown
from xurpas_data_quality.visuals import plot_to_base64, create_tiny_histogram, create_histogram, create_distribution_plot, create_heatmap, create_interaction_plot
from xurpas_data_quality.render.render import render_report

from dataclasses import fields

def get_detailed_variable_info(df, key:str, variables:dict):
    details = variables['details']
    bottom = [            
        HTMLContainer(
            type="default",
            name="Statistics",
            id= "stats",
            container_items= [
                HTMLContainer(
                    type="column",
                    container_items=
                        HTMLTable(
                            data=details[0],
                            name="Quantile Statistics"
                        )
                    
                ),
                HTMLContainer(
                    type="column",
                    container_items=
                        HTMLTable(
                            data=details[0],
                            name="Descriptive Statistics"
                        )
                )
            ]
        ),
        HTMLPlot(
            name="Histogram",
            type="large",
            id="histo",
            plot=plot_to_base64(create_histogram(df[key]))
        ),
        HTMLTable(
            id = f"{key}-common_values",
            name = "Common Values",
            data= variables["common"].to_html(classes="table table-sm", border=0)),
        HTMLContainer(
            type="tabs",
            name="Extreme Values",
            container_items=[
                HTMLTable(
                    id = f"{key}-min-values",
                    name="Minimum 10 Values",
                    data=variables["min"].to_html(classes="table table-sm", border=0)
                ),
                HTMLTable(
                    id = f"{key}-max-values",
                    name="Maximum 10 Values",
                    data=variables["max"].to_html(classes="table table-sm", border=0)
                )
            ]
        )
    ]
    if df[key].dtype != 'object':
        bottom.append(            
            HTMLPlot(
                name="Distribution",
                id="distribution",
                type="large",
                plot=plot_to_base64(create_distribution_plot(df[key]))
            ))
    return HTMLContainer(
        type="tabs",
        col=key,
        container_items=bottom
    )

def get_variable_data(data: TableDescription) -> list:
    variables = []

    for key, value in data.variables.items():
        split_dict = lambda d: (dict(list(d.items())[:len(d)//2]), dict(list(d.items())[len(d)//2:]))
        table_1, table_2 = split_dict(value['overview'])

        variable_body = {
            'table_1':HTMLTable(table_1),
            'table_2':HTMLTable(table_2),
            'plot': HTMLPlot(plot=plot_to_base64(create_tiny_histogram(data.df[key])))
        }
        btn = HTMLToggle("More details", key)
        variables.append(
                    HTMLVariable(
                        name=key,
                        body = variable_body,
                        bottom = HTMLCollapse(btn, 
                                              get_detailed_variable_info(data.df,
                                                                         key,
                                                                         data.variables[key]))
                    )
                )
    
    return variables

def get_interactions(data:TableDescription):
    df = data.df.select_dtypes(exclude=['object'])
    outer_tabs = []
    for column in df.columns:
        inner_tabs = []
        for inner_col in df.columns:
            inner_tabs.append(
                HTMLContainer(
                    type="default",
                    name= inner_col,
                    id = f"{column}-{inner_col}-interaction-inner",
                    container_items = [HTMLPlot(
                        plot= plot_to_base64(create_interaction_plot(df[inner_col],df[column])),
                        type = "large",
                        name = f"{column}-{inner_col} Interaction Plot",
                        id = f"{column}-{inner_col}_interaction_plot"
                    )]
                )
            )
        outer_tabs.append(
            HTMLContainer(
                type="tabs",
                name = column,
                id = f"{column}-interaction-outer",
                container_items = inner_tabs
            )
        )
    return outer_tabs

def get_report(data: TableDescription,minimal:bool, name:str=None):
    report = render_report(data=data, report_name=name, minimal=minimal)
    return report


def get_report_old(data: TableDescription, name:str=None)-> HTMLBase:
    content = []
    overview_section = HTMLContainer(
        type="box",
        name="Overview",
        container_items = [
            HTMLContainer(
                type="column",
                container_items = HTMLTable(
                    data=data.df_statistics,
                    name="Dataset Statistics"
                )),
            HTMLContainer(
                type="column",
                container_items =  HTMLTable(
                    data=data.var_types,
                    name="Variable Types"
                )
            )
        ]
    )
    dropdown = [HTMLDropdown(
        dropdown_items= list(data.df),
        dropdown_content= HTMLContainer(
            type="default",
            container_items=get_variable_data(data)),
        id="variables-dropdown"
    )]
    variables_section = HTMLContainer(
        type="box",
        name="Variables",
        container_items = dropdown
    )

    corr_df = data.df.corr(numeric_only=True).round(3)
    correlation = HTMLContainer(
        type="box",
        name="Correlation",
        container_items=[
            HTMLContainer(
                type="tabs",
                container_items=[
                    HTMLPlot(plot=plot_to_base64(create_heatmap(corr_df)),
                             type="large",
                             id="corr",
                             name="Heatmap"),
                    HTMLTable(
                        id='sample',
                        name="Table",
                        data=corr_df.to_html(classes="table table-sm", border=0))
                ]
            )
        ]
    )

    samples = HTMLContainer(
        type="box",
        name="Sample",
        container_items=[
            HTMLTable(
                id = "sample",
                data=data.df.head(10).to_html(classes="table table-sm", border=0)
            )
        ]
    )

    interactions = HTMLContainer(
        type="box",
        name="Interactions",
        container_items=[
            HTMLContainer(
                type="tabs",
                container_items= get_interactions(data)
            )
        ]
    )

    """    distribution = HTMLContainer(
            type="box",
            name="Distribution",
            container_items=[
                HTMLPlot(
                    plot= plot_to_base64(create_distribution_from_dataframe(data.df)),
                    type="large"
                )
            ]
        )"""
    
    content.extend([
        overview_section,
        variables_section,
        correlation,
        interactions,
        samples
    ])

    body = HTMLContainer(
        type="sections",
        container_items = content,
    )
    
    if name is not None:
        return HTMLBase(
            body=body,
            name=name
        )
    
    else:
        return HTMLBase(
            body=body
        )