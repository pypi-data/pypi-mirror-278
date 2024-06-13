from hqm.tools.utility import get_project_root
from hqm.tools.utility import read_root
from hqm.tools.utility import cache_json
from hqm.tools.selection import selection
from hqm.tools.utility import get_lumi
import zfit
import awkward as ak
import numpy as np

from log_store import log_store

log=log_store.add_logger('hqm:KDE_shape')

def get_KDE_shape(obs, kind, q2, bandwidth=10, dataset="2018", trigger="ETOS", pdf_name="", bts_index=0):
    if dataset == "r1":
        years = ["2011", "2012"]
    elif dataset == "r2p1":
        years = ["2015", "2016"]
    elif dataset == "all":
        years = ["2011", "2012", "2015", "2016", "2017", "2018"]
    else:
        years = [dataset]

    all_data = []
    all_lumi_weights = []
    for year in years:
        json_file = f"KDE_{year}_{trigger}_{q2}_{kind}.json"

        @cache_json(json_file)
        def _get_data_array():
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
            data_list = ak.to_numpy(data_array.B_M).tolist()
            return data_list

        data_list = _get_data_array()
        lumi = get_lumi(year)
        all_data += data_list
        all_lumi_weights += [lumi / len(data_list)] * len(data_list)

    data_np = np.array(all_data)
    lumi_weights = np.array(all_lumi_weights)

    if len(years) == 1 and bts_index == 0:
        zdata = zfit.Data.from_numpy(obs, array=data_np)
    else:
        weights = np.ones(len(data_np))
        if len(years) > 1:
            weights *= lumi_weights
        if bts_index > 0:
            np.random.seed(bts_index + len(data_np))
            weights *= np.random.poisson(1, len(data_np))

        log.debug('Making zdata with:')
        log.debug(f'Obs:     {obs}')
        log.debug(f'Data:    {data_np.shape}')
        log.debug(f'Weights: {weights.shape}')

        zdata = zfit.Data.from_numpy(obs=obs, array=data_np, weights=weights)
        log.debug('Made zdata')

    shape = zfit.pdf.KDE1DimFFT(obs=obs, data=zdata, name=f"{pdf_name}_{year}_{trigger}", bandwidth=bandwidth)

    return shape
