import os
from typing import Tuple

import numpy as np

import scipy
import xarray as xr
import rioxarray
from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from feature_engine.discretisation import EqualWidthDiscretiser
from feature_engine.wrappers import SklearnTransformerWrapper

from skimage.segmentation import quickshift
from sklearn.preprocessing import MinMaxScaler, RobustScaler

from rote_satio.models.segmentatition.planet.dispatcher import PlanetPipeline
from rote_satio.utils.geobia_transformer import SegmentsTransformer
from rote_satio.utils.index_transformer import IndexTransformer
from rote_satio.utils.utils import parse_to_pandas


class AutoSegmentation():
    def __init__(
            self,
            image_path: str,
            image_program: str,
            generate_objects: bool = True,
    ):
        """
        Args:
            image_path: Path to the image that needs to be segmented.
            image_program: Program of the sensor of the image.
            generate_objects: If True, there will be generation of geobias objects.

        Returns:
            self (AutoSegmentation): And AutoSegmentation object with the given image_path and image_program
                that can be used to perform segmentation on the image.
        """
        self._check_input(image_path, image_program)
        self.image_path = image_path
        self.image_program = image_program
        self.generate_objects = generate_objects
        self.umap_pipeline = None
        self.hdbscan_pipeline = None


    def predict(self):
        """
        Predicts the segmentation of the image. Using a pre-trained model.
        Returns:
            xr.DataArray: DataArray of the predicted labels.

        """
        self._read_image()
        self._generate_indexes()
        if self.generate_objects:
            self._generete_segments()
        df = parse_to_pandas(self.image)
        pipeline = PlanetPipeline()
        labels = pipeline.predict(df)
        return self._convert_to_xarray(labels)


    def train(self, values: Tuple[int, int] = (5, 50)):
        """
        Trains a models to segment the image. It uses kmeans to segment the image and uses
        the elbow method to find the best number of clusters.
        Args:
            values: A tuple with the range of number of clusters to test.

        Returns:
            self (AutoSegmentation): DataArray of the predicted labels.

        """
        self._read_image()
        self._generate_indexes()
        if self.generate_objects:
            self._generete_segments()
        df = parse_to_pandas(self.image)
        number_clusters = np.arange(values[0], values[1])
        pipeline = Pipeline([
            ('scaler', SklearnTransformerWrapper(transformer=MinMaxScaler())),
            ('robust_scaler', SklearnTransformerWrapper(transformer=RobustScaler())),
            ('scaler_2', SklearnTransformerWrapper(transformer=MinMaxScaler())),
            ('discretizer', EqualWidthDiscretiser(bins=10)),
            ('scaler_3', SklearnTransformerWrapper(transformer=MinMaxScaler())),
        ])
        df = pipeline.fit_transform(df)

        inertia_list = []

        for num_clust in number_clusters:
            kmeans = KMeans(n_clusters=num_clust, random_state=42, max_iter=1000, init='k-means++')
            kmeans.fit(df)
            inertia_list.append(kmeans.inertia_)
        kneedle = KneeLocator(
            number_clusters,
            inertia_list,
            curve='convex',
            direction='decreasing'
        )
        best_k = kneedle.elbow
        kmeans = KMeans(n_clusters=best_k, random_state=42, max_iter=1000, init='k-means++')
        kmeans.fit(df)
        labels = kmeans.predict(df)
        return self._convert_to_xarray(labels)


    def _convert_to_xarray(self, labels):
        labels = labels.reshape(self.image.shape[1], self.image.shape[2])
        segments = quickshift(
            labels,
            kernel_size=1,
            convert2lab=False,
            max_dist=2,
            ratio=1.0

        )
        labels = scipy.ndimage.median(
            input=labels,
            labels=segments,
            index=segments
        )

        labels = np.expand_dims(labels, axis=0)
        labels = xr.DataArray(
            data=labels,
            dims=['band', 'y', 'x'],
            coords={
                'band': ['labels'],
                'y': self.image.y.data,
                'x': self.image.x.data,
            },
            attrs={'long_name': ['labels']}
        )
        labels = labels.rio.write_crs(self.image.rio.crs)
        return labels

    def _check_input(self, image_path: str, image_program: str):
        """
        Args:
            image_path: Path to the image that needs to be segmented.
            image_program: Program of the sensor of the image.

        Returns:
            None
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")

        if image_program not in ["Planet"]:
            raise ValueError(f"Invalid image program {image_program}. Supported programs are ['Planet']")

        if image_program is None:
            raise ValueError("Image program cannot be None")


    def _read_image(self) -> xr.Dataset:
        """
        Reads and returns the image from the image_path.
        Args:
            None

        Returns:
            xr.DataArray: DataArray of the image read from the image_path.
        """
        self.image = rioxarray.open_rasterio(self.image_path, engine='rasterio')



    def _generate_indexes(self):
        """
        Generates indexes from the image.
        Args:
            None

        Returns:
            None
        """
        index_transformer = IndexTransformer(program=self.image_program)
        self.image = index_transformer.transform(self.image)


    def _generete_segments(self):
        """
        Generates segments from the image.
        Args:
            None

        Returns:
            None
        """
        segments_transformer = SegmentsTransformer()
        self.image = segments_transformer.transform(self.image)




