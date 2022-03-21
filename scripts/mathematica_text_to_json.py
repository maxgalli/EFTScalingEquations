import json
import sys
import re

with open(sys.argv[1], "r") as f:
  txt_eqn = f.read()

txt_eqn = txt_eqn.replace("*10^", "E")

terms = []

start = 0
for i, char in enumerate(txt_eqn):
  if char in ["+", "-"] and txt_eqn[i-1] != "E":
    terms.append(txt_eqn[start:i])
    start = i
terms.append(txt_eqn[start:])
terms = terms[1:] #remove "1." from the beginning

lin = {}
quad = {}
cross = {}

for term in terms:
  num, params = float(term.split(" ")[0]), term.split(" ")[1:]
  if len(params) == 2:
    cross["B_%s_%s"%(params[0], params[1])] = num
  elif "^2" in params[0]:
    quad["B_%s_2"%params[0][:-2]] = num
  else:
    lin["A_%s"%params[0]] = num
  param = "c" + "".join(term.split("c")[1:])

lin = {key:lin[key] for key in sorted(lin)}
quad = {key:quad[key] for key in sorted(quad)}
cross = {key:cross[key] for key in sorted(cross)}
eqn = {**lin, **quad, **cross}

with open(sys.argv[2], "w") as f:
  json.dump({"inclusive":eqn}, f, indent=4)