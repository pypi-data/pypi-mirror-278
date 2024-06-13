from hqm.tools.utility import load_json
from hqm.tools.utility import get_project_root
from hqm.tools.utility import read_root
from hqm.tools.utility import get_lumi
from hqm.tools.selection import selection
from hqm.tools.Cut import Cut
from hqm.part_reco.convolution_shape import get_convolution_shape
from hqm.part_reco.convolution_shape import load_pdf
import zfit
import awkward as ak
from zutils.pdf import SUJohnson
import mplhep
import matplotlib.pyplot as plt
import hist
import numpy as np
import os
from logzero import logger


class FullyRecoYield:
    data_pid = selection["ee"]["pid"]
    bdt_cmb = selection["ee"]["bdt_cmb"]["ETOS"]
    bdt_prc = selection["ee"]["bdt_prc"]["ETOS"]
    jpsi_q2 = Cut(lambda x: (x.Jpsi_M * x.Jpsi_M > 6000000.0) & (x.Jpsi_M * x.Jpsi_M < 12960000.0))
    psi2_q2 = Cut(lambda x: (x.Jpsi_M * x.Jpsi_M > 9920000.0) & (x.Jpsi_M * x.Jpsi_M < 16400000.0))
    high_q2 = Cut(lambda x: (x.Jpsi_M * x.Jpsi_M > 15500000.0) & (x.Jpsi_M * x.Jpsi_M < 22000000.0))
    jpsi_mass = Cut(lambda x: (x.B_M_Jpsi > 5080) & (x.B_M_Jpsi < 5680))
    psi2_mass = Cut(lambda x: (x.B_M_Psi > 4800) & (x.B_M_Psi < 5680))
    normal_mass = Cut(lambda x: (x.B_M > 4500) & (x.B_M < 6000))
    project_root = get_project_root()

    @classmethod
    def get(cls, kind, q2, dataset):
        if kind == "jpsi":
            kind_dir = "ctrl"
        else:
            kind_dir = kind
        if dataset == "all":
            all_datasets = ["r1", "r2p1", "2017", "2018"]
        else:
            all_datasets = [dataset]

        fit_yield = 0
        for ds in all_datasets:
            json_path = (
                f"/publicfs/lhcb/user/campoverde/Data/model/fits/v25/data/v10.21p2/{kind_dir}/{ds}/pars_ETOS.json"
            )
            obj = load_json(json_path)
            fit_yield += obj["nsig_dt"][0]

        q2_cut = {"jpsi": cls.jpsi_q2, "psi2": cls.psi2_q2, "high": cls.high_q2}
        mass_cut = {"jpsi": cls.jpsi_mass, "psi2": cls.psi2_mass}

        fit_cut = cls.bdt_cmb & cls.bdt_prc & q2_cut[kind] & mass_cut[kind]
        normal_cut = cls.bdt_cmb & cls.bdt_prc & q2_cut[q2] & cls.normal_mass

        if dataset == "r1":
            years = ["2011", "2012"]
        elif dataset == "r2p1":
            years = ["2015", "2016"]
        elif dataset == "all":
            years = ["2011", "2012", "2015", "2016", "2017", "2018"]
        else:
            years = [dataset]

        all_fit_efficiencies = []
        all_normal_efficiencies = []
        all_lumi_weights = []
        for year in years:
            data_path = cls.project_root + f"root_sample/v6/{kind_dir}/v10.21p2/2018_ETOS/noq2_nomass.root"
            data_array = read_root(data_path, "ETOS")

            fit_efficiency = fit_cut.get_entries(data_array) / len(data_array)
            normal_efficiency = normal_cut.get_entries(data_array) / len(data_array)
            all_fit_efficiencies.append(fit_efficiency)
            all_normal_efficiencies.append(normal_efficiency)
            all_lumi_weights.append(get_lumi(year))

        fit_efficiency = np.average(all_fit_efficiencies, weights=all_lumi_weights)
        normal_efficiency = np.average(all_normal_efficiencies, weights=all_lumi_weights)

        fully_reco_yield = fit_yield / fit_efficiency * normal_efficiency

        logger.info(
            f"fit_yield: {fit_yield}, fit_efficiency: {fit_efficiency}, normal_efficiency: {normal_efficiency}, fully_reco_yield: {fully_reco_yield}"
        )

        return fully_reco_yield


def get_KDE_shape(obs, kind, q2, name, bandwidth=10):
    if kind == "jpsi":
        kind_dir = "ctrl"
    else:
        kind_dir = kind
    data_path = get_project_root() + f"root_sample/v6/{kind_dir}/v10.21p2/2018_ETOS/{q2}_nomass.root"
    data_array = read_root(data_path, "ETOS")
    bdt = FullyRecoYield.bdt_cmb & FullyRecoYield.bdt_prc
    data_array = bdt.apply(data_array)

    zdata = zfit.Data.from_numpy(obs, array=ak.to_numpy(data_array.B_M))
    if bandwidth is None:
        shape = zfit.pdf.KDE1DimFFT(obs=obs, data=zdata, name=name)
    else:
        shape = zfit.pdf.KDE1DimFFT(obs=obs, data=zdata, name=name, bandwidth=bandwidth)

    return shape


def get_cmb_ee_shape(obs, q2):
    mu_cmb = zfit.Parameter(f"cmb_ee_mu_{q2}", 4000, 3500, 5000)
    scale_cmb = zfit.Parameter(f"cmb_ee_scale_{q2}", 10, 0.1, 100)
    a = zfit.Parameter(f"cmb_ee_a_{q2}", -10, -20, 0)
    b = zfit.Parameter(f"cmb_ee_b_{q2}", 1, 0, 10)
    comb_ee = SUJohnson(obs=obs, mu=mu_cmb, lm=scale_cmb, gamma=a, delta=b, name=f"comb_ee_{q2}")

    pickle_path = f"data/comb_ee/latest/{q2}_2018_B_M_withBDTprc/{q2}_2018_B_M_withBDTprc_fit_result.pickle"
    comb_ee = load_pdf(pickle_path, comb_ee, cache_json_p=False)
    return comb_ee


def plot(data_array, shape_yield_name_list, mass_window, path, nbins=100):
    data_hist = hist.Hist.new.Regular(nbins, mass_window[0], mass_window[1], overflow=False, name="B_M").Double()
    data_hist.fill(data_array.B_M)

    plt.figure()
    mplhep.histplot(data_hist, yerr=True, histtype="errorbar", color="black", label="data")
    x = np.linspace(mass_window[0], mass_window[1], 2000)
    previous_y = None
    for shape, shape_yield, name in shape_yield_name_list:
        if shape_yield == 0:
            continue
        print(shape, shape_yield, name)
        y = shape.pdf(x, norm=mass_window) * (mass_window[1] - mass_window[0]) / nbins * shape_yield
        if previous_y is None:
            plt.fill_between(x, y, label=name)
            previous_y = y
        else:
            plt.fill_between(x, previous_y, previous_y + y, label=name)
            previous_y += y
    plt.legend()
    plt.xlim(mass_window)
    logger.info(f"saving plot to {path}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.savefig(path)
    plt.close()


def main():
    psi2S_part_reco_shape, psi2S_ratio, _ = get_convolution_shape("psi2S_psi2S", "2018", "ETOS")
    Jpsi_part_reco_shape, Jpsi_ratio, _ = get_convolution_shape("Jpsi_psi2S", "2018", "ETOS")

    mass_window = (4500, 6000)

    obs = zfit.Space("B_M", limits=mass_window)
    cmb_shape = get_cmb_ee_shape(obs, "psi2")
    JpsiK_shape = get_KDE_shape(obs, "jpsi", "psi2", "JpsiK")
    psi2SK_shape = get_KDE_shape(obs, "psi2", "psi2", "psi2SK")

    Jpsi_ratio *= Jpsi_part_reco_shape.integrate(mass_window)[0] / JpsiK_shape.integrate(mass_window)[0]
    psi2S_ratio *= psi2S_part_reco_shape.integrate(mass_window)[0] / psi2SK_shape.integrate(mass_window)[0]

    data_path = get_project_root() + "root_sample/v6/data/v10.21p2/2018_ETOS/psi2_nomass.root"
    data_array = read_root(data_path, "ETOS")
    data_cut = FullyRecoYield.data_pid & FullyRecoYield.bdt_cmb & FullyRecoYield.normal_mass & FullyRecoYield.bdt_prc
    data_array = data_cut.apply(data_array)

    data_yield = len(data_array)
    psi2SK_yield = FullyRecoYield.get("psi2", "psi2")
    JpsiK_yield = FullyRecoYield.get("jpsi", "psi2")

    psi2S_part_reco_yield = psi2SK_yield * psi2S_ratio
    Jpsi_part_reco_yield = JpsiK_yield * Jpsi_ratio

    cmb_yield = data_yield - JpsiK_yield - psi2SK_yield - psi2S_part_reco_yield - Jpsi_part_reco_yield
    cmb_yield = 0 if cmb_yield < 0 else cmb_yield

    logger.info("Yield after fit:")
    print(f"JpsiK_yield: {JpsiK_yield}")
    print(f"psi2SK_yield: {psi2SK_yield}")
    print(f"Jpsi_part_reco_yield: {Jpsi_part_reco_yield}")
    print(f"psi2S_part_reco_yield: {psi2S_part_reco_yield}")
    print(f"cmb_yield: {cmb_yield}")

    shape_yield_name_list = [
        (cmb_shape, cmb_yield, "combinatorial"),
        (psi2S_part_reco_shape, psi2S_part_reco_yield, "psi2S_part_reco"),
        (Jpsi_part_reco_shape, Jpsi_part_reco_yield, "Jpsi_part_reco"),
        (psi2SK_shape, psi2SK_yield, "psi2SK"),
        (JpsiK_shape, JpsiK_yield, "JpsiK"),
    ]
    plot_path = get_project_root() + "output/check/part_reco/psi2S_region/latest/psi2S_region.pdf"
    plot(data_array, shape_yield_name_list, mass_window, plot_path)


if __name__ == "__main__":
    main()
