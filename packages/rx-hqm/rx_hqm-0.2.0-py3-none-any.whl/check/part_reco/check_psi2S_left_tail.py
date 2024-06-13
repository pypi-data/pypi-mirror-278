from hqm.tools.utility import read_root
from hqm.tools.utility import get_project_root
from hqm.tools.utility import get_lumi
from hqm.tools.selection import selection
from hqm.tools.Cut import Cut
import numpy as np
import awkward as ak
import uproot
import mplhep
import hist
import os
import matplotlib.pyplot as plt
from logzero import logger


def get_gen_eventnumber(kind, year):
    kind_dir = "ctrl" if kind == "jpsi" else kind
    data_path = f"/publicfs/lhcb/user/campoverde/Data/RK/{kind_dir}_ee/v10.21p2/{year}.root"
    with uproot.open(data_path) as f:
        event_number = f["gen"].num_entries

    return event_number


def get_data(kind, dataset, q2):
    kind_dir = "ctrl" if kind == "jpsi" else kind

    if dataset == "rl":
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


def plot_variable(data, variable, suffix=""):
    lower_limit = ak.min(data[variable])
    upper_limit = ak.max(data[variable])
    h_data = hist.Hist.new.Regular(100, lower_limit, upper_limit, flow=False, name=variable).Weight()
    h_data.fill(data[variable], weight=data["lumi_weight"])
    plt.figure()
    mplhep.histplot(h_data, label="Data")
    plot_path = get_project_root() + f"output/check/part_reco/check_psi2S_left_tail/latest/{variable}{suffix}.pdf"
    logger.info(f"Saving plot to {plot_path}")
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)
    plt.close()


def main():
    data_psi2q2 = get_data("data", "all", "psi2")
    normal_mass_cut = Cut(lambda x: (x.B_M > 4500) & (x.B_M < 6000))
    psi2SK_cut_psi2_mass_constraint = Cut(lambda x: (x.B_M_Psi > 5229.34) & (x.B_M_Psi < 5329.34))
    psi2SK_cut_left_tail = Cut(lambda x: (x.B_M > 4500) & (x.B_M < 5000))

    total_cut = normal_mass_cut & psi2SK_cut_psi2_mass_constraint & psi2SK_cut_left_tail
    data = total_cut.apply(data_psi2q2)

    plot_variable(data, "B_M")
    plot_variable(data, "B_M_Psi")
    plot_variable(data, "Jpsi_M")

    psi2SK_mass = 3686.10
    width = 40
    tightq2_cut = Cut(lambda x: (x.Jpsi_M > (psi2SK_mass - width)) & (x.Jpsi_M < (psi2SK_mass + width)))

    total_cut_tightq2 = normal_mass_cut & tightq2_cut
    suffix = "_tightq2"
    data_tightq2 = total_cut_tightq2.apply(data_psi2q2)

    plot_variable(data_tightq2, "B_M", suffix)
    plot_variable(data_tightq2, "B_M_Psi", suffix)
    plot_variable(data_tightq2, "Jpsi_M", suffix)

    total_cut_tightq2_massconstraint = normal_mass_cut & psi2SK_cut_psi2_mass_constraint & tightq2_cut
    suffix = "_tightq2_massconstraint"
    data_tightq2_massconstraint = total_cut_tightq2_massconstraint.apply(data_psi2q2)

    plot_variable(data_tightq2_massconstraint, "B_M", suffix)
    plot_variable(data_tightq2_massconstraint, "B_M_Psi", suffix)
    plot_variable(data_tightq2_massconstraint, "Jpsi_M", suffix)

    tightprc_cut = Cut(lambda x: x.BDT_prc > 0.6)
    total_cut_tightprc = normal_mass_cut & tightprc_cut
    suffix = "_tightprc"
    data_tightprc = total_cut_tightprc.apply(data_psi2q2)

    plot_variable(data_tightprc, "B_M", suffix)
    plot_variable(data_tightprc, "B_M_Psi", suffix)
    plot_variable(data_tightprc, "Jpsi_M", suffix)

    total_cut_tightprc_massconstraint = normal_mass_cut & psi2SK_cut_psi2_mass_constraint & tightprc_cut
    suffix = "_tightprc_massconstraint"
    data_tightprc_massconstraint = total_cut_tightprc_massconstraint.apply(data_psi2q2)

    plot_variable(data_tightprc_massconstraint, "B_M", suffix)
    plot_variable(data_tightprc_massconstraint, "B_M_Psi", suffix)
    plot_variable(data_tightprc_massconstraint, "Jpsi_M", suffix)

    total_cut_tightprc_massconstraint_lefttail = (
        normal_mass_cut & psi2SK_cut_psi2_mass_constraint & tightprc_cut & psi2SK_cut_left_tail
    )
    suffix = "_tightprc_massconstraint_lefttail"
    data_tightprc_massconstraint_lefttail = total_cut_tightprc_massconstraint_lefttail.apply(data_psi2q2)

    plot_variable(data_tightprc_massconstraint_lefttail, "B_M", suffix)
    plot_variable(data_tightprc_massconstraint_lefttail, "B_M_Psi", suffix)
    plot_variable(data_tightprc_massconstraint_lefttail, "Jpsi_M", suffix)


if __name__ == "__main__":
    main()
