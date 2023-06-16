from dataclasses import dataclass
import numpy as np
import pickle
from scipy import interpolate


@dataclass
class MosOp:
    """ A class that stores data relevant to the operating point of a MOS
    transistor. Specifically the following are stored:
        - VGS
        - VDS
        - VBS
        - Gm
        - Gmb
        - Gds
        - Cgs, Cgd, Cgb
        - Cds, Cdb
        - Csb
    """
    vbs: float
    vds: float
    vgs: float
    igs: float
    ids: float


class MosChar:

    def __init__(self, filename, dataset):
        if filename is None and dataset is None:
            raise ValueError("Must provide either a file name or dataset")
        if filename is None:
            self._dataset = dataset
        else:
            self._dataset = pickle.load(open(filename, "rb"))

        self._min_vbs = min(self._dataset['vbs'])
        self._max_vbs = max(self._dataset['vbs'])
        self._min_vgs = min(self._dataset['vgs'])
        self._max_vgs = max(self._dataset['vgs'])
        self._min_vds = min(self._dataset['vds'])
        self._max_vds = max(self._dataset['vds'])
        breakpoint()
        self.char_freq = self._dataset['params']['sp_freq']
        self._splines_map = {}
        self._interpolate_dataset()

    def _interpolate_dataset(self):
        """
        Internal method that interpolates the dataset and sets up
        the data necessary for lookup
        """
        self._interpolate_dc_data()
        self._interpolate_sp_data()

    def _get_ss_params_from_y_params(y_params):
        w = 2 * np.pi * self.char_freq
        gm = (y_params[1, 0].real - y_params[2, 0].real) / 2
        gds = (y_params[1, 1].real - y_params[2, 1].real) / 2
        gb = (y_params[2, 2].real - y_params[1, 2].real) / 2

        cgd12 = -y_params[0, 1].imag / w
        cgd21 = -y_params[1, 0].imag / w
        cgs12 = -y_params[0, 2].imag / w
        cgs21 = -y_params[2, 0].imag / w
        cds23 = -y_params[1, 2].imag / w
        cds32 = -y_params[2, 1].imag / w
        cgg = y_params[0, 0].imag / w
        cdd = y_params[1, 1].imag / w
        css = y_params[2, 2].imag / w

        cgd = (cgd12 + cgd21) / 2
        cgs = (cgs12 + cgs21) / 2
        cds = (cds12 + cds21) / 2
        return dict(gm=gm, gds=gds, gb=gb, cgg=cgg, cdd=cdd, css=css, cgs=cgs,
                cds=cds, cgd=cgd)


    def _interpolate_sp_data(self):
        """
        Internal method that interpolates the s-parameter data.
        For every characterized vbs value, a spline is created across
        vgs and vds. This calculates gm, gds, gb, and all the caps
        """
        vbs = self._dataset['vbs']
        vgs = self._dataset['vgs']
        vds = self._dataset['vds']
        arr_shape = (len(vbs), len(vgs), len(vds))
        out_vars = ['gm', 'gds', 'gb', 'cgg', 'cdd', 'css', 'cgd', 'cgs', 'cds']
        out_dict = {k: np.zeros(shape) for k in out_vars}
        for i in range(len(vbs)):
            for j in range(len(vgs)):
                for k in range(len(vds)):
                    params = self._get_ss_params_from_y_params(
                        self._dataset['y_params'][i, j, k])
                    for k, v in params.items():
                        out_dict[k][i, j, k] = v

        for k, v in out_dict.items():
            self._splines_map[k] = [interpolate.RectBivariateSpline(
                vgs, vds, v[i, :, :]) for i in range(len(vbs))]

    def _interpolate_dc_data(self):
        """
        Internal method that interpolates the DC data
        For every characterized vbs value, a spline is created across vgs and
        vds. During queries, the splines are linearly interpolated for the vbs
        value
        """
        vbs = self._dataset['vbs']
        vgs = self._dataset['vgs']
        vds = self._dataset['vds']
        ids = self._dataset['ids']
        igs = self._dataset['igs']
        self._ids_splines = [interpolate.RectBivariateSpline(
            vgs, vds, ids[i, :, :]) for i in range(len(vbs))]
        self._igs_splines = [interpolate.RectBivariateSpline(
            vgs, vds, igs[i, :, :]) for i in range(len(vbs))]

    def _lin_interp(self, x, x0, x1, y0, y1):
        return y0 + (y1 - y0) / (x1 - x0) * (x - x0)

    def _get_interp_value(self, spline_list, vgs, vds, vbs, dvgs=0, dvds=0):
        """
        Interpolate a spline across vgs, vds, vbs.
        The RectBivariateSplines are across VGS and VDS; one spline is provided
        per vbs point. The output is linearly interpolated across vbs
        """
        vbs_vals = self._dataset['vbs']
        low_idx = 0
        high_idx = 0
        for idx, char_pt in enumerate(vbs_vals):
            if char_pt >= vbs:
                low_idx = idx - 1
                high_idx = idx
                break
        else:
            raise ValueError("vbs value not within range")
        return self._lin_interp(
            vbs, vbs_vals[low_idx], vbs_vals[high_idx],
            spline_list[low_idx](vgs, vds, dx=dvgs, dy=dvds),
            spline_list[high_idx](vgs, vds, dx=dvgs, dy=dvds))

    def _validate_voltages(self, vbs, vds, vgs):
        """ Ensure that the vgs, vds, and vbs are within characterization"""
        if self._min_vbs > vbs or vbs > self._max_vbs:
            raise ValueError(
                f"VBS={vbs} outside of range [{self._min_vbs},{self._max_vbs}]")
        if self._min_vgs > vgs or vgs > self._max_vgs:
            raise ValueError(
                f"VGS={vgs} outside of range [{self._min_vgs},{self._max_vgs}]")
        if self._min_vds > vds or vds > self._max_vds:
            raise ValueError(
                f"VDS={vds} outside of range [{self._min_vds},{self._max_vds}]")

    def get_op(self, vgs, vds, vbs):
        self._validate_voltages(vbs, vgs, vds)
        igs = self._get_interp_value(self._igs_splines, vgs, vds, vbs)
        ids = self._get_interp_value(self._ids_splines, vgs, vds, vbs)
        return MosOp(vbs, vds, vgs, igs, ids)

    def save_dataset(self, filename):
        pickle.dump(self._dataset, open(filename, "wb"))

