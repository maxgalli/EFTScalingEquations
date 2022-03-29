# EFT Scaling Equations

## STXS

Combine:
- [model](https://github.com/jonathon-langford/HiggsAnalysis-CombinedLimit/blob/102x-comb2021-STXStoSMEFT-improved/python/STXStoSMEFTModel.py)


## Differentials

Despite the attempt of using as much as possible what was already implemented for the STXS, a few things are different in the differential so the content of the folders inside ```equations_differentials``` might change a bit in terms of structure.

Each folder in ```equations_differentials``` can be interpreted as a different SMEFT model that can be fitted. The content is as follows:

- ```pois.yml```: file in the format

```
wilson_coeff:
    val:
    max:
    min:
```

which is read by the combine model and describes the Wilson coefficients we want to fit (note that it is adopted from the STXS one, but removes the ```exponential``` key);

- ```cfg.yml```: file in the format

```
decay_channel: path/to/eft2obs-output
```
which is meant to be fed to the script ```scripts_differentials/eft2obs_to_channel``` to generate a ```channels.json``` output; the eft2obs output files are meant to be stored in a ```eft2obs_ouputs``` subfolder

- ```decay.json```: taken from the STXS one, in the we use e.g. ```hgg``` instead of ```gamgam``` for various reasons (mostly because of the way I implemented the model); note that at the moment of writing we have a script ```scripts_differentials/decays_from_paper.py``` which dumps a version of the parametrized BRs based on calculations performed in [this paper](https://arxiv.org/pdf/1906.06949.pdf) suggested by Ilaria - it is still under investigation whether and how this can be used instead of simulating

- ```channels.py```: see above; this is supposed to be the counterpart of STXS's ```prod.json``` file; in our case we target only ggH and we deal with gen bins that *should* be aligned across the different analyses, but in practice usually aren't; the two levels of the nested dictionary in the JSON file are thus the decay channel / analysis (e.g. ```hgg```) and the bin range (e.g. ```0p0_5p0```, with this specific format!)


Combine:
- [branch](https://github.com/maxgalli/HiggsAnalysis-CombinedLimit/tree/EFT_model)
- [model](https://github.com/maxgalli/HiggsAnalysis-CombinedLimit/blob/EFT_model/python/DIFFtoSMEFTModel.py)