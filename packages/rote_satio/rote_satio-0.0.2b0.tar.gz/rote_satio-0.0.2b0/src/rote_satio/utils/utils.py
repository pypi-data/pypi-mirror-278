import xarray as xr
import pandas as pd


def parse_to_pandas(image: xr.DataArray) -> pd.DataFrame:
    """
    Returns as pandas dataframe of the image.
    Args:
        image: xarray.DataArray of the image.

    Returns:
        pd.DataFrame: Pandas dataframe of the image.

    """
    df = image.squeeze().drop_vars("spatial_ref")
    df.name = 'data'
    return df.to_dataframe().unstack('band').reset_index(drop=True)

