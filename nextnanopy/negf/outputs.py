import os

import numpy as np

from nextnanopy.outputs import DataFile as _DataFile
from nextnanopy.outputs import resolve_loader


def get_loader(extension, filename_only):
    return resolve_loader(extension, filename_only, product="nextnano.NEGF")


class DataFile(_DataFile):
    """Backwards-compatible alias for nextnanopy.DataFile(..., product='nextnano.NEGF')."""

    def __init__(self, fullpath, **loader_kwargs):
        super().__init__(fullpath, product="nextnano.NEGF", **loader_kwargs)


def get_iv(path=""):
    piv = os.path.join(path, "Current_vs_Voltage.dat")
    return np.loadtxt(piv, skiprows=1, delimiter="\t", unpack=True)


def get_WannierStark_on(folder):
    ws = np.loadtxt(
        os.path.join(folder, "WannierStark", "WannierStark_statesOn.dat"),
        skiprows=2,
        delimiter="\t",
        unpack=True,
    )
    return ws


def get_WannierStark(folder):
    ws = np.loadtxt(
        os.path.join(folder, "WannierStark", "WannierStark_states.dat"),
        skiprows=2,
        delimiter="\t",
        unpack=True,
    )
    return ws


def get_WannierStark_norm(folder, scaling_factor=1):
    ws = np.loadtxt(
        os.path.join(folder, "WannierStark", "WannierStark_states.dat"),
        skiprows=2,
        delimiter="\t",
        unpack=True,
    )
    norm = min(ws[1])
    z = ws[0]
    pot = ws[1] - norm
    ws_norm = ws[2:] - norm
    ws_norm_scal = scale_wf(ws_norm, scaling_factor)
    return z, pot, ws_norm_scal


def get_WannierStark_norm_cpp(folder, scaling_factor=1):
    ws = np.loadtxt(
        os.path.join(folder, "EnergyEigenstates", "EigenStates.dat"),
        skiprows=2,
        delimiter="\t",
        unpack=True,
    )
    norm = min(ws[1])
    z = ws[0]
    pot = ws[1] - norm
    ws_norm = ws[2:] - norm
    ws_norm_scal = scale_wf(ws_norm, scaling_factor)
    return z, pot, ws_norm_scal


def scale_wf(wf_input, factor):
    scaled = np.copy(wf_input)
    for i, cur in enumerate(wf_input):
        mi = min(cur)
        ma = max(cur)
        scaled[i] = np.interp(cur, [mi, ma], [mi, factor * (ma - mi) + mi])

    return scaled
