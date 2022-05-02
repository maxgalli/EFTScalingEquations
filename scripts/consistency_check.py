from imp import load_compiled
import json
import sys
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
#plt.rcParams['figure.constrained_layout.use'] = True
from collections import OrderedDict as od
import numpy as np
import pandas as pd

def loadEqns(directory):
  with open(os.path.join(directory, "prod.json"), "r") as f:
    prod = json.load(f, object_pairs_hook=od)
  with open(os.path.join(directory, "decay.json"), "r") as f:
    decay = json.load(f, object_pairs_hook=od)
  eqns = prod
  for decay_mode in decay.keys():
    eqns[decay_mode] = decay[decay_mode]
  return eqns

def loadJson(path):
  with open(path, "r") as f:
    return json.load(f, object_pairs_hook=od)

def findCommonBins(eqns1, eqns2):
  bins = list(eqns1.keys())
  bins_to_remove = []
  for b in bins:
    if b not in eqns2.keys():
      bins_to_remove.append(b)
  for b in bins_to_remove:
    bins.remove(b)

  missing_from_1 = set(eqns2.keys()).difference(eqns1.keys())
  missing_from_2 = set(eqns1.keys()).difference(eqns2.keys())
  return bins, missing_from_1, missing_from_2

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

def getChi2(values1, values2, errors1, errors2):
  diff = values1 - values2
  diff_error2 = errors1**2 + errors2**2
  return np.sum(diff**2 / diff_error2)

def makeComparisonPlot(terms, values1, values2, errors1, errors2, title, saveinto):
  params, missing_from_1, missing_from_2 = terms

  #values1 = np.array(values1, dtype=float)
  #values2 = np.array(values2, dtype=float)
  #errors1 = np.array(errors1, dtype=float)
  #errors2 = np.array(errors2, dtype=float)

  chi2 = getChi2(values1, values2, errors1, errors2)
  chi2_adj = getChi2(values1, values2, errors1+abs(values1)*0.01, errors2+abs(values2)*0.01) #add a 1% relative error

  idx = np.argsort(abs(values1))[::-1]
  params = [params[i] for i in idx]
  values1 = values1[idx]
  values2 = values2[idx]
  errors1 = errors1[idx]
  errors2 = errors2[idx]

  r1 = values1/values1
  r2 = values2/values1
  r1_err = errors1/values1
  r2_err = errors2/values1

  x = np.arange(len(params))
  plt.errorbar(x, r1, r1_err, fmt='o', fillstyle='none', capsize=2, color="blue", label="%s / %s"%(options.name1, options.name1))
  plt.errorbar(x, r2, r2_err, fmt='x', capsize=2, color="orange", label="%s / %s"%(options.name2, options.name1))

  plt.ylim(-1,2)

  y_bot, y_top = plt.ylim()
  y_range = y_top-y_bot
  offset = y_range/10
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

  x_min, x_max = plt.xlim()
  plt.xlim(x_min-0.5, x_max+0.5)
  #x_min, x_max = plt.xlim()
  #offset = (x_max-x_min)*0.2
  #plt.xlim(x_min, x_max+offset)

  missing_text_1 = "Missing from %s:\n"%options.name1 + "\n".join(missing_from_1)
  plt.text(x_max, y_top, missing_text_1, horizontalalignment="left", verticalalignment="top")
  missing_text_2 = "Missing from %s:\n"%options.name2 + "\n".join(missing_from_2)
  plt.text(x_max, y_bot, missing_text_2, horizontalalignment="left", verticalalignment="bottom")

  plt.text(x_min, y_bot, r"$\chi^2 = %.1f / %d$"%(chi2, len(values1)), horizontalalignment="left", verticalalignment="bottom")
  plt.text(x_min, y_bot, r"$\chi^2_{adj} = %.1f / %d$"%(chi2_adj, len(values1)), horizontalalignment="left", verticalalignment="top")

  plt.xticks(x, params)
  plt.ylabel("Ratio")
  plt.legend(loc="upper left")
  plt.title(title)

  fig = matplotlib.pyplot.gcf()
  width, height = fig.get_size_inches()
  if len(params) > 5: width = 0.6 * (len(params)/5) * width
  fig.set_size_inches(width, 3)

  plt.savefig(os.path.join(saveinto, title+".png"))
  plt.savefig(os.path.join(saveinto, title+".pdf"))

  plt.close()

def getPulls(common_terms, values1, values2, errors1, errors2):
  diff = abs(values1 - values2)
  diff_error = np.sqrt(errors1**2 + errors2**2)
  pull_array = diff / diff_error
  #pull_array = abs(diff / ((values1+values2)/2)) * 100

  pull_dict = {}
  for i, term in enumerate(common_terms):   
    pull_dict[term] = pull_array[i]
  return pull_dict

def makePullPlot(pulls, saveinto):
  pulls = pd.DataFrame(pulls).T
  pulls.sort_index(axis=1, inplace=True)
  pulls.replace(np.nan, 0, inplace=True)

  print(pulls)
  print(pulls.max().max())

  #plt.imshow(pulls, cmap="OrRd", norm=matplotlib.colors.LogNorm(vmax=pulls.max().max()*10))  
  #plt.imshow(pulls, cmap="OrRd")
  #plt.imshow(pulls, cmap="afmhot_r")
  plt.imshow(pulls, cmap="RdYlGn_r")
  
  plt.xticks(ticks=np.arange(len(pulls.columns)), labels=pulls.columns, fontsize=8, rotation='vertical')
  plt.yticks(ticks=np.arange(len(pulls.index)), labels=pulls.index, fontsize=8)

  plt.gca().set_xticks(ticks=np.arange(len(pulls.columns))+0.5, minor=True)
  plt.gca().set_yticks(ticks=np.arange(len(pulls.index))+0.5, minor=True)

  plt.grid(color='0.8', linestyle="-", linewidth=1, which="minor")  
  cbar = plt.colorbar()
  cbar.set_label("Pull")

  fig = matplotlib.pyplot.gcf()
  #width, height = fig.get_size_inches()
  #if len(params) > 5: width = 0.6 * (len(params)/5) * width
  fig.set_size_inches(30, 20)

  plt.savefig(os.path.join(saveinto, "pulls.png"))
  plt.savefig(os.path.join(saveinto, "pulls.pdf"))

def makeComparisonPlots(eqns1, eqns2, bins, params, saveinto, noLinear=False, noQuadratic=False, noCross=False):
  os.system("mkdir -p %s"%saveinto)

  pulls = {}

  for b in bins:
  #for b in ["bb", "cc", "tautau", "gg", "Zgam", "gamgam"]:
  #for b in ["llll", "llnunu", "llqq", "lnuqq", "nunuqq", "qqqq"]:
    print(b)
    all_terms = set(eqns1[b].keys()).union(eqns2[b].keys())
    all_terms = list(filter(lambda x: x[0] != "u", all_terms)) #get rid of uncertainty terms
    all_terms = list(filter(lambda x: len(set(x.split("_")[1:]).intersection(params.union(["2"]))) == len(x.split("_")[1:]), all_terms)) #keep only terms made up with coeffs from params  
    #all_terms = list(filter(lambda x: (x in eqns1[b].keys()) and (x in eqns2[b].keys()), all_terms)) #only compare terms that are both non zero

    #all_terms = list(filter(lambda x: "chb_chwb" not in x, all_terms))

    if noLinear:
      all_terms = list(filter(lambda x: "A" not in x, all_terms))
    if noQuadratic:
      all_terms = list(filter(lambda x: "_2" not in x, all_terms))
    if noCross:
      all_terms = list(filter(lambda x: ("A" in x) or ("_2" in x), all_terms))

    common_terms = list(filter(lambda x: (x in eqns1[b].keys()) and (x in eqns2[b].keys()), all_terms))
    #missing_from_1 = list(filter(lambda x: (x not in eqns1[b].keys()) and (x in eqns2[b].keys()), all_terms))
    #missing_from_2 = list(filter(lambda x: (x  in eqns1[b].keys()) and (x not in eqns2[b].keys()), all_terms))
    params1 = []
    for key in eqns1[b].keys():
      if key[0]!="u": params1 += key.split("_")[1:]
    params2 = []
    for key in eqns2[b].keys():
      if key[0]!="u": params2 += key.split("_")[1:]

    params1 = set(params1).intersection(params)
    params2 = set(params2).intersection(params)
    missing_from_1 = params2.difference(params1)
    missing_from_2 = params1.difference(params2)

    terms = [common_terms, missing_from_1, missing_from_2]

    values1 = np.array([eqns1[b][term] for term in common_terms], dtype=float)
    values2 = np.array([eqns2[b][term] for term in common_terms], dtype=float)
    errors1 = np.array([eqns1[b]["u_"+term] if "u_"+term in eqns1[b].keys() else 0 for term in common_terms], dtype=float)
    errors2 = np.array([eqns2[b]["u_"+term] if "u_"+term in eqns2[b].keys() else 0 for term in common_terms], dtype=float)
    makeComparisonPlot(terms, values1, values2, errors1, errors2, b, saveinto)
    pulls[b] = getPulls(common_terms, values1, values2, errors1+abs(values1)*0.01, errors2+abs(values2)*0.01)

  makePullPlot(pulls, saveinto)

if __name__=="__main__":
  from optparse import OptionParser
  parser = OptionParser(usage="%prog equations/set1 equations/set2 [options]")
  parser.add_option("--name1", dest="name1", default=None)
  parser.add_option("--name2", dest="name2", default=None)
  #parser.add_option("--json1", dest="json1", default=None)
  #parser.add_option("--json2", dest="json2", default=None)
  parser.add_option("--noLinearTerms", action="store_true")
  parser.add_option("--noQuadraticTerms", action="store_true")
  parser.add_option("--noCrossTerms", action="store_true")
  parser.add_option("--outdir", dest="outdir", default="comparisonPlots")
  parser.add_option("--excludeProcs", dest="excludeProcs", help="Comma separated list of bins to exclude. Will exclude all bins with matching string in name.", default=None)
  (options, args) = parser.parse_args()
  if options.name1 == None:
    options.name1 = args[0].strip("/").split("/")[-1]
  if options.name2 == None:
    options.name2 = args[1].strip("/").split("/")[-1]

  if ".json" in args[0]:
    eqns1 = loadJson(args[0])
    eqns2 = loadJson(args[1])
  else:
    eqns1 = loadEqns(args[0])
    eqns2 = loadEqns(args[1])

  common_bins, missing_bins_from_1, missing_bins_from_2 = findCommonBins(eqns1, eqns2)
  common_coeffs, missing_coeffs_from_1, missing_coeffs_from_2 = findCommonWilsonCoeffs(eqns1, eqns2)

  print(">> Common bins:")
  for each in common_bins:
    print(" %s"%each)
  print(">> Bins missing from set 1:")
  for each in missing_bins_from_1:
    print(" %s"%each)
  print(">> Bins missing from set 2:")
  for each in missing_bins_from_2:
    print(" %s"%each)

  print(">> Common Wilson Coefficients:")
  for each in common_coeffs:
    print(" %s"%each)
  print(">> Wilson Coefficients missing from set 1:")
  for each in missing_coeffs_from_1:
    print(" %s"%each)
  print(">> Wilson Coefficients missing from set 2:")
  for each in missing_coeffs_from_2:
    print(" %s"%each)

  if options.excludeProcs != None:
    bins_to_include = []
    for each in common_bins:
      should_include = True
      for exclude in options.excludeProcs.split(","):
        if exclude in each:
          should_include = False
          break
      if should_include: bins_to_include.append(each)
  else:
    bins_to_include = common_bins
 
  makeComparisonPlots(eqns1, eqns2, bins_to_include, common_coeffs, options.outdir, options.noLinearTerms, options.noQuadraticTerms, options.noCrossTerms)