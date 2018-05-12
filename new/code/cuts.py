# from ROOT import *
import ROOT
import glob

ch = ROOT.TChain("mytree")
MyFileNames12 = glob.glob('../data/data.root')
for fName in MyFileNames12:
    ch.Add(fName)

print("Adding chain done", ch.GetNtrees(), 'files ')

hBmas1 = ROOT.TH1F('hBmas1', 'B_mass', 100, 6.2751 - 0.4751, 6.2751 + 0.6249)
hBmas2 = ROOT.TH1F('hBmas2', 'B_mass', 100, 6.2751 - 0.4751, 6.2751 + 0.6249)
hBmas3 = ROOT.TH1F('hBmas3', 'B_mass', 100, 6.2751 - 0.4751, 6.2751 + 0.6249)
hBmas4 = ROOT.TH1F('hBmas4', 'B_mass', 100, 6.2751 - 0.4751, 6.2751 + 0.6249)
hBmas5 = ROOT.TH1F('hBmas5', 'B_mass', 100, 6.2751 - 0.4751, 6.2751 + 0.6249)
hBmas6 = ROOT.TH1F('hBmas6', 'B_mass', 100, 6.2751 - 0.4751, 6.2751 + 0.6249)
hBmas7 = ROOT.TH1F('hBmas7', 'B_mass', 100, 6.2751 - 0.4751, 6.2751 + 0.6249)
hBmas8 = ROOT.TH1F('hBmas8', 'B_mass', 100, 6.2751 - 0.4751, 6.2751 + 0.6249)
hBmas9 = ROOT.TH1F('hBmas9', 'B_mass', 100, 6.2751 - 0.4751, 6.2751 + 0.6249)
hBmas10 = ROOT.TH1F('hBmas10', 'B_mass', 100, 6.2751 - 0.4751, 6.2751 + 0.6249)
hBmas11 = ROOT.TH1F('hBmas11', 'B_mass', 100, 6.2751 - 0.4751, 6.2751 + 0.6249)


cuts_cos = [0.985, 0.99, 0.995, 0.999, 0.9995, 0.9999, 0.99995]
cuts_sign = [3, 5, 7, 10, 15, 20, 25]
cuts_prob = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cuts_K1_pt = [1, 1.5, 2, 2.5, 3, 4, 6, 10]
cuts_dr = [0.1, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2]

cut_jpsi = 'JPSI_mass_Cmumu > 3.04 && JPSI_mass_Cmumu < 3.15'
cut_B_pt = ' && B_pt_Cjp > 8'

cut_sign = ' && B_pvdistsignif2_Cjp > ' + str(cuts_sign[1])
cut_K1_pt = ' && K1_pt > ' + str(cuts_K1_pt[4])
cut_prob = ' && B_vtxprob_Cjp > ' + str(cuts_prob[2])
cut_cos = ' && B_pvcos2_Cjp > ' + str(cuts_cos[3])
# cut_dr = ' && DRpiJ < ' + str(cuts_dr[0])

cut = cut_jpsi + cut_B_pt + cut_sign + cut_K1_pt + cut_prob + cut_cos

cuts = []

# for i in cuts_cos:
#     cuts.append(cut + ' && B_pvcos2_Cjp > ' + str(i))

# for i in cuts_sign:
#     cuts.append(cut + ' && B_pvdistsignif2_Cjp > ' + str(i))

# for i in cuts_prob:
#     cuts.append(cut + ' && B_vtxprob_Cjp > ' + str(i))

# for i in cuts_K1_pt:
#     cuts.append(cut + ' && K1_pt > ' + str(i))

for i in cuts_dr:
    cuts.append(cut + ' && DRpiJ < ' + str(i))

ch.Draw('B_mass_Cjp >> hBmas1', cut)
ch.Draw('B_mass_Cjp >> hBmas2', cuts[1])
ch.Draw('B_mass_Cjp >> hBmas3', cuts[2])
ch.Draw('B_mass_Cjp >> hBmas4', cuts[3])
ch.Draw('B_mass_Cjp >> hBmas5', cuts[4])
ch.Draw('B_mass_Cjp >> hBmas6', cuts[5])
ch.Draw('B_mass_Cjp >> hBmas7', cuts[6])
ch.Draw('B_mass_Cjp >> hBmas8', cuts[7])
ch.Draw('B_mass_Cjp >> hBmas9', cuts[8])
ch.Draw('B_mass_Cjp >> hBmas10', cuts[9])
# ch.Draw('B_mass_Cjp >> hBmas11', cuts[10])

ff = ROOT.TFile("../data/B_cut_dr.root", "recreate")

hBmas1.Write()
hBmas2.Write()
hBmas3.Write()
hBmas4.Write()
hBmas5.Write()
hBmas6.Write()
hBmas7.Write()
hBmas8.Write()
hBmas9.Write()
hBmas10.Write()
# hBmas11.Write()

ff.Close()
