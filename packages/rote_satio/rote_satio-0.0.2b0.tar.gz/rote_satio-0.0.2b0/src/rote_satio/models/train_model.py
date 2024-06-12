import glob
import os
from pathlib import Path
import typer
import pandas as pd
import rioxarray
from sklearn.pipeline import Pipeline


from rote_satio.models.segmentatition.planet.dispatcher import PlanetPipeline
from rote_satio.utils.geobia_transformer import SegmentsTransformer
from rote_satio.utils.index_transformer import IndexTransformer
from rote_satio.utils.utils import parse_to_pandas

app = typer.Typer()

def load_data(
        data_folder: str,
        name_regex: str,
        image_program: str,
) -> pd.DataFrame:
    """
    Load the data from the data folder.
    Args:
        name_regex: Regex to match the files.
        data_folder: Path to the data folder.
        image_program: Program of the sensor of the image.

    Returns:
        pd.DataFrame: Dataframe of the data.
    """
    # current file location
    current_file = Path(os.getcwd())
    # root_folder = current_file.parents[2]

    # access the data folder and list the files
    data_folder_path = current_file / data_folder



    # Files that match the regex
    files = glob.glob(str(data_folder_path / name_regex))
    if len(files) == 0:
        raise ValueError(f"No files found in {data_folder_path} with the regex {name_regex}")
    df = pd.DataFrame()
    # Transform the files into a dataframe
    for file in files:
        # read file as xarray
        data_array_file = rioxarray.open_rasterio(file, engine='rasterio')

        # data augmentation though indexes
        index_transformer = IndexTransformer(program=image_program)
        data_array_file = index_transformer.transform(data_array_file)
        geobia_transformer = SegmentsTransformer().fit(data_array_file)
        data_array_file = geobia_transformer.transform(data_array_file)

        # parse to pandas
        df_file = parse_to_pandas(data_array_file)
        df = pd.concat([df, df_file], axis=0)
    return df


def data_reduction(data: pd.DataFrame, data_factor_reduction: float) -> pd.DataFrame:
    """
    Reduce the data by the factor but the reduction is systematic, not random.
    This means that the data is reduced by taking every nth row, which try to keep the data as
    representative as possible.
    Args:
        data: Dataframe of the data to reduce.
        data_factor_reduction: Factor to reduce the data by.

    Returns:
        pd.DataFrame: Reduced dataframe.
    """
    return data.iloc[::int(1/data_factor_reduction)]


def load_dispatcher(program: str, type_model) -> Pipeline:
    """
    Load the dispatcher for the models.
    Args:
        type_model:
        program: Program of the sensor of the image.

    Returns:
        str: Path to the dispatcher.
    """
    if program == 'Planet' and type_model == 'segmentation':
        return PlanetPipeline()
    else:
        raise ValueError(f"Invalid program {program} or type_model {type_model}")

@app.command()
def train_model(
        program: str,
        type_model: str,
        data_folder: str,
        reduce_data=True,
        data_factor_reduction: float = 0.2,
        name_regex: str = '*'
) -> None:
    # Load the data
    data_frame = load_data(
        data_folder=data_folder,
        name_regex=name_regex,
        image_program=program
        )
    if reduce_data:
        data_frame = data_reduction(data_frame, data_factor_reduction)

    # Train the model
    model = load_dispatcher(program, type_model)

    # Save the model
    model.fit(data_frame)


if __name__ == "__main__":
    app()

