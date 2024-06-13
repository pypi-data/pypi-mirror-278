from hqm.model.double_swap import dswp_bmass as dswpb
from hqm.model.double_swap import log        as dswpb_log

import zfit
import logging
import zutils.utils      as zut

#-------------------------------
class data:
    obs_bb = zfit.Space('mass_bb', limits=(5000, 6000))
    obs_mm = zfit.Space('mass_mm', limits=(2600, 3300))
    ncnd   = zfit.param.Parameter('ncnd', 1000, 0, 10000)
#-------------------------------
def check_pdf(tp_pdf, out_dir, name):
    pdf_bb, pdf_mm = tp_pdf

    zut.print_pdf(pdf_bb, txt_path=f'{out_dir}/bmass_pdf_{name}.txt')
    zut.print_pdf(pdf_mm, txt_path=f'{out_dir}/mumu_pdf_{name}.txt')
#-------------------------------
def test_sign():
    obj = dswpb(data.obs_bb, data.obs_mm, proc='sign', name='sign_test')
    obj.out_dir = 'tests/double_swap/sign'
    pdf_1 = obj.get_pdf(extended=False)
    pdf_2 = obj.get_pdf(extended=True)
    pdf_3 = obj.get_pdf(extended=True, ncnd=data.ncnd)

    check_pdf(pdf_1, obj.out_dir, 't1')
    check_pdf(pdf_2, obj.out_dir, 't2')
    check_pdf(pdf_3, obj.out_dir, 't3')
#-------------------------------
def test_ctrl_mc():
    obj = dswpb(data.obs_bb, data.obs_mm, proc='ctrl', name='ctrl_test')
    obj.out_dir = 'tests/double_swap/ctrl_mc'

    pdf_1 = obj.get_pdf(extended=False)
    pdf_2 = obj.get_pdf(extended=True)
    pdf_3 = obj.get_pdf(extended=True, ncnd=data.ncnd)

    check_pdf(pdf_1, obj.out_dir, 't1')
    check_pdf(pdf_2, obj.out_dir, 't2')
    check_pdf(pdf_3, obj.out_dir, 't3')
#-------------------------------
def test_ctrl_dt():
    scl = zfit.param.Parameter('scl',-10, -20,  20)
    res = zfit.param.Parameter('res',1.1, 0.6, 1.2)

    obj = dswpb(data.obs_bb, data.obs_mm, proc='ctrl', name='ctrl_test')
    obj.out_dir = 'tests/double_swap/ctrl_dt'
    obj.mass_scale      = scl
    obj.mass_resolution = res

    pdf_1 = obj.get_pdf(extended=False)
    pdf_2 = obj.get_pdf(extended=True)
    pdf_3 = obj.get_pdf(extended=True, ncnd=data.ncnd)

    check_pdf(pdf_1, obj.out_dir, 't1')
    check_pdf(pdf_2, obj.out_dir, 't2')
    check_pdf(pdf_3, obj.out_dir, 't3')
#-------------------------------
def test_cmb():
    obj = dswpb(data.obs_bb, data.obs_mm, proc='cmb', name='cmb_test')
    obj.out_dir = 'tests/double_swap/cmb'
    pdf_1 = obj.get_pdf(extended=False)
    pdf_2 = obj.get_pdf(extended=True)
    pdf_3 = obj.get_pdf(extended=True, ncnd=data.ncnd)

    check_pdf(pdf_1, obj.out_dir, 't1')
    check_pdf(pdf_2, obj.out_dir, 't2')
    check_pdf(pdf_3, obj.out_dir, 't3')
#-------------------------------
def test_plot():
    obj            = dswpb(data.obs_bb, data.obs_mm, proc='cmb', name='plot_test')
    obj.out_dir    = 'tests/double_swap/plot'
    pdf_bb, pdf_mm = obj.get_pdf()

    pdf = zfit.pdf.ProductPDF([pdf_bb, pdf_mm])

    zut.print_pdf(pdf)

    sam = pdf.create_sampler(n=1000)
#-------------------------------
def main():
    dswpb_log.setLevel(logging.DEBUG)
    test_ctrl_mc()
    test_ctrl_dt()
    return
    test_sign()
    test_plot()
    test_cmb()
#-------------------------------
if __name__ == '__main__':
    main()

