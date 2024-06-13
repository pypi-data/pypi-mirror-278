from hqm.tools.utility import get_project_root
from hqm.tools.utility import get_lumi
from hqm.tools.utility import read_root
from hqm.tools.selection import selection
from hqm.tools.utility import dump_pickle
from hqm.tools.Cut import Cut
import uproot
import awkward as ak
import numpy as np
import hist
import matplotlib.pyplot as plt
import os
import mplhep
import argparse


def get_gen_eventnumber(kind, year):
    kind_dir = "ctrl" if kind == "jpsi" else kind
    data_path = f"/publicfs/lhcb/user/campoverde/Data/RK/{kind_dir}_ee/v10.21p2/{year}.root"
    with uproot.open(data_path) as f:
        event_number = f["gen"].num_entries

    return event_number


def get_data(kind, dataset, q2):
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

    cut = bdt_cmb & bdt_prc & pid

    project_root = get_project_root()
    all_data = []
    all_lumi_weights = []
    for year in years:
        data_path = project_root + f"root_sample/v6/{kind_dir}/v10.21p2/{year}_ETOS/{q2}_nomass.root"
        data_array = read_root(data_path, "ETOS")
        data_array = cut.apply(data_array)
        all_data.append(data_array)
        lumi = get_lumi(year)
        if kind == "data":
            lumi_weight = 1.0
        else:
            gen_eventnumber = get_gen_eventnumber(kind, year)
            lumi_weight = lumi / gen_eventnumber
        all_lumi_weights += [lumi_weight] * len(data_array)

    lumi_weights = np.array(all_lumi_weights)
    lumi_weights *= len(lumi_weights) / np.sum(lumi_weights)
    data_array = ak.concatenate(all_data)
    data_array["lumi_weight"] = lumi_weights
    return data_array


def weight_hist(h_data, h_MC, plot_name):
    data_values = h_data.values()
    MC_values = h_MC.values()
    weight_values = data_values / MC_values
    weight_values[~np.isfinite(weight_values)] = 1

    weight_hist = hist.Hist.new.Regular(100, 4500, 6000, name="weight", flow=False).Double()
    weight_hist[...] = weight_values

    plt.figure()
    mplhep.histplot(weight_hist, yerr=False, histtype="errorbar", color="black", label="data/MC")
    plot_path = get_project_root() + f"output/part_reco/ratio/fully_reco_shape/latest/{plot_name}_weight.pdf"
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)
    plt.close()

    pickle_path = get_project_root() + f"data/part_reco/ratio/fully_reco_shape/latest/{plot_name}_weight.pickle"
    os.makedirs(os.path.dirname(pickle_path), exist_ok=True)
    dump_pickle(weight_hist, pickle_path)


def compare(data, MC, cut, plot_name):
    data_array = cut.apply(data)
    MC_array = cut.apply(MC)

    h_data = hist.Hist.new.Regular(100, 4500, 6000, name="B_M", flow=False).Weight()
    h_data.fill(data_array.B_M, weight=data_array.lumi_weight)

    h_MC = hist.Hist.new.Regular(100, 4500, 6000, name="B_M", flow=False).Weight()
    h_MC.fill(MC_array.B_M, weight=MC_array.lumi_weight)

    h_MC *= h_data.sum().value / h_MC.sum().value

    weight_hist(h_data, h_MC, plot_name)

    plt.figure()
    h_data.plot_ratio(
        h_MC,
        rp_ylabel=r"Ratio",
        rp_num_label="Data",
        rp_denom_label="MC",
        rp_uncert_draw_type="bar",
    )
    plot_path = get_project_root() + f"output/part_reco/ratio/fully_reco_shape/latest/{plot_name}.pdf"
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)
    plt.close()


def main(dataset):
    data_jpsiq2 = get_data("data", dataset, "jpsi")
    data_psi2q2 = get_data("data", dataset, "psi2")

    JpsiK_MC_jpsiq2 = get_data("jpsi", dataset, "jpsi")
    JpsiK_MC_psi2q2 = get_data("jpsi", dataset, "psi2")
    psi2SK_MC_psi2q2 = get_data("psi2", dataset, "psi2")
    psi2SK_MC_jpsiq2 = get_data("psi2", dataset, "jpsi")

    normal_mass_cut = Cut(lambda x: (x.B_M > 4500) & (x.B_M < 6000))

    JpsiK_cut_jpsi_mass_constraint = Cut(lambda x: (x.B_M_Jpsi > 5229.34) & (x.B_M_Jpsi < 5329.34))
    # JpsiK_cut_psi2_mass_constraint = Cut(lambda x: (x.B_M_Psi > 5200) & (x.B_M_Psi < 5350))

    # psi2SK_cut_jpsi_mass_constraint = Cut(lambda x: (x.B_M_Jpsi > 5200) & (x.B_M_Jpsi < 5350))
    psi2SK_cut_psi2_mass_constraint = Cut(lambda x: (x.B_M_Psi > 5229.34) & (x.B_M_Psi < 5329.34))

    compare(data_jpsiq2, JpsiK_MC_jpsiq2, JpsiK_cut_jpsi_mass_constraint, f"JpsiK_jpsiq2_{dataset}")
    compare(data_psi2q2, psi2SK_MC_psi2q2, psi2SK_cut_psi2_mass_constraint, f"psi2SK_psi2q2_{dataset}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", help="dataset to be used")
    args = parser.parse_args()
    main(args.dataset)
