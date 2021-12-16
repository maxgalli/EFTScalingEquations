import json
import sys
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import OrderedDict as od
import numpy as np

def loadEqns(directory):
  with open(os.path.join(directory, "prod.json"), "r") as f:
    prod = json.load(f, object_pairs_hook=od)
  with open(os.path.join(directory, "decay.json"), "r") as f:
    decay = json.load(f, object_pairs_hook=od)
  eqns = prod
  for decay_mode in decay.keys():
    eqns[decay_mode] = decay[decay_mode]
  return eqns

def findCommonBins(eqns1, eqns2):
  bins = eqns1.keys()
  bins_to_remove = []
  for b in bins:
    if b not in eqns2.keys():
      bins_to_remove.append(b)
  for b in bins_to_remove:
    bins.remove(b)
  return bins

def findAllParams(eqns):
  params = []
  for b in eqns.keys():
    for term in eqns[b].keys():
      if (term[0] != "u"):
        params += term.split("_")[1:]
  params = filter(lambda x: x != "2", params)
  return set(params)

def findCommonWilsonCoeffs(eqns1, eqns2):
  params1 = findAllParams(eqns1)
  params2 = findAllParams(eqns2)
  return params1.intersection(params2), params2.difference(params1), params1.difference(params2)

def makeComparisonPlot(params, values1, values2, errors1, errors2, title, saveinto):
  values1 = np.array(values1, dtype=float)
  values2 = np.array(values2, dtype=float)
  r1 = values1/values1
  r2 = values2/values1
  r1_err = errors1/values1
  r2_err = errors2/values1

  x = np.arange(len(params))
  plt.errorbar(x, r1, r1_err, fmt='o', fillstyle='none', capsize=2, color="blue", label="%s / %s"%(options.name1, options.name1))
  plt.errorbar(x, r2, r2_err, fmt='x', capsize=2, color="orange", label="%s / %s"%(options.name2, options.name1))

  y_bot, y_top = plt.ylim()
  y_range = y_top-y_bot
  offset = y_range/20
  for i in range(len(values1)):
    if abs(values1[i]) > abs(values2[i]):
      offset1 = offset
      offset2 = -offset
    else:
      offset1 = -offset
      offset2 = offset
    plt.text(i, r1[i]+offset1, "%.2g"%values1[i], horizontalalignment="center", verticalalignment="center", color="blue")
    plt.text(i, r2[i]+offset2, "%.2g"%values2[i], horizontalalignment="center", verticalalignment="center", color="orange")
  plt.ylim(y_bot-offset*1.5, y_top+offset*1.5)

  plt.xticks(x, params)
  plt.ylabel("Ratio")
  plt.legend()
  plt.title(title)
  plt.savefig(os.path.join(saveinto, title+".png"))
  plt.clf()

def makeComparisonPlots(eqns1, eqns2, bins, params, saveinto):
  os.system("mkdir -p %s"%saveinto)

  for b in bins:
    print(b)
    all_terms = set(eqns1[b].keys()).union(eqns2[b].keys())
    all_terms = list(filter(lambda x: x[0] != "u", all_terms)) #get rid of uncertainty terms
    all_terms = list(filter(lambda x: len(set(x.split("_")[1:]).intersection(params.union(["2"]))) == len(x.split("_")[1:]), all_terms)) #keep only terms made up with coeffs from params  
    all_terms = list(filter(lambda x: (x in eqns1[b].keys()) and (x in eqns2[b].keys()), all_terms)) #only compare terms that are both non zero

    values1 = [eqns1[b][term] for term in all_terms]
    values2 = [eqns2[b][term] for term in all_terms]
    errors1 = [eqns1[b]["u_"+term] if "u_"+term in eqns1[b].keys() else 0 for term in all_terms]
    errors2 = [eqns2[b]["u_"+term] if "u_"+term in eqns2[b].keys() else 0 for term in all_terms]
    makeComparisonPlot(all_terms, values1, values2, errors1, errors2, b, saveinto)    

if __name__=="__main__":
  from optparse import OptionParser
  parser = OptionParser(usage="%prog equations/set1 equations/set2")
  parser.add_option("--name1", dest="name1", default=None)
  parser.add_option("--name2", dest="name2", default=None)
  (options, args) = parser.parse_args()
  if options.name1 == None:
    options.name1 = args[0].strip("/").split("/")[-1]
  if options.name2 == None:
    options.name2 = args[1].strip("/").split("/")[-1]

  eqns1 = loadEqns(args[0])
  eqns2 = loadEqns(args[1])

  common_bins = findCommonBins(eqns1, eqns2)
  common_coeffs, missing_coeffs_from_1, missing_coeffs_from_2 = findCommonWilsonCoeffs(eqns1, eqns2)

  print(">> Common Wilson Coefficients:")
  for each in common_coeffs:
    print(" %s"%each)
  print(">> Wilson Coefficients missing from set 1:")
  for each in missing_coeffs_from_1:
    print(" %s"%each)
  print(">> Wilson Coefficients missing from set 2:")
  for each in missing_coeffs_from_2:
    print(" %s"%each)

  makeComparisonPlots(eqns1, eqns2, common_bins, common_coeffs, "comparisonPlots")