# from ROOT import *
import ROOT
from math import sqrt
from array import array

f = ROOT.TFile('B_cut_.root', 'read')  # file where to read from

signals, signals_err = array('d'), array('d')

for i in range(1, 8):
    pname = 'Pic_mass_bin_' + str(i) + '.png'

    histname = "hBmas" + str(i)

    mbmin = 5.06
    mbmax = 5.46
    mbNbins = 150  # range of plot + N(bins)

    varname = "M(B) , [GeV]"
    TwoGaus = 1

    canvW = 1000
    canvH = 600
    _PicName = 'pictures/' + pname  # name of file with picture

    fit_M0 = 5.27963
    fit_Sigma0 = 0.015
    fit_N0 = 80000

    mb = ROOT.RooRealVar("mb", varname, mbmin, mbmax)

    exec('hh = f.%s.Clone();' % histname)
    hh.SetName('hh')

    datahist = ROOT.RooDataHist('datahist', 'datahist', ROOT.RooArgList(mb), hh)  ## create RooHist from histogram

    ###                                          initial  lower   upper
    ###                                          values   bound   bound

    S1 = ROOT.RooRealVar("S1", "Signal", fit_N0, 1, 900000)
    S1_mean = ROOT.RooRealVar("S1_mean", "mean ", fit_M0, fit_M0 - 0.1, fit_M0 + 0.1)
    S1_sigma = ROOT.RooRealVar("S1_sigma", "sigma", fit_Sigma0, 0.001, 0.05)

    B = ROOT.RooRealVar("B", "B", 40000, 1, 900000000)
    B_c = ROOT.RooRealVar("B_c", "B_c ", -2.3, -20, 100)
    B_1 = ROOT.RooRealVar("B_1", "B_1 ", 0.1, 0.0, 1.0)
    B_2 = ROOT.RooRealVar("B_2", "B_2 ", 0.1, 0.0, 1.0)
    B_3 = ROOT.RooRealVar("B_3", "B_3 ", 0.1, 0.0, 1.0)
    B_4 = ROOT.RooRealVar("B_4", "B_4 ", 0.1, 0.0, 1.0)
    BX1 = ROOT.RooFormulaVar("BX1", "BX1", '1.0 - @0', ROOT.RooArgList(B_1))
    BX2 = ROOT.RooFormulaVar("BX2", "BX2", '1.0 - @0 -@1', ROOT.RooArgList(B_1, B_2))
    BX3 = ROOT.RooFormulaVar("BX3", "BX3", '1.0 - @0 -@1 -@2', ROOT.RooArgList(B_1, B_2, B_3))
    BX4 = ROOT.RooFormulaVar("BX4", "BX4", '1.0 - @0 -@1 -@2 -@3', ROOT.RooArgList(B_1, B_2, B_3, B_4))

    if TwoGaus:
        S = ROOT.RooRealVar("S", "Signal", fit_N0, 4, 900000)
        S2_frac = ROOT.RooRealVar("S2_frac", "frac", 0.2, 0., 1.0)
        S1 = ROOT.RooFormulaVar("S1", "Signal", 'S * (1.0 - S2_frac)', ROOT.RooArgList(S, S2_frac))
        S2 = ROOT.RooFormulaVar("S2", "Signal", 'S * S2_frac', ROOT.RooArgList(S, S2_frac))
        S2_sigma = ROOT.RooRealVar("S2_sigma", "sigma", fit_Sigma0 * 1.5, 0.007, 0.08)
        pdfS2 = ROOT.RooGaussian("pdfS2", "gaus", mb, S1_mean, S2_sigma)

    pdfS1 = ROOT.RooGaussian("pdfS1", "gaus", mb, S1_mean, S1_sigma)

    # pdfB    = RooExponential("pdfB" , "pdfB"    , mb    , B_c)
    # pdfB    = RooBernstein("pdfB" , "pdfB"    , mb, RooArgList(B_1, BX1)) ## 1st order
    # pdfB    = RooBernstein("pdfB" , "pdfB"    , mb, RooArgList(B_1, B_2, BX2)) ## 2nd order
    # pdfB    = ROOT.RooBernstein("pdfB" , "pdfB"    , mb, ROOT.RooArgList(B_1, B_2, B_3, BX3)) ## 3rd order
    pdfB = ROOT.RooBernstein("pdfB", "pdfB", mb, ROOT.RooArgList(B_1, B_2, B_3, B_4, BX4))  # 4rd order

    alist1 = ROOT.RooArgList(pdfS1, pdfB);
    alist2 = ROOT.RooArgList(S1, B);

    if TwoGaus:
        alist1 = ROOT.RooArgList(pdfS1, pdfS2, pdfB);
        alist2 = ROOT.RooArgList(S1, S2, B);

    pdfSum = ROOT.RooAddPdf("model", "model", alist1, alist2)

    # FIX Mass and Sigma
    # S1_mean.setConstant(True)
    # S1_sigma.setConstant(True)
    if TwoGaus: S2_frac.setConstant(True)
    if TwoGaus: S2_sigma.setConstant(True)

    rrr = pdfSum.fitTo(datahist, ROOT.RooFit.NumCPU(4), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Save())
    # S1_sigma.setConstant(False)
    if TwoGaus: S2_sigma.setConstant(False)

    rrr = pdfSum.fitTo(datahist, ROOT.RooFit.NumCPU(4), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Save())
    # S1_mean.setConstant(False)
    rrr = pdfSum.fitTo(datahist, ROOT.RooFit.NumCPU(4), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Save())
    if TwoGaus: S2_frac.setConstant(False)
    rrr = pdfSum.fitTo(datahist, ROOT.RooFit.Save())

    cB = ROOT.TCanvas("cB", "cB", canvW, canvH)
    mframe = 0
    mframe = mb.frame(mbNbins)
    datahist.plotOn(mframe, ROOT.RooFit.MarkerSize(0.6))
    pdfSum.plotOn(mframe, ROOT.RooFit.Components('pdfB'), ROOT.RooFit.LineColor(ROOT.kBlue),
                  ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineWidth(2))
    pdfSum.plotOn(mframe, ROOT.RooFit.Components('pdfS1'), ROOT.RooFit.LineColor(ROOT.kGreen), ROOT.RooFit.LineWidth(1))

    # if TwoGaus : pdfSum.plotOn(mframe, ROOT.RooFit().Components('pdfS2'), ROOT.RooFit().LineColor(kGreen), ROOT.RooFit().LineWidth(1))

    pdfSum.plotOn(mframe, ROOT.RooFit.LineColor(ROOT.kRed))
    pdfSum.paramOn(mframe, ROOT.RooFit.Layout(0.57, 0.98, 0.94))
    datahist.plotOn(mframe, ROOT.RooFit.MarkerSize(0.6))
    mframe.SetTitle(_PicName)
    mframe.Draw()
    # L1=TLine(3.706, 0, 3.706, 300)
    # L2=TLine(3.666, 0, 3.666, 300)
    # L1.Draw("same")
    # L2.Draw("same")

    cB.SaveAs(_PicName)

    rrr.Print()

    LS = rrr.minNll()

    S1_sigma.setConstant(True)
    S1_mean.setConstant(True)

    if TwoGaus:
        S2_sigma.setConstant(True)
    # S1.setVal(0)
    # S1.setConstant(True)

    rrr = pdfSum.fitTo(datahist, ROOT.RooFit.NumCPU(4), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Save())
    # rrr = pdfSum.fitTo( datahist, RooFit.NumCPU(4), RooFit.PrintLevel(-1), RooFit.Save())
    # rrr = pdfSum.fitTo( datahist, RooFit.NumCPU(4), RooFit.PrintLevel(-1), RooFit.Save())

    L0 = rrr.minNll()

    prob = ROOT.TMath.Prob(L0 - LS, 1)
    print('Signif =', ROOT.TMath.ErfcInverse(prob) * sqrt(2.))

    signals.append(int(S.getValV()))
    signals_err.append(int(S.getError()))
    # print('\n\n\n\n\n\n   S1 = ' + str(S.getValV()) + '\n\n\n\n\n\n')

    # END

print(signals)
print(signals_err)

sign = array('d')

for i in range(0, 7):
    sign.append(signals[i] / signals_err[i])

cuts = array('d')
cuts.append(25)
cuts.append(20)
cuts.append(15)
cuts.append(10)
cuts.append(7)
cuts.append(5)
cuts.append(3)

print(cuts, sign)

graph = ROOT.TGraph(7, cuts, sign)

ff = ROOT.TFile("graf.root", "recreate")

graph.Write()

ff.Close()
