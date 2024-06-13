import zfit
from hqm.tools.utility import get_project_root
from hqm.tools.utility import read_root
from hqm.check.part_reco.psi2S_region import FullyRecoYield
from hqm.check.part_reco.psi2S_region import get_KDE_shape
from hqm.part_reco.convolution_shape import get_convolution_shape
import awkward as ak
import hist
import matplotlib.pyplot as plt
import numpy as np
import mplhep
from logzero import logger
import os
import argparse


def plot(data_array, total_model, mass_window, path, nbins=100):
    data_hist = hist.Hist.new.Regular(nbins, mass_window[0], mass_window[1], overflow=False, name="B_M").Double()
    data_hist.fill(data_array.B_M)

    plt.figure()
    mplhep.histplot(data_hist, yerr=True, histtype="errorbar", color="black", label="data")
    x = np.linspace(mass_window[0], mass_window[1], 2000)
    previous_y = None
    for pdf in total_model.pdfs:
        pdf_yield = zfit.run(pdf.get_yield())
        print(pdf, pdf_yield, pdf.name)
        y = pdf.pdf(x) * (mass_window[1] - mass_window[0]) / nbins * pdf_yield
        if previous_y is None:
            plt.fill_between(x, y, label=pdf.name)
            previous_y = y
        else:
            plt.fill_between(x, previous_y, previous_y + y, label=pdf.name)
            previous_y += y
    plt.legend()
    plt.xlim(mass_window)
    plt.ylim(bottom=0)
    logger.info(f"saving plot to {path}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.savefig(path)
    plt.close()


def get_nll(obs, q2, shared_parameters):
    _name = {"jpsi": "Jpsi", "psi2": "psi2S"}

    psi2S_part_reco_shape, _psi2S_ratio, _ = get_convolution_shape(f"psi2S_{_name[q2]}", "2018", "ETOS")
    Jpsi_part_reco_shape, _Jpsi_ratio, _ = get_convolution_shape(f"Jpsi_{_name[q2]}", "2018", "ETOS")
    logger.info(f"muon psi2S_ratio: {_psi2S_ratio}")
    logger.info(f"muon Jpsi_ratio: {_Jpsi_ratio}")
    for param in psi2S_part_reco_shape.get_params():
        param.floating = False
    for param in Jpsi_part_reco_shape.get_params():
        param.floating = False

    JpsiK_shape = get_KDE_shape(obs, "jpsi", q2, "JpsiK")
    psi2SK_shape = get_KDE_shape(obs, "psi2", q2, "psi2SK")

    mass_window = obs.limit1d
    psi2S_mass_window_factor = psi2S_part_reco_shape.integrate(mass_window)[0] / psi2SK_shape.integrate(mass_window)[0]
    Jpsi_mass_window_factor = Jpsi_part_reco_shape.integrate(mass_window)[0] / JpsiK_shape.integrate(mass_window)[0]
    print(f"psi2S_mass_window_factor: {psi2S_mass_window_factor}")
    print(f"Jpsi_mass_window_factor: {Jpsi_mass_window_factor}")

    psi2S_part_reco_shape.set_norm_range(mass_window)
    Jpsi_part_reco_shape.set_norm_range(mass_window)

    data_cut = FullyRecoYield.data_pid & FullyRecoYield.bdt_cmb & FullyRecoYield.normal_mass & FullyRecoYield.bdt_prc
    data_path = get_project_root() + f"root_sample/v6/data/v10.21p2/2018_ETOS/{q2}_nomass.root"
    data_array = read_root(data_path, "ETOS")
    data_array = data_cut.apply(data_array)

    suffix = q2
    psi2SK_yield = zfit.Parameter(f"psi2SK_yield_{suffix}", FullyRecoYield.get("psi2", q2), 0, 1e8)
    JpsiK_yield = zfit.Parameter(f"JpsiK_yield_{suffix}", FullyRecoYield.get("jpsi", q2), 0, 1e8)
    psi2S_part_reco_yield = zfit.param.ComposedParameter(
        f"psi2S_ratio_reco_yield_{suffix}",
        lambda p: p["a"] * p["b"] * p["c"],
        {"a": shared_parameters["psi2S_ratio"], "b": psi2S_mass_window_factor, "c": psi2SK_yield},
    )
    Jpsi_part_reco_yield = zfit.param.ComposedParameter(
        f"Jpsi_part_reco_yield_{suffix}",
        lambda p: p["a"] * p["b"] * p["c"],
        {"a": shared_parameters["Jpsi_ratio"], "b": Jpsi_mass_window_factor, "c": JpsiK_yield},
    )

    psi2S_part_reco_shape.set_yield(psi2S_part_reco_yield)
    Jpsi_part_reco_shape.set_yield(Jpsi_part_reco_yield)
    psi2SK_shape.set_yield(psi2SK_yield)
    JpsiK_shape.set_yield(JpsiK_yield)

    # psi2SK_yield.floating = False
    # JpsiK_yield.floating = False

    total_model = zfit.pdf.SumPDF(
        [psi2S_part_reco_shape, Jpsi_part_reco_shape, psi2SK_shape, JpsiK_shape], obs=obs, name="total_model"
    )
    zdata = zfit.Data.from_numpy(obs=obs, array=ak.to_numpy(data_array.B_M))

    # binning = zfit.binned.RegularBinning(100, mass_window[0], mass_window[1], name="B_M")
    # binned_obs = zfit.Space(obs=obs.obs[0], limits=mass_window, binning=binning)

    # total_model_binned = total_model.to_binned(binned_obs)
    # zdata_binned = zfit.data.BinnedData.from_unbinned(binned_obs, zdata)

    nll = zfit.loss.ExtendedUnbinnedNLL(model=total_model, data=zdata)
    # nll = zfit.loss.ExtendedBinnedNLL(model=total_model_binned, data=zdata_binned)
    return nll, data_array, total_model


def main(dataset):
    mass_window = (4500, 6000)
    obs = zfit.Space("B_M", limits=mass_window)

    psi2S_ratio = zfit.Parameter(f"psi2S_ratio_{dataset}", 2, 0.1, 10)
    Jpsi_ratio = zfit.Parameter(f"Jpsi_ratio_{dataset}", 2, 0.1, 10)

    shared_parameters = {
        "psi2S_ratio": psi2S_ratio,
        "Jpsi_ratio": Jpsi_ratio,
    }
    nll1, data_jpsi, total_model_jpsi = get_nll(obs, "jpsi", shared_parameters)
    nll2, data_psi2, total_model_psi2 = get_nll(obs, "psi2", shared_parameters)
    nll = nll1 + nll2

    minimizer = zfit.minimize.Minuit()
    result = minimizer.minimize(nll)
    result.hesse()
    print(result)

    plot_path = get_project_root() + f"output/check/part_reco/simultaneous_fit/latest/simultaneous_fit_jpsi_{dataset}.pdf"
    plot(data_jpsi, total_model_jpsi, mass_window, plot_path)
    plot_path = get_project_root() + f"output/check/part_reco/simultaneous_fit/latest/simultaneous_fit_psi2_{dataset}.pdf"
    plot(data_psi2, total_model_psi2, mass_window, plot_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--dataset" type=str, help="dataset", default="2018")
    args = parser.parse_args()
    main(args.dataset)
