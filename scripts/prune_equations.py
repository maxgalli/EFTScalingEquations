import sys
import json
from collections import OrderedDict as od
import os
import math 

def cleanUp(new_json_dict, options):
  for tag in new_json_dict.keys():
    params = new_json_dict[tag].keys()
    params = list(filter(lambda x: x[0] != "u", params))
    for param in params:
      param_value = new_json_dict[tag][param]
      if abs(param_value) < options.abs_threshold:
        del new_json_dict[tag][param]
        del new_json_dict[tag]["u_"+param]
      elif options.round:
        dp = math.ceil(-math.log10(options.abs_threshold)) + 1
        new_json_dict[tag][param] = round(new_json_dict[tag][param], dp)
        new_json_dict[tag]["u_"+param] = round(new_json_dict[tag]["u_"+param], dp)

  return new_json_dict

def getNTerms(prod):
  n = 0
  for tag in prod.keys():
    n += len(prod[tag].keys())/2
  return n

if __name__=="__main__":
  from optparse import OptionParser
  parser = OptionParser(usage="%prog equations/set [options]")
  parser.add_option("--absoluteThreshold", dest="abs_threshold", default=0.0001, type=float)
  parser.add_option("--round", dest="round", default=False, action="store_true")
  (options, args) = parser.parse_args()

  with open(os.path.join(args[0], "prod.json"), "r") as f:
    prod = json.load(f, object_pairs_hook=od)
  with open(os.path.join(args[0], "decay.json"), "r") as f:
    decay = json.load(f, object_pairs_hook=od)
  print("Total number terms before: %d"%(getNTerms(prod)+getNTerms(decay)))
  prod = cleanUp(prod, options)
  decay = cleanUp(decay, options)
  print("Total number terms after: %d"%(getNTerms(prod)+getNTerms(decay)))

  postfix = "_" + str(options.abs_threshold).replace(".", "p")
  new_dir = args[0].strip("/")+postfix
  try: 
    os.mkdir(new_dir)
  except:
    pass

  with open(os.path.join(new_dir, "prod.json"), "w") as f:
    json.dump(prod, f, indent=4)
  with open(os.path.join(new_dir, "decay.json"), "w") as f:
    json.dump(decay, f, indent=4)