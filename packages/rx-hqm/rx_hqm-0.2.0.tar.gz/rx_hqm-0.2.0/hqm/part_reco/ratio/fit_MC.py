import zfit
from hqm.tools.fit import fit
from hqm.tools.utility import get_project_root
from hqm.tools.utility import read_root
from hqm.tools.utility import get_lumi
from hqm.tools.selection import selection
import argparse
import awkward as ak
import numpy as np
import uproot


class fit_JpsiK_MC(fit):
    def __init__(self, obs: zfit.Space, data: zfit.Data, name_suffix=""):
        self._name_suffix = name_suffix
        super().__init__(obs, data)

    def build_model(self):
        mu = zfit.Parameter(f"mu_{self._name_suffix}", 5200, 4500, 6000)
        sigma = zfit.Parameter(f"sigma_{self._name_suffix}", 20, 0, 100)
        alphal = zfit.Parameter(f"alphal_{self._name_suffix}", 1, 0.1, 10)
        nl = zfit.Parameter(f"nl_{self._name_suffix}", 3, 1, 70)
        alphar = zfit.Parameter(f"alphar_{self._name_suffix}", 1, 0.1, 10)
        nr = zfit.Parameter(f"nr_{self._name_suffix}", 3, 1, 70)

        # Create the DoubleCB
        dscb = zfit.pdf.DoubleCB(
            mu=mu,
            sigma=sigma,
            alphal=alphal,
            nl=nl,
            alphar=alphar,
            nr=nr,
            obs=self.obs,
            name=f"{self._name_suffix}q2",
        )
        self.add_pdf(dscb)

    def run(self):
        self.build_model()
        self.fit_data()

        project_root = get_project_root()
        pickle_path = project_root + f"data/part_reco/ratio/fit_MC/latest/fit_MC_{self._name_suffix}.pickle"
        self.dump_result(pickle_path)
        plot_path = project_root + f"output/part_reco/ratio/fit_MC/latest/fit_MC_{self._name_suffix}.pdf"
        self.plot(plot_path)


def get_gen_eventnumber(kind, year):
    kind_dir = "ctrl" if kind == "jpsi" else kind
    data_path = f"/publicfs/lhcb/user/campoverde/Data/RK/{kind_dir}_ee/v10.21p2/{year}.root"
    with uproot.open(data_path) as f:
        event_number = f["gen"].num_entries

    return event_number


def get_data(obs, q2, dataset, kind):
    if dataset == "r1":
        years = ["2011", "2012"]
    elif dataset == "r2p1":
        years = ["2015", "2016"]
    elif dataset == "all":
        years = ["2011", "2012", "2015", "2016", "2017", "2018"]
    else:
        years = [dataset]

    trigger = "ETOS"
    all_data = []
    all_lumi_weights = []
    for year in years:
        if kind == "jpsi":
            kind_dir = "ctrl"
        else:
            kind_dir = kind
        data_path = get_project_root() + f"root_sample/v6/{kind_dir}/v10.21p2/{year}_{trigger}/{q2}_nomass.root"
        data_array = read_root(data_path, trigger)
        if trigger in ["ETOS", "GTIS"]:
            bdt_cmb = selection["ee"]["bdt_cmb"][trigger]
            bdt_prc = selection["ee"]["bdt_prc"][trigger]
        elif trigger in ["MTOS"]:
            bdt_cmb = selection["mm"]["bdt_cmb"][trigger]
            bdt_prc = selection["mm"]["bdt_prc"][trigger]
        else:
            raise

        bdt = bdt_cmb & bdt_prc
        data_array = bdt.apply(data_array)

        lumi = get_lumi(year)
        all_data.append(data_array.B_M)
        gen_eventnumber = get_gen_eventnumber(kind, year)
        all_lumi_weights += [lumi / gen_eventnumber] * len(data_array)

    data_np = ak.to_numpy(ak.concatenate(all_data))
    lumi_weights = np.array(all_lumi_weights)
    lumi_weights *= len(lumi_weights) / np.sum(lumi_weights)

    zdata = zfit.Data.from_numpy(obs, array=data_np, weights=lumi_weights)
    return zdata


def main(q2, dataset, kind):
    obs = zfit.Space("B_M", limits=(4500, 6000))
    data = get_data(obs, q2, dataset, kind)
    fitter = fit_JpsiK_MC(obs, data, f"{'JpsiK' if kind == 'jpsi' else 'psi2SK'}_{dataset}_{q2}")
    fitter.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--kind", type=str, help="kind")
    parser.add_argument("-q", "--q2", type=str, help="q2 region")
    parser.add_argument("-d", "--dataset", type=str, help="dataset", default="2018")
    args = parser.parse_args()
    main(args.q2, args.dataset, args.kind)
