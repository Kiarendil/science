from ROOT import *; RAD = RooAbsData; RAD.setDefaultStorageType ( RAD.Tree )
from math import sqrt; from variables import * ## import vars
isMC = 0; nMC = 1;
from array import array

fileDS = TFile('../data/new.root', 'read')

signals, signals_err = array('d'), array('d')

for i in range(7):
    datasetI = fileDS.Get('ds' + str(i)).Clone();
    datasetI.Print()

    bumin = 5.90; bumax = 6.80; mbu.setMin(bumin); mbu.setMax(bumax); binN = 225  ## data ext
    # bumin = 5.17; bumax = 5.53; mbu.setMin(bumin); mbu.setMax(bumax); binN = 120  ## data baseline
    # bumin = 5.150; bumax = 5.400; mbu.setMin(bumin); mbu.setMax(bumax); binN = 100  ## MC
    _cutM = ' && mbu > %f && mbu < %f'%(bumin, bumax)

    dataset = datasetI.reduce(' 2 > 1 ' + _cutM )
    dataset.Print()

    ###                                          initial  lower   upper
    ###                                          values   bound   bound
    S       = RooRealVar ( "S"      , "Signal"  , 400000, 40    , 90000000)
    S_f1    = RooRealVar ( "S_f1"   , "frac"    , 0.32  , 0.    , 1.0   )
    S_f2    = RooRealVar ( "S_f2"   , "frac"    , 0.52  , 0.    , 1.0   )
    # S1      = RooFormulaVar( "S1"   , "Signal"  , 'S * (1.0 - S2_frac)', RooArgList(S,S2_frac))
    # S2      = RooFormulaVar( "S2"   , "Signal"  , 'S * S2_frac', RooArgList(S,S2_frac))

    S1_mean = RooRealVar ( "S1_mean", "mean "   , 6.2751, 6.1751 ,6.3751  )
    S1_sigma= RooRealVar ( "S1_sigma","sigma"   , 0.0113, 0.001 , 0.03  )
    S2_sigma= RooRealVar ( "S2_sigma","sigma"   , 0.021 , 0.007 , 0.055 )
    S3_sigma= RooRealVar ( "S3_sigma","sigma"   , 0.049 , 0.007 , 0.085 )

    pdfS1   = RooGaussian( "pdfS1"  , "gaus"    , mbu   ,S1_mean, S1_sigma)
    pdfS2   = RooGaussian( "pdfS2"  , "gaus"    , mbu   ,S1_mean, S2_sigma)
    pdfS3   = RooGaussian( "pdfS3"  , "gaus"    , mbu   ,S1_mean, S3_sigma)
    # pdfSig  = RooAddPdf  ("pdfSig", "pdfSig", RooArgList(pdfS1, pdfS2), RooArgList(S_f1))
    pdfSig  = RooAddPdf  ("pdfSig", "pdfSig", RooArgList(pdfS1, pdfS2, pdfS3), RooArgList(S_f1, S_f2))

    B       = RooRealVar ( "B"      , "B"       , 500000, 1     , 900000000 )
    B_c1    = RooRealVar ( "B_c1"   , "B_c1"    , -0.47 , -20   , 1         )
    # B_c     = RooRealVar ( "B_c"    , "B_c "    , 0.3   , -20   , 100   )
    # B_c2    = RooRealVar ( "B_c2"   , "B_c2"    , 0.00  , -20   , 30    )

    G       = RooRealVar ( "G"      , "G"       , 13000 , 1     , 900000 )
    R       = RooRealVar ( "R"      , "R"       , 35000 , 1     , 900000 )
    B_m0    = RooRealVar ( "B_m0"   , "B_m0"    , 5.107 , 5.05  , 5.22  )
    B_al    = RooRealVar ( "B_al"   , "B_al"    , 0.45  , 0.01  , 3.0   )
    B_si    = RooRealVar ( "B_si"   , "B_si"    , 0.026 , 0.008 , 0.2   )
    W_a     = RooRealVar    ( "W_a"    , "W_a " , 0.38  , 0.0   , 1.0       )
    # W_b     = RooRealVar    ( "W_b"    , "W_b " , 0.25  , 0.0   , 1.0       )
    W_b     = RooFormulaVar ( "W_b"    , "W_b " , '1.0 -W_a', RooArgList(W_a))
    # W_c     = RooRealVar    ( "W_c"    , "W_c "    , 0.15  , 0.0   , 1.0       )
    W_c     =  RooFormulaVar( "W_c"    , "W_c"     , '1.0 -W_a-W_b', RooArgList(W_a,W_b))

    m_jpsipi_mean1      = RooRealVar("m_jpsipi_mean1","m_jpsipi_mean1",5.34693e+00)
    m_jpsipi_mean2      = RooRealVar("m_jpsipi_mean2","m_jpsipi_mean2",5.46876e+00)
    m_jpsipi_mean3      = RooRealVar("m_jpsipi_mean3","m_jpsipi_mean3",5.48073e+00)
    m_jpsipi_sigma1l    = RooRealVar("m_jpsipi_sigma1l","m_jpsipi_sigma1l",2.90762e-02);
    m_jpsipi_sigma1r    = RooRealVar("m_jpsipi_sigma1r","m_jpsipi_sigma1r",6.52519e-02);
    m_jpsipi_sigma2     = RooRealVar("m_jpsipi_sigma2","m_jpsipi_sigma2",9.94712e-02);
    m_jpsipi_sigma3     = RooRealVar("m_jpsipi_sigma3","m_jpsipi_sigma3",3.30152e-01);
    m_jpsipi_fraction2  = RooRealVar("m_jpsipi_fraction2","m_jpsipi_fraction2",2.34646e-01);
    m_jpsipi_fraction3  = RooRealVar("m_jpsipi_fraction3","m_jpsipi_fraction3",1.14338e-01);
    m_jpsipi_gaussian1  = RooBifurGauss ("m_jpsipi_gaussian1","m_jpsipi_gaussian1",mbu,m_jpsipi_mean1,m_jpsipi_sigma1l,m_jpsipi_sigma1r);
    m_jpsipi_gaussian2  = RooGaussian   ("m_jpsipi_gaussian2","m_jpsipi_gaussian2",mbu,m_jpsipi_mean2,m_jpsipi_sigma2);
    m_jpsipi_gaussian3  = RooGaussian   ("m_jpsipi_gaussian3","m_jpsipi_gaussian3",mbu,m_jpsipi_mean3,m_jpsipi_sigma3);
    pdfJPI              = RooAddPdf     ("pdfJPI","pdf_m_jpsipi",RooArgList(m_jpsipi_gaussian3,m_jpsipi_gaussian2,m_jpsipi_gaussian1),RooArgList(m_jpsipi_fraction3,m_jpsipi_fraction2));


    RR_mean = RooRealVar ( "RR_mean", "mean "   , 5.1   , 4.9   , 5.2   )
    RR_sigma= RooRealVar ( "RR_sigma","sigma"   , 0.03  , 0.001 , 0.3   )
    pdfRR   = RooGaussian( "pdfRR"  , "gaus"    , mbu   ,RR_mean, RR_sigma)

    pdfW    = RooBernstein  ("pdfW" , "pdfW"    , mbu, RooArgList(W_a, W_b))#, W_c))
    pdfG    = RooGenericPdf ("pdfG" , "@1 - @0 > 0.0000001 ? ((@1 - @0)^@2) : 0.0", RooArgList(mbu, B_m0, B_al))
    pdfWG   = RooProdPdf    ("pdfWG", "pdfWG"   , RooArgList ( pdfW, pdfG))

    pdfB    = RooExponential("pdfB" , "pdfB"    , mbu   , B_c1)
    # pdfWB   = RooProdPdf ("pdfWB"   , "pdfWB"   , RooArgList(pdfW,pdfB))

    # alist1  = RooArgList (pdfSig, pdfB, pdfWG);  alist2 = RooArgList (S, B, G);
    # alist1  = RooArgList (pdfSig, pdfB, pdfRR);  alist2 = RooArgList (S, B, G);
    if isMC==0:
        alist1  = RooArgList (pdfSig, pdfB, pdfJPI);  alist2 = RooArgList (S, B, G);
        if (bumin < 5.169):
            alist1  = RooArgList (pdfSig, pdfB, pdfJPI, pdfRR);  alist2 = RooArgList (S, B, G, R);
        #
    else:
        alist1  = RooArgList (pdfSig, pdfB);  alist2 = RooArgList (S, B);

    pdfSum  = RooAddPdf  ("model", "model", alist1, alist2)


    B_m0.setConstant(True)
    W_a.setConstant(True)
    S_f1.setConstant(True)
    S_f2.setConstant(True)
    R.setConstant(True)
    RR_mean.setConstant(True)
    RR_sigma.setConstant(True)
    S1_sigma.setConstant(True)
    S2_sigma.setConstant(True)
    S3_sigma.setConstant(True)
    # W_b.setConstant(True)
    S1_mean.setConstant(True);
    # G.setConstant(True);B_m0.setConstant(True);B_al.setConstant(True);B_si.setConstant(True)
    rrr = pdfSum.fitTo( dataset, RooFit.NumCPU(7), RooFit.PrintLevel(-1), RooFit.Save())
    W_a.setConstant(False)
    # W_b.setConstant(False)
    rrr = pdfSum.fitTo( dataset, RooFit.NumCPU(7), RooFit.PrintLevel(-1), RooFit.Save())
    B_m0.setConstant(False)
    rrr = pdfSum.fitTo( dataset, RooFit.NumCPU(7), RooFit.PrintLevel(-1), RooFit.Save())
    S1_sigma.setConstant(False)
    S2_sigma.setConstant(False)
    S3_sigma.setConstant(False)
    rrr = pdfSum.fitTo( dataset, RooFit.NumCPU(7), RooFit.PrintLevel(-1), RooFit.Save())
    S1_mean.setConstant(False);
    rrr = pdfSum.fitTo( dataset, RooFit.NumCPU(7), RooFit.PrintLevel(-1), RooFit.Save())
    R.setConstant(False)
    RR_mean.setConstant(False)
    RR_sigma.setConstant(False)
    rrr = pdfSum.fitTo( dataset, RooFit.NumCPU(7), RooFit.Save())
    S_f1.setConstant(False)
    S_f2.setConstant(False)
    rrr = pdfSum.fitTo( dataset, RooFit.NumCPU(7), RooFit.PrintLevel(-1), RooFit.Save())
    rrr = pdfSum.fitTo( dataset, RooFit.NumCPU(7), RooFit.PrintLevel(-1), RooFit.Save())
    rrr = pdfSum.fitTo( dataset, RooFit.NumCPU(7), RooFit.PrintLevel(-1), RooFit.Save())
    rrr = pdfSum.fitTo( dataset, RooFit.NumCPU(7), RooFit.PrintLevel(-1), RooFit.Save())
    rrr.Print()

    sigma_eff = sqrt (  S_f1.getVal()       *   (S1_sigma.getVal() ** 2)    +
                        S_f2.getVal()       *   (S2_sigma.getVal() ** 2)    +
       (1.0 - S_f1.getVal() - S_f2.getVal())*   (S3_sigma.getVal() ** 2)    )



    _MYW = 800; _MYH = 600
    _MYT = 0.08*_MYH; _MYB = 0.14*_MYH;
    _MYL = 0.15*_MYW; _MYR = 0.04*_MYW;

    _MYcanvName = 'fit_cos_' + str(i);
    cB = TCanvas("cB","cB",_MYW,_MYH);

    cB.SetLeftMargin( _MYL/_MYW );  cB.SetRightMargin( _MYR/_MYW );
    cB.SetTopMargin( _MYT/_MYH );   cB.SetBottomMargin( _MYB/_MYH );
    cB.SetTickx(0); cB.SetTicky(0);
    # cB.SetLogy()

    # bufram = 0;
    bufram = mbu.frame(binN);
    bufram.GetXaxis().SetTitleOffset(1.0); bufram.GetYaxis().SetTitleOffset(1.3);
    dataset.plotOn( bufram, RooFit.MarkerSize(0.6), RooFit.Name('data'));

    pdfSum.plotOn(  bufram,     RooFit.Components('pdfB'),
                                RooFit.LineColor(9),
                                RooFit.LineStyle(2),
                                RooFit.LineWidth(2),
                                RooFit.Name('bkgr'))

    pdfSum.plotOn(  bufram,     RooFit.Components('pdfJPI'),
                                RooFit.LineColor(4),
                                RooFit.LineStyle(9),
                                RooFit.LineWidth(2),
                                RooFit.Range(5.25, bumax),
                                RooFit.Name('jppi'))

    pdfSum.plotOn(  bufram,     RooFit.Components('pdfRR'),
                                RooFit.LineColor(4),
                                RooFit.LineStyle(7),
                                RooFit.LineWidth(2),
                                RooFit.Range(5.1, 5.17),
                                RooFit.Name('refl'))

    pdfSum.plotOn(  bufram,     RooFit.Components('pdfSig'),
                                RooFit.LineColor(kGreen+2),
                                RooFit.LineStyle(5),
                                RooFit.LineWidth(2),
                                RooFit.Name('sign'),
                                RooFit.Range(S1_mean.getVal()-5.0*sigma_eff, S1_mean.getVal()+5.0*sigma_eff)  )

    dataset.plotOn( bufram, RooFit.MarkerSize(0.6), RooFit.Name('data'));
    pdfSum.plotOn(  bufram,     RooFit.LineColor(2),
                                RooFit.LineStyle(1),
                                RooFit.LineWidth(3),
                                RooFit.Name('fitt'),
                                RooFit.Range(bumin, bumax) )

    dataset.plotOn( bufram, RooFit.MarkerSize(0.6), RooFit.Name('data'));
    # bufram.SetTitle('')##nn
    bufram.SetTitle('S='+str(S.getVal())[:8]+'+-'+str(S.getError())[:5]+'__M='+str(1000*S1_mean.getVal())[:7]+'+-'+str(1000*S1_mean.getError())[:5])
    bufram.Draw()

    leg = TLegend(0.71,0.70 if isMC else 0.61,0.93,0.90);
    leg.SetTextFont(42)
    leg.SetTextSize(0.05)
    leg.AddEntry(bufram.findObject('data')  ,"Data"     , "ep");
    leg.AddEntry(bufram.findObject('fitt')  ,"Fit"      , "l");
    leg.AddEntry(bufram.findObject('sign')  ,"Signal"   , "l");
    leg.AddEntry(bufram.findObject('bkgr')  ,"Comb. Bkg", "l");
    leg.AddEntry(bufram.findObject('jppi')  ,"B^{+}#rightarrowJ/#psi#pi^{+}", "l")
    leg.AddEntry(bufram.findObject('refl')  ,"B#rightarrowJ/#psiK^{+}X", "l");

    leg.Draw('same');
    #

    # cB.Update(); cB.RedrawAxis(); cB.GetFrame().Draw();

    cB.SaveAs("../pictures/" + _MYcanvName + ".pdf");
    # cB.SaveAs(_MYcanvName + ".pdf");

    # cB.SaveAs( _MYcanvName+".png");
    # cB.SaveAs( _MYcanvName+".eps");
    # _fi=TFile( _MYcanvName+".root", 'recreate')
    # cB.Write()
    # rrr.Write()
    # _fi.Close()


    # __ps = RooArgSet(S, S1_mean, S1_sigma, S2_sigma, B, B_c1)
    # pdfSum.paramOn(bufram, RooFit.Parameters(__ps), RooFit.Layout(0.55,0.9,0.9));
    # pdfSum.paramOn(bufram, RooFit.Layout(0.55,1.0 - _MYR/_MYW, 0.77)); bufram.Draw();
    # leg.Draw('same');
    # cB.Update(); cB.RedrawAxis(); cB.GetFrame().Draw(); cB.SaveAs(_MYcanvName+".gif")
    #
    rrr.Print();
    print 'sigma_eff =', sigma_eff

    print S.getVal(), S.getError()
    signals.append(int(S.getValV()))
    signals_err.append(int(S.getError()))

fileDS.Close()

print signals
print signals_err

significance = array('d')

for i in range(7):
    significance.append(signals[i] / signals_err[i])

cuts_cos = array('d', [0.985, 0.99, 0.995, 0.999, 0.9995, 0.9999, 0.99995])

print cuts_cos, significance

graph = TGraph(7, cuts_cos, significance)

graph.SetTitle('cuts_cos')

ff = TFile("../data/grafs.root", "recreate")

graph.Write()

ff.Close()
