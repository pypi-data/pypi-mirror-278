import pandas as pd

from kywy.client.kawa_decorators import inputs, outputs


@inputs(pk=int, measure1=float, measure2=float)
@outputs(measure3=float)
def execute(df: pd.DataFrame):
    df['measure3'] = df['measure1'] + df['measure2']
    return df
