from ROOT import *; RAD = RooAbsData; RAD.setDefaultStorageType ( RAD.Tree )
from math import sqrt; from variables import * ## import vars
isMC = 0; nMC = 1;
from array import array


cuts = array('d')
cuts.append(0.99)
cuts.append(0.995)
cuts.append(0.999)
cuts.append(0.9995)
cuts.append(0.9999)
cuts.append(0.99995)

cuts = array('d', [3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 25.0])
sign = array('d', [104.43515037593986, 200.61371841155236, 102.22428174235404, 98.0989110707804, 87.82176520994001, 101.05460385438973, 115.80135135135136])


print cuts, sign

graph = TGraph(7, cuts, sign)
graph.SetTitle('cuts_sign')

ff = TFile("../data/new_grafs.root", "update")

graph.Write()

ff.Close()
