import numpy as np
from skimage.segmentation import quickshift
from sklearn.base import TransformerMixin, BaseEstimator
import warnings
import xarray as xr
import scipy


class SegmentsTransformer(BaseEstimator, TransformerMixin):
    def __init__(
            self,
            kernel_size: int = 1,
            ):
        """
        This is a `skimage.segmentation.quickshift` wrapper to automate the computation of zonal segments for
        each band of the input data. Each of the zonal segments is computed using the quickshift algorithm. It
        returns and xarray.DataArray with the zonal segments as new bands where each band is named as 'Zonal_{band}'.

        Args:
            kernel_size:  Width of Gaussian kernel used in smoothing the sample density. Higher means fewer clusters.
                for more info: https://scikit-image.org/docs/dev/api/skimage.segmentation.html#skimage.segmentation.quickshift
        Returns:
            xarray.DataArray: A new DataArray with the zonal segments computed.
        """
        self.kernel_size = kernel_size

    def fit(self, X: xr.DataArray, y=None):
        warnings.warn("This transformer does not need to be fitted. It will return self.", FutureWarning)
        if not isinstance(X, xr.DataArray):
            raise ValueError(f"X should be of type xarray.DataArray. Got {type(X)}")

        return self

    def transform(self, X: xr.DataArray):
        """
        It computes the zonal segments for the input data.
        Args:
            X: The input data.

        Returns:

        """
        for band in X.band.values:
            if not band.startswith('Zonal'):
                try:
                    band = int(band)
                except ValueError:
                    segments = quickshift(
                        X.sel(band=band).data,
                        kernel_size=self.kernel_size,
                        convert2lab=False,
                        max_dist=1,
                        ratio=1.0
                    )
                    zonal_segments = scipy.ndimage.mean(
                        input=X.sel(band=band).data,
                        labels=segments,
                        index=segments
                    )
                    zonal_segments = zonal_segments[np.newaxis, :, :]
                    zonal_segments_array = xr.DataArray(
                        zonal_segments,
                        dims=['band', 'y', 'x'],
                        coords={
                            'band': [f'Zonal_{band}'],
                            'y': X.y,
                            'x': X.x
                        }
                    )
                    X = xr.concat([X, zonal_segments_array], dim='band')
        X = X.rio.write_crs(X.rio.crs)
        X.attrs['long_name'] = list(X.band.values)
        return X
