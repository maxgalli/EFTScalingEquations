import json
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import OrderedDict as od
import numpy as np
import os

import mplhep as hep

proc_groups = ["GG2H", "QQ2HQQ", "QQ2HLNU", "QQ2HLL", "GG2HLL", "TTH", "THW", "THQ", "BBH"]

param_groups = [
  ["chb", "chwb", "chw", "cuwre", "ctwre", "cubre", "ctbre", "chdd", "cw"],
  ["chq3", "chd", "chu", "chq1", "chl1", "che", "cehre", "cbhre"],
  ["chl3", "cll1"],  
  ["chg", "ctgre", "cthre", "cg", "cqu8"]
]

param_groups = [
  ["chb", "chwb", "chw", "cw"],
  ["chj3", "chd", "chu", "chj1"],
  ["chl3", "cll1", "chbox", "chdd"],  
  ["chg", "ctgre", "cthre", "cg", "cqu8"]
]

def loadEqn(json_path):
  with open(json_path, "r") as f:
    eq = json.load(f, object_pairs_hook=od)
  return eq

def getDeltaMu(eqns, bin_name, coeff, val):
  A = B = 0
  if "A_%s"%coeff in eqns[bin_name].keys():
    A = eqns[bin_name]["A_%s"%coeff]
  if "B_%s"%coeff in eqns[bin_name].keys():
    B = eqns[bin_name]["B_%s"%coeff]

  #return A*val + B*val*val
  return A*val

def getVal(eqns, coeff):
  possible_vals = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2, 5, 10]
  
  max_delta_mu = 0
  for bin_name in eqns.keys():
    new_delta_mu = abs(getDeltaMu(eqns, bin_name, coeff, 1.0))
    if new_delta_mu > max_delta_mu:
      max_delta_mu = new_delta_mu

  assert max_delta_mu != 0, coeff
  perfect_val = 1 / max_delta_mu
  for val in possible_vals[::-1]:
    if perfect_val > val:
      return val

style = hep.style.CMS
#style['font.size'] = 20
plt.style.use(hep.style.CMS)

# fig, axs = plt.subplots(4, 1, sharex=True, sharey='row')
# fig.set_size_inches(10, 10)
# hep.cms.text("Work in progress", ax=axs[0])

# bin_groups = 5
# n_bins = 4
# n_coeff = 4

# xtick_loc = []

# for ax in axs:
#   ax.set_ylim(-1, 1)

#   for i in range(bin_groups):
#     for j in range(n_bins):
#       bin_x = i*n_bins*n_coeff + j*n_coeff + i*n_coeff
#       xtick_loc.append(bin_x)
#       ax.plot([bin_x, bin_x], [-1, 1], '--', color='0.8', zorder=-1)

#       for k in range(n_coeff):
#         coeff_x = bin_x + k
#         ax.bar([coeff_x], np.random.random(1)-0.5, align='edge')
#       ax.set_prop_cycle(None)
      
#     if i != bin_groups-1:
#       pass
#       ax.plot([coeff_x+1, coeff_x+1], [-1, 1], '--', color='0.8', zorder=-1)
#       ax.fill_between([coeff_x+1+0.1, coeff_x+n_coeff+1-0.1], -1, 1, color='0.95', zorder=-1)

# axs[3].set_xlim(0, coeff_x+1)
# axs[3].set_xticks(xtick_loc[:len(xtick_loc)//4])
# axs[3].minorticks_off()
# labels = ["g%d_b%d"%(j,i)+i*"o" for i in range(n_bins) for j in range(bin_groups)]
# axs[3].set_xticklabels(labels, ha="left")
# axs[3].tick_params(axis='x', labelrotation=-45, labelsize='xx-small')

# plt.savefig("test.png")

directory = sys.argv[1]

prod = loadEqn(os.path.join(directory, "prod.json"))
decay = loadEqn(os.path.join(directory, "decay.json"))

bin_names = od()

for proc_group in proc_groups:
  selection = lambda x: (proc_group == x.split("_")[0]) and ("FWDH" not in x)
  bin_names[proc_group] = list(filter(selection, prod.keys()))

proc_groups.append("decay")
bin_names["decay"] = decay.keys()

eqns = {**prod, **decay}

fig, axs = plt.subplots(4, 1, sharex=True, sharey='row', constrained_layout=True)
fig.set_size_inches(30, 15)
#hep.cms.text("Work in progress", ax=axs[0], loc=0)

xtick_loc = []
xtick_labels = []

group_spacing = 4
max_bin_width = max([len(group) for group in param_groups])

vals = od()
for param_group in param_groups:
  for param in param_group:
    vals[param] = getVal(eqns, param)

for l, param_group in enumerate(param_groups):
  ax = axs[l]
  ax.set_ylim(-1, 1)
  ax.set_ylabel(r"$\Delta \mu$")

  x = 0

  for proc_group in proc_groups:
    if l == 0:
      center_x = x + (len(bin_names[proc_group])*max_bin_width) / 2
      ax.text(center_x, 1, proc_group, horizontalalignment="center", verticalalignment="bottom")

    for bin_name in bin_names[proc_group]:      
      xtick_loc.append(x)
      xtick_labels.append(bin_name)
      ax.plot([x, x], [-1, 1], '--', color='0.8', zorder=-1)

      for coeff in param_group:
        val = vals[coeff]
        #ax.bar([x], getDeltaMu(eqns, bin_name, coeff, val), align='edge', label="%s = %.2f"%(coeff, val))
        ax.bar([x], getDeltaMu(eqns, bin_name, coeff, val), align='edge')
        x += 1
      x += max_bin_width - len(param_group)
      ax.set_prop_cycle(None)
    
    #if i != bin_groups-1:
    #  pass
    ax.plot([x, x], [-1, 1], '--', color='0.8', zorder=-1)
    ax.fill_between([x+0.1, x+group_spacing-0.1], -1, 1, color='0.95', zorder=-1)
    x += group_spacing

  legend_text = ""
  for i, coeff in enumerate(param_group):
    val = vals[coeff]
    ax.text(x+1, 0.8-i*0.2, "%s = %.2f"%(coeff, val), color=plt.rcParams['axes.prop_cycle'].by_key()['color'][i], verticalalignment='top', fontsize="xx-small")

axs[3].set_xlim(0, x)
axs[3].set_xticks(xtick_loc[:len(xtick_loc)//len(param_groups)])
axs[3].minorticks_off()
axs[3].set_xticklabels(xtick_labels[:len(xtick_loc)//len(param_groups)], ha="left")
axs[3].tick_params(axis='x', labelrotation=-45, labelsize='xx-small')

plt.savefig("test.pdf")