import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from spyndex import spyndex
from spyndex import constants
import xarray as xr


class IndexTransformer(BaseEstimator, TransformerMixin):
    def __init__(
            self,
            program: str = 'Planet',
            ):
        """
        This is a `spyndex` wrapper to automate the computation of multiple spectral indexes.
        It is heavily based on the `spyndex` package, which is a Python package for the computation of spectral indices
        for more information please visit [spyndex](https://spyndex.readthedocs.io/en/latest/):

        Args:
            program: Program of the sensor of the image. Until 0.0.2beta version only 'Planet' is supported.

        """
        self.program = program
        self.indexes = self.get_indexes()

    def get_indexes(self):
        """
        It returns the indexes supported by the program of the program being used by `spyndex
        Returns:
            List of indexes supported by the program.

        """
        if self.program not in ["Planet"]:
            raise ValueError(f"Invalid image program {self.program}. Supported programs are ['Planet']")
        # skiped indexes due to errors.
        skip_indexes = ['NIRvP', 'kEVI', 'kIPVI', 'kNDVI', 'kRVI', 'kVARI', 'AVI']
        if self.program == 'Planet':
            self.indexes = [
                'ARVI', 'ATSAVI', 'AVI', 'BCC', 'BNDVI', 'BWDRVI', 'bNIRv', 'CIG', 'CVI', 'DSWI4', 'DVI',
                'EBI', 'ENDVI', 'EVI', 'EVI2', 'EVIv', 'ExG', 'ExGR', 'ExR', 'FCVI', 'GARI',
                'GBNDVI', 'GCC', 'GDVI', 'GEMI', 'GLI', 'GNDVI', 'GOSAVI', 'GRNDVI', 'GRVI', 'GSAVI', 'IAVI', 'IKAW',
                'IPVI', 'MCARI1', 'MCARI2', 'MGRVI', 'MNLI', 'MRBVI', 'MSAVI', 'MSR', 'MTVI1', 'MTVI2',
                'NDDI', 'NDVI', 'NDYI', 'NGRDI', 'NIRv', 'NIRvP', 'NLI', 'NormG', 'NormNIR',
                'NormR', 'OCVI', 'OSAVI', 'RCC', 'RDVI', 'RGBVI', 'RGRI', 'RI', 'SARVI', 'SAVI', 'SAVI2', 'SEVI',
                'SI', 'SR', 'SR2', 'TDVI', 'TGI', 'TSAVI', 'TVI', 'TriVI', 'VARI', 'VIG', 'WDRVI', 'WDVI', 'NDTI',
                'NDWI', 'NDWIns', 'OSI', 'PI', 'RNDVI', 'BAI', 'NDGlaI', 'NDSII', 'PISI', 'VgNIRBI',
                'VrNIRBI', 'BITM', 'BIXS', 'RI4XS', 'kEVI', 'kIPVI', 'kNDVI', 'kRVI', 'kVARI']

        return [index for index in self.indexes if index not in skip_indexes]

    def transform(self, X: xr.DataArray) -> xr.DataArray:
        """
        It computes the indexes for the input data.
        Args:
            X: Input data.
        Returns
            xr.DataArray: A new DataArray with the indexes computed.
        """
        self._get_params(X)


        idx = spyndex.computeIndex(
            index=self.indexes,
            params=self.params
        )
        idx = xr.where(np.isinf(idx) | np.isnan(idx), 0, idx)
        idx = idx.rename({'index': 'band'})
        idx = xr.concat([X, idx], dim='band')
        idx.attrs['long_name'] = list(X.band.values)
        idx = idx.rio.write_crs(X.rio.crs)
        return idx


    def _get_bands_names(self):
        """
        This function returns the band names for the program being used. Until 0.0.2beta version only 'Planet' is supported.
        Returns:

        """
        if self.program == 'Planet':
            return ['B1', 'B2', 'B3', 'B4']

    def _get_params(self, X: xr.DataArray) -> None:
        """
        Some indexes require parameters to be computed. This function sets the parameters for the indexes.
        Args:
            X: An xarray DataArray with the bands of the image.

        Returns:
            None
        """
        self.params = {
            "gamma": constants.gamma.value,
            "sla": constants.sla.value,
            "slb": constants.slb.value,
            "alpha": constants.alpha.value,
            "g": constants.g.value,
            "C1": constants.C1.value,
            "C2": constants.C2.value,
            "omega": constants.omega.value,
            "L": constants.L.value,
            "nexp": constants.nexp.value,
            "cexp": constants.cexp.value,
            "fdelta": constants.fdelta.value,
            "beta": constants.beta.value,
            "epsilon": constants.epsilon.value,
            "k": constants.k.value,
        }


        if self.program == 'Planet':
            self.params['B'] = X.isel(band=2)
            self.params['R'] = X.isel(band=0)
            self.params['G'] = X.isel(band=1)
            self.params['N'] = X.isel(band=3)



