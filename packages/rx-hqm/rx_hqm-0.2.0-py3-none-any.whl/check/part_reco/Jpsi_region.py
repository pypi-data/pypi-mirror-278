from hqm.check.part_reco.psi2S_region import FullyRecoYield
from hqm.check.part_reco.psi2S_region import get_KDE_shape
from hqm.check.part_reco.psi2S_region import get_cmb_ee_shape
from hqm.check.part_reco.psi2S_region import plot
from hqm.part_reco.convolution_shape import get_convolution_shape
from hqm.tools.utility import get_project_root
from hqm.tools.utility import read_root
import zfit
from logzero import logger


def main():
    psi2S_part_reco_shape, psi2S_ratio, _ = get_convolution_shape("psi2S_Jpsi", "2018", "ETOS")
    Jpsi_part_reco_shape, Jpsi_ratio, _ = get_convolution_shape("Jpsi_Jpsi", "2018", "ETOS")

    mass_window = (4500, 6000)

    obs = zfit.Space("B_M", limits=mass_window)
    cmb_shape = get_cmb_ee_shape(obs, "jpsi")
    JpsiK_shape = get_KDE_shape(obs, "jpsi", "jpsi", "JpsiK")
    psi2SK_shape = get_KDE_shape(obs, "psi2", "jpsi", "psi2SK")

    Jpsi_ratio *= Jpsi_part_reco_shape.integrate(mass_window)[0] / JpsiK_shape.integrate(mass_window)[0]
    psi2S_ratio *= psi2S_part_reco_shape.integrate(mass_window)[0] / psi2SK_shape.integrate(mass_window)[0]

    data_path = get_project_root() + "root_sample/v6/data/v10.21p2/2018_ETOS/jpsi_nomass.root"
    data_array = read_root(data_path, "ETOS")
    data_cut = FullyRecoYield.data_pid & FullyRecoYield.bdt_cmb & FullyRecoYield.normal_mass & FullyRecoYield.bdt_prc
    data_array = data_cut.apply(data_array)

    data_yield = len(data_array)
    psi2SK_yield = FullyRecoYield.get("psi2", "jpsi")
    JpsiK_yield = FullyRecoYield.get("jpsi", "jpsi")

    psi2S_part_reco_yield = psi2SK_yield * psi2S_ratio
    Jpsi_part_reco_yield = JpsiK_yield * Jpsi_ratio

    cmb_yield = data_yield - JpsiK_yield - psi2SK_yield - psi2S_part_reco_yield - Jpsi_part_reco_yield
    cmb_yield = 0 if cmb_yield < 0 else cmb_yield

    logger.info("Yield:")
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
    plot_path = get_project_root() + "output/check/part_reco/Jpsi_region/latest/Jpsi_region.pdf"
    plot(data_array, shape_yield_name_list, mass_window, plot_path)


if __name__ == "__main__":
    main()
