from hqm.tools.utility import read_root
from hqm.tools.utility import get_project_root
from hqm.tools.utility import plot1d
from hqm.part_reco.convolution_shape import get_correction_right_CB
from hqm.part_reco.convolution_shape import load_pdf
from hqm.tools.selection import selection
import zfit
import hist
import awkward as ak
import mplhep
import matplotlib.pyplot as plt
import os
from logzero import logger
import numpy as np


def get_data(q2, mass="normal", trigger="ETOS"):
    root_path = get_project_root() + f"root_sample/v6/bdpsi2kst/v10.21p2/2018_{trigger}/{q2}_{mass}.root"
    data_array = read_root(root_path, trigger)

    kind = "ee" if trigger == "ETOS" else "mm"
    bdt_cmb = selection[kind]["bdt_cmb"][trigger]
    bdt_prc = selection[kind]["bdt_prc"][trigger]

    pid = selection["ee"]["pid"]

    total_cut = bdt_cmb & bdt_prc & pid if trigger == "ETOS" else bdt_cmb & bdt_prc
    data_array = total_cut.apply(data_array)

    return data_array


def get_convolution_shape(correction_function):
    data_array = get_data("psi2", "nomass", "MTOS")
    plot_path = get_project_root() + "output/check/part_reco/Bd2Kspsi2S_MC_highq2_check/latest/psi2q2.pdf"
    plot1d(ak.to_numpy(data_array["B_M"]), 100, "B_M", plot_path)

    data_hist = hist.Hist.new.Regular(100, 4000, 6000, name="B_M", flow=False).Double()
    data_hist.fill(ak.to_numpy(data_array["B_M"]))

    hist_pdf = zfit.pdf.HistogramPDF(data_hist)
    unbinned_pdf = zfit.pdf.SplinePDF(hist_pdf, obs=zfit.Space("B_M", limits=(3000, 7000)))
    convolution_shape = zfit.pdf.FFTConvPDFV1(
        func=unbinned_pdf, kernel=correction_function, name=f"convolution_shape", n=1000
    )

    return convolution_shape


def get_correction_function():
    kind = "psi2S_high"
    year = "2018"
    trigger = "ETOS"

    obs_kernel = zfit.Space("B_M", limits=(-800, 1200))
    name = f"{kind}_{year}_{trigger}"

    correction_function = get_correction_right_CB(obs_kernel, name)
    pickle_path = f"data/part_reco/fit_convolution/latest/{kind}/{year}_{trigger}/fit_result.pickle"
    correction_function = load_pdf(pickle_path, correction_function)
    for param in correction_function.get_params():
        param.floating = False

    return correction_function


def compare_convolution_shape():
    highq2_data = get_data("high")
    nbins = 100
    highq2_hist = hist.Hist.new.Regular(nbins, 4500, 6000, name="B_M", flow=False).Double()
    highq2_hist.fill(ak.to_numpy(highq2_data["B_M"]))

    convolution_shape = get_convolution_shape(get_correction_function())

    plt.figure()
    mplhep.histplot(highq2_hist, label="MC high-q2", color="black", histtype="errorbar", yerr=True)

    x = np.linspace(4500, 6000, 2000)
    y = convolution_shape.pdf(x, norm=(4500, 6000)) * highq2_hist.sum() / nbins * (6000 - 4500)
    plt.plot(x, y, label="convolution_shape", color="red")

    plt.legend()

    plot_path = (
        get_project_root() + "output/check/part_reco/Bd2Kspsi2S_MC_highq2_check/latest/compare_convolution_shape.pdf"
    )
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    logger.info(f"Saving plot to {plot_path}")
    plt.savefig(plot_path)
    plt.close()


def main():
    compare_convolution_shape()


if __name__ == "__main__":
    main()
