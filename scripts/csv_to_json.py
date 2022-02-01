import pandas as pd
import json
import sys
from collections import OrderedDict as od

eqns_df = pd.read_csv(sys.argv[1])
eqns_df.set_index("channel", inplace=True)
eqns_df.drop("width", axis=1, inplace=True)

eqns_dict = od()
for channel in eqns_df.index:
  channel_eqn = od()
  for param in eqns_df.columns:
    A = eqns_df.loc[channel, param]
    if A != 0:
      channel_eqn["A_"+param] = A
      channel_eqn["u_A_"+param] = 0.0005 #error from 3d.p
  eqns_dict[channel] = channel_eqn

with open(sys.argv[2], "w") as f:
  json.dump(eqns_dict, f, indent=4)