# from ROOT import *
import ROOT

PDG_MUON_MASS = 0.1056583745;
PDG_PION_MASS = 0.13957018;
PDG_KAON_MASS = 0.493677;
PDG_PROTON_MASS = 0.9382720813;
PDG_KSHORT_MASS = 0.497611;
PDG_KSHORT_DM = 0.000013;
PDG_KSHORT_TIME = 0.8954 * 0.0000000001;
PDG_KS_MASS = PDG_KSHORT_MASS;
PDG_LAMBDA_MASS = 1.115683;
PDG_LAMBDA_DM = 0.000006;
PDG_LAMBDA_TIME = 2.632 * 0.0000000001;
PDG_SIGMA0_MASS = 1.192642;
PDG_XImunus_MASS = 1.32171;
PDG_XImunus_DM = 0.00007;
PDG_XImunus_TIME = 1.639 * 0.0000000001;
PDG_KSTAR_MASS = 0.89581;
PDG_KSTAR_GAMMA = 0.0508;
PDG_PHI_MASS = 1.019461;
PDG_PHI_GAMMA = 0.004266;
PDG_JPSI_MASS = 3.096900;
PDG_PSI2S_MASS = 3.686097;
PDG_X3872_MASS = 3.87169;
PDG_BU_MASS = 5.27931;
PDG_B0_MASS = 5.27962;
PDG_dm_BST_B = 0.04518;
PDG_BS_MASS = 5.36682;
PDG_BC_MASS = 6.2751;
PDG_LB_MASS = 5.61951;
PDG_C = 29979245800.;  ## in cm/c
PDG_LIFETIME_BU = 1.638 * (10 ** -12)  ## in s
PDG_LIFETIME_B0 = 1.52 * (10 ** -12)  ## in s
PDG_LIFETIME_BS = 1.511 * (10 ** -12)  ## in s
PDG_LIFETIME_KS = 0.8954 * (10 ** -10)  ## in s
PDG_LIFETIME_LAMBDA = 2.632 * (10 ** -10)  ## in s
PDG_LIFETIME_LB = 1.466 * (10 ** -12)  ## in s
PDG_BS2_MASS = 5.83983
PDG_BS1_MASS = 5.82878
PDG_B1_MASS = 5.7249
PDG_B2ST_MASS = 5.739
PDG_DMBstB = 0.04538

bmin = 5.9
bmax = 6.8
binN = 100
# bmin = 5.77;   __bmax = 5.795; binN = 25

# tt1 = 0.0;tt2 = 15
# tt1 = 0.0;tt2 = 0.03
tt1 = 0.0
tt2 = 1.0

mbu = ROOT.RooRealVar("mbu", "M(bu), [GeV]", 5.9, 6.8)
mjpsi = ROOT.RooRealVar("mjpsi", "M(psi), [GeV]", 2.8, 4.0)
lacos = ROOT.RooRealVar("lacos", "cos(theta)", -1.1, 1.1)
lads = ROOT.RooRealVar("lads", "DetSign", 0.0, 10000)
ptpi = ROOT.RooRealVar("ptpi", "ptpi", 0.0, 5.0)
ipspi = ROOT.RooRealVar("ipspi", "ipspi", 0.0, 1000.0)
vtxxi = ROOT.RooRealVar("vtxxi", "vtxxi", 0., 1.0)
mom = ROOT.RooRealVar("mom", "M(Om), [GeV]", 1.6, 1.8)


### Tp = Tlab * sqrt(1-v2/c2) = d/v * sqrt(1-v2/c2)
### p = m*v / sqrt(1-v2/c2)
### sqrt(1-v2/c2) = m*v/p
### m2v2c2/p2c2 + v2/c2= 1
### v = c * sqrt(1/(1+m2c2/p2)) [=~ c * (1-m2c2/2p2)]
### Tp = d/v * sqrt(1-1/(1+m2c2/p2))
### 
def DetachSignificance2(vtx, vtxE1, vtxE2):
    return sqrt(vtx.X() ** 2 / (vtxE1.X() ** 2 + vtxE2.X() ** 2) + vtx.Y() ** 2 / (vtxE1.Y() ** 2 + vtxE2.Y() ** 2));


def DetachSignificance3(vtx, vtxE1, vtxE2):
    return sqrt(vtx.X() ** 2 / (vtxE1.X() ** 2 + vtxE2.X() ** 2) + vtx.Y() ** 2 / (
                vtxE1.Y() ** 2 + vtxE2.Y() ** 2) + vtx.Z() ** 2 / (vtxE1.Z() ** 2 + vtxE2.Z() ** 2));


def DirectionCos2(v1, v2):
    r1 = sqrt(v1.X() ** 2 + v1.Y() ** 2);
    r2 = sqrt(v2.X() ** 2 + v2.Y() ** 2);
    return (v1.X() * v2.X() + v1.Y() * v2.Y()) / (r1 * r2 + 0.0000001);


def DirectionCos3(v1, v2):
    r1 = sqrt(v1.X() ** 2 + v1.Y() ** 2 + v1.Z() ** 2);
    r2 = sqrt(v2.X() ** 2 + v2.Y() ** 2 + v2.Z() ** 2);
    return (v1.X() * v2.X() + v1.Y() * v2.Y() + v1.Z() * v2.Z()) / (r1 * r2 + 0.0000001)


def DirectionChi22(vtx0, vtx0E, vtx1, vtx1E, P, PE):
    dvtx = vtx1 - vtx0;
    dvtxE = TVector3(sqrt(vtx0E.X() ** 2 + vtx1E.X() ** 2), sqrt(vtx0E.Y() ** 2 + vtx1E.Y() ** 2),
                     sqrt(vtx0E.Z() ** 2 + vtx1E.Z() ** 2))
    Pscaled = P * (dvtx.Mag() / P.Mag())
    PscaledE = PE * (dvtx.Mag() / P.Mag())
    return DetachSignificance2(Pscaled - dvtx, PscaledE, dvtxE);


def DirectionChi23(vtx0, vtx0E, vtx1, vtx1E, P, PE):
    dvtx = vtx1 - vtx0  ## vertex difference
    dvtxE = TVector3(sqrt(vtx0E.X() ** 2 + vtx1E.X() ** 2), sqrt(vtx0E.Y() ** 2 + vtx1E.Y() ** 2),
                     sqrt(vtx0E.Z() ** 2 + vtx1E.Z() ** 2))  ## its error
    Pscaled = P * (dvtx.Mag() / P.Mag())  ## scaled momentum to be the same length as vertex difference
    PscaledE = PE * (dvtx.Mag() / P.Mag())  ## its error
    return DetachSignificance3(Pscaled - dvtx, PscaledE, dvtxE);
