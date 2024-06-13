import zfit
from hqm.tools.utility import get_project_root
from hqm.tools.utility import read_root
from hqm.tools.utility import dump_pickle
from hqm.tools.utility import load_pickle
from hqm.tools.utility import get_lumi
from hqm.tools.selection import selection
from hqm.tools.Cut import Cut
from hqm.check.part_reco.psi2S_region import FullyRecoYield
from hqm.part_reco.convolution_shape import get_convolution_shape
from hqm.part_reco.ratio.fully_reco_shape import get_gen_eventnumber
from hqm.model.part_reco import get_shape
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
    data_hist.fill(data_array)

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


def _get_part_reco(year="2018", trigger="ETOS", parameter_name_prefix="", pdf_name="", kind=None):
    parameter_name_prefix = parameter_name_prefix + "_" if parameter_name_prefix != "" else ""

    part_reco_shape, ratio, _ = get_convolution_shape(
        kind=kind,
        year=year,
        trigger=trigger,
        parameter_name_prefix=parameter_name_prefix.removesuffix("_"),
    )

    return part_reco_shape, ratio


def get_data(dataset="2018", q2="jpsi"):
    if dataset == "r1":
        years = ["2011", "2012"]
    elif dataset == "r2p1":
        years = ["2015", "2016"]
    elif dataset == "all":
        years = ["2011", "2012", "2015", "2016", "2017", "2018"]
    else:
        years = [dataset]
    all_array = []
    data_cut = FullyRecoYield.data_pid & FullyRecoYield.bdt_cmb & FullyRecoYield.normal_mass & FullyRecoYield.bdt_prc
    for year in years:
        data_path = get_project_root() + f"root_sample/v6/data/v10.21p2/{year}_ETOS/{q2}_nomass.root"
        data_array = read_root(data_path, "ETOS")
        data_array = data_cut.apply(data_array)
        all_array.append(data_array.B_M)
    return ak.concatenate(all_array) if len(years) > 1 else all_array[0]


# def get_fully_reco(obs, q2, dataset, kind):
#     name_suffix = f"{'JpsiK' if kind == 'jpsi' else 'psi2SK'}_{dataset}_{q2}"

#     mu = zfit.Parameter(f"mu_{name_suffix}", 5200, 4500, 6000)
#     sigma = zfit.Parameter(f"sigma_{name_suffix}", 20, 0, 100)
#     alphal = zfit.Parameter(f"alphal_{name_suffix}", 1, 0.1, 10)
#     nl = zfit.Parameter(f"nl_{name_suffix}", 3, 1, 50)
#     alphar = zfit.Parameter(f"alphar_{name_suffix}", 1, 0.1, 10)
#     nr = zfit.Parameter(f"nr_{name_suffix}", 3, 1, 50)

#     # Create the DoubleCB
#     dscb = zfit.pdf.DoubleCB(
#         mu=mu,
#         sigma=sigma,
#         alphal=alphal,
#         nl=nl,
#         alphar=alphar,
#         nr=nr,
#         obs=obs,
#         name=f"{'JpsiK' if kind == 'jpsi' else 'psi2SK'}_{dataset}_{q2}q2",
#     )

#     pickle_path = get_project_root() + f"data/part_reco/ratio/fit_MC/latest/fit_MC_{name_suffix}.pickle"
#     obj = load_pickle(pickle_path)
#     result = obj["result"]

#     params = dscb.get_params()
#     zfit.param.set_values(params, result)

#     for param in [alphal, nl, alphar, nr]:
#         param.floating = False

#     return dscb


def get_fully_reco(obs, q2, dataset, kind):
    kind_dir = "ctrl" if kind == "jpsi" else kind

    if dataset == "r1":
        years = ["2011", "2012"]
    elif dataset == "r2p1":
        years = ["2015", "2016"]
    elif dataset == "all":
        years = ["2011", "2012", "2015", "2016", "2017", "2018"]
    else:
        years = [dataset]

    bdt_cmb = selection["ee"]["bdt_cmb"]["ETOS"]
    bdt_prc = selection["ee"]["bdt_prc"]["ETOS"]
    pid = selection["ee"]["pid"]
    mass = Cut(lambda x: (x.B_M > 4500) & (x.B_M < 6000))

    cut = bdt_cmb & bdt_prc & pid & mass

    project_root = get_project_root()
    all_data = []
    all_lumi_weights = []
    for year in years:
        data_path = project_root + f"root_sample/v6/{kind_dir}/v10.21p2/{year}_ETOS/{q2}_nomass.root"
        data_array = read_root(data_path, "ETOS")
        data_array = cut.apply(data_array)
        all_data.append(data_array)
        lumi = get_lumi(year)
        gen_eventnumber = get_gen_eventnumber(kind, year)
        lumi_weight = lumi / gen_eventnumber
        all_lumi_weights += [lumi_weight] * len(data_array)

    lumi_weights = np.array(all_lumi_weights)
    lumi_weights *= len(lumi_weights) / np.sum(lumi_weights)
    data_array = ak.concatenate(all_data)
    data_array["lumi_weight"] = lumi_weights

    decay_name = "JpsiK" if kind == "jpsi" else "psi2SK"

    if q2 == kind:
        # pickle_path = (
        #     get_project_root()
        #     + f"data/part_reco/ratio/fully_reco_shape/latest/{decay_name}_{q2}q2_{dataset}_weight.pickle"
        # )

        # use JpsiK weight for psi2SK
        pickle_path = (
            get_project_root() + f"data/part_reco/ratio/fully_reco_shape/latest/JpsiK_jpsiq2_{dataset}_weight.pickle"
        )
        weight_hist = load_pickle(pickle_path)
        weight_getter = np.vectorize(lambda x: weight_hist[x * 1j])
        shape_weight = weight_getter(data_array.B_M)
        data_array["shape_weight"] = shape_weight * data_array.lumi_weight
    else:
        data_array["shape_weight"] = data_array.lumi_weight

    data_np = ak.to_numpy(data_array.B_M)
    weight_np = ak.to_numpy(data_array.shape_weight)

    zdata = zfit.Data.from_numpy(obs, array=data_np, weights=weight_np)
    shape = zfit.pdf.KDE1DimFFT(obs=obs, data=zdata, name=f"{decay_name}_{dataset}_{q2}q2")

    plt.figure()
    x = np.linspace(4500, 6000, 2000)
    y = shape.pdf(x) * (6000 - 4500) / 100
    plt.plot(x, y, label=f"{decay_name}_{dataset}_{q2}q2")
    plt.xlim(4500, 6000)
    plt.ylim(bottom=0)
    plt.legend()
    plot_path = (
        get_project_root() + f"output/part_reco/ratio/simultaneous_fit/latest/KDE/{decay_name}_{dataset}_{q2}q2.pdf"
    )
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)
    plt.close()

    return shape


def get_nll(obs, q2, shared_parameters, dataset):
    _name = {"jpsi": "Jpsi", "psi2": "psi2S"}

    psi2S_part_reco_shape, _psi2S_ratio = get_shape(dataset, "ETOS", _get_part_reco, kind=f"psi2S_{_name[q2]}")
    Jpsi_part_reco_shape, _Jpsi_ratio = get_shape(dataset, "ETOS", _get_part_reco, kind=f"Jpsi_{_name[q2]}")
    logger.info(f"muon psi2S_ratio: {_psi2S_ratio}")
    logger.info(f"muon Jpsi_ratio: {_Jpsi_ratio}")
    for param in psi2S_part_reco_shape.get_params():
        param.floating = False
    for param in Jpsi_part_reco_shape.get_params():
        param.floating = False

    JpsiK_shape = get_fully_reco(obs, q2, dataset, "jpsi")
    psi2SK_shape = get_fully_reco(obs, q2, dataset, "psi2")

    mass_window = obs.limit1d
    psi2S_mass_window_factor = psi2S_part_reco_shape.integrate(mass_window)[0] / psi2SK_shape.integrate(mass_window)[0]
    Jpsi_mass_window_factor = Jpsi_part_reco_shape.integrate(mass_window)[0] / JpsiK_shape.integrate(mass_window)[0]
    print(f"psi2S_{q2}q2_mass_window_factor: {psi2S_mass_window_factor}")
    print(f"Jpsi_{q2}_mass_window_factor: {Jpsi_mass_window_factor}")

    psi2S_part_reco_shape.set_norm_range(mass_window)
    Jpsi_part_reco_shape.set_norm_range(mass_window)

    data_array = get_data(dataset, q2)

    suffix = f"{q2}_{dataset}"

    psi2SK_expected_yield = FullyRecoYield.get("psi2", q2, dataset)
    JpsiK_expected_yield = FullyRecoYield.get("jpsi", q2, dataset)
    psi2SK_yield = zfit.Parameter(f"psi2SK_yield_{suffix}", psi2SK_expected_yield, 0, 1e8)
    JpsiK_yield = zfit.Parameter(f"JpsiK_yield_{suffix}", JpsiK_expected_yield, 0, 1e8)
    constraint = zfit.constraint.GaussianConstraint(
        [psi2SK_yield, JpsiK_yield],
        [psi2SK_expected_yield, JpsiK_expected_yield],
        [psi2SK_expected_yield * 0.1, JpsiK_expected_yield * 0.1],
    )

    # psi2SK_yield.floating = False
    # JpsiK_yield.floating = False

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

    total_model = zfit.pdf.SumPDF(
        [psi2S_part_reco_shape, Jpsi_part_reco_shape, psi2SK_shape, JpsiK_shape], obs=obs, name="total_model"
    )
    zdata = zfit.Data.from_numpy(obs=obs, array=ak.to_numpy(data_array))

    # nll = zfit.loss.ExtendedUnbinnedNLL(model=total_model, data=zdata, constraints=constraint)
    nll = zfit.loss.ExtendedUnbinnedNLL(model=total_model, data=zdata)
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
    nll1, data_jpsi, total_model_jpsi = get_nll(obs, "jpsi", shared_parameters, dataset)
    nll2, data_psi2, total_model_psi2 = get_nll(obs, "psi2", shared_parameters, dataset)
    nll = nll1 + nll2

    minimizer = zfit.minimize.Minuit()
    result = minimizer.minimize(nll)
    result.hesse()
    print(result)

    result.freeze()
    pickle_path = (
        get_project_root() + f"data/part_reco/ratio/simultaneous_fit/latest/simultaneous_fit_result_{dataset}.pickle"
    )
    dump_pickle(result, pickle_path)

    plot_path = (
        get_project_root() + f"output/part_reco/ratio/simultaneous_fit/latest/simultaneous_fit_jpsi_{dataset}.pdf"
    )
    plot(data_jpsi, total_model_jpsi, mass_window, plot_path)
    plot_path = (
        get_project_root() + f"output/part_reco/ratio/simultaneous_fit/latest/simultaneous_fit_psi2_{dataset}.pdf"
    )
    plot(data_psi2, total_model_psi2, mass_window, plot_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, help="dataset", default="2018")
    args = parser.parse_args()
    main(args.dataset)
