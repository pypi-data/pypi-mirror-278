import pathlib

import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize

from . import CellPhase, ChannelCountsProblem, PatchClampData, PatchClampProtocol, setup_logging
from .utils import moving_average

RESULTS = pathlib.Path.cwd()
setup_logging()


def plot_measurement():
    fig = plt.figure()
    axes: matplotlib.axes.Axes = fig.add_subplot(1, 1, 1)
    axes.plot()
    axes.set_xlabel("")
    axes.set_ylabel("")
    axes.legend()
    fig.savefig(str(RESULTS / "plot.pdf"))


def plot_full_comparison(method="nnls", n=800):
    measurements = PatchClampData.pyload(PatchClampProtocol.Activation, CellPhase.G0)
    data = moving_average(np.array(measurements.to_list()), n)
    # data = np.array(measurements.to_list())[::12]
    problem = ChannelCountsProblem.new(measurements)
    problem.precompute_single_channel_currents()
    single_channels = moving_average(np.array(problem.get_current_basis()), n)
    # single_channels = np.array(problem.get_current_basis())[:, (3,)]
    # single_channels = np.concatenate([single_channels, np.ones((single_channels.shape[0], 1))], axis=1)
    if method == "lstsq":
        channel_counts, res, rank, s = np.linalg.lstsq(single_channels[: len(data), :], data, rcond=None)
    elif method == "nnls":
        channel_counts, rnorm = scipy.optimize.nnls(single_channels[: len(data), :], data)
    elif method == "langthaler":
        channel_counts = np.array([22, 78, 5, 1350, 40, 77, 19, 200, 17, 12, 13])
    channel_counts = channel_counts.astype(int)
    time = np.linspace(0, 9.901, single_channels.shape[0])
    print(f"Best fit: {channel_counts}")

    fig = plt.figure(figsize=(8, 4))
    axes: matplotlib.axes.Axes = fig.add_subplot(1, 1, 1)
    axes.plot(time[: len(data)], data, label="Measurements")
    axes.plot(time, (single_channels * channel_counts).sum(axis=1), label="Simulation")
    axes.set_xlabel("Time $t$ / s")
    axes.set_ylabel("Current $I$ / pA")
    axes.legend()
    fig.savefig(str(RESULTS / "data-vs-simulation.pdf"))


def set_results_folder(path: pathlib.Path):
    global RESULTS
    RESULTS = path
