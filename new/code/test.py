# from ROOT import *
import ROOT
import glob

ch = ROOT.TChain("ds0")
MyFileNames1B = glob.glob('../data/new.root')
MyFileNames = MyFileNames1B

fileDS = ROOT.TFile('../data/new.root', 'read')

datasetI = fileDS.Get('ds' + str(0)).Clone()
datasetI.Print()

cut = 'B_pvdistsignif2_Cjp > 3'
datasetI.createHistogram(mass, 2, cut, "hist")

MyFileNames12 = glob.glob('../data/new.root')
for fName in datasetI:
    ch.Add(fName)

print("Adding chain done", ch.GetNtrees(), 'files ')
print('variables: ')

for v in [a.GetName() for a in ch.GetListOfLeaves()]:
    print(v)

hBmas1 = ROOT.TH1F('hBmas1', 'B_mass', 100, 6.2751 - 0.4751, 6.2751 + 0.6249)

ch.Draw('B_mass_Cjp >> hBmas1', cut)

ff = ROOT.TFile("../data/test.root", "recreate")

hBmas1.Write()

ff.Close()
