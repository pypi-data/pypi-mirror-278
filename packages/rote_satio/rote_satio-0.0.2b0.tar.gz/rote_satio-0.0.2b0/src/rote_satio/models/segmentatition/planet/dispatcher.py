import os
from pathlib import Path

import pandas as pd
from feature_engine.discretisation import EqualWidthDiscretiser
from feature_engine.wrappers import SklearnTransformerWrapper
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, RobustScaler

from hdbscan import HDBSCAN, approximate_predict
from umap import UMAP

from rote_satio.models.utils.utils import save_pipeline, load_pipeline


class PlanetPipeline(Pipeline):
    preprocessing_pipeline_name = 'preprocessing_pipeline.joblib'
    model_name = 'clustering_pipeline.joblib'
    current_file = Path(os.path.dirname(__file__))

    def __init__(self):
        super().__init__([
            ('preprocessing', self._preprocessing_pipeline()),
            ('clustering', self._clustering_pipeline())
        ])


    def _preprocessing_pipeline(self):
        return Pipeline([
            ('robust_scaler', SklearnTransformerWrapper(transformer=RobustScaler())),
            ('scaler', SklearnTransformerWrapper(transformer=MinMaxScaler())),
            ('discretizer', EqualWidthDiscretiser(bins=10)),
            ('scaler_2', SklearnTransformerWrapper(transformer=MinMaxScaler())),
            ('umap', UMAP(n_components=7, n_jobs=-1, n_neighbors=12)),
            ]
        )

    def _clustering_pipeline(self):
        return HDBSCAN(
            min_cluster_size=10,
            min_samples=50,
            gen_min_span_tree=True,
            prediction_data=True,
        )

    def fit(self, X, y=None, **params):
        preprocessing_pipeline = self._preprocessing_pipeline()
        # save columns names to csv
        pd.DataFrame(data = X.columns).to_csv(self.current_file.joinpath('columns.csv'))



        preprocessing_pipeline.fit(X)
        preprocessed = preprocessing_pipeline.transform(X)

        clustered = self._clustering_pipeline()
        clustered.fit(preprocessed)

        preprocessed_location = self.current_file.joinpath(self.preprocessing_pipeline_name)
        pretrain_hdbscan = self.current_file.joinpath(self.model_name)

        save_pipeline(preprocessing_pipeline, preprocessed_location)
        save_pipeline(clustered, pretrain_hdbscan)

        return self

    def predict(self, X):
        # current file location in the package
        current_file = Path(os.path.dirname(__file__))

        preprocessed_pipeline_location = current_file.joinpath(self.preprocessing_pipeline_name)
        pretrain_hdbscan = current_file.joinpath(self.model_name)

        preprocessed_x = load_pipeline(preprocessed_pipeline_location).transform(X)
        clustered_x, strengs = approximate_predict(load_pipeline(pretrain_hdbscan), preprocessed_x)
        return clustered_x
