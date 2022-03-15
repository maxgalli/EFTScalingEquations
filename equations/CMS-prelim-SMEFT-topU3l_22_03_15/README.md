## Preliminary CMS equations produced by Matthew Knight (matthew.knight@cern.ch)

### Model details

|                        |                     |
|------------------------|---------------------|
| Model                  | SMEFT               |
| Flavour Symmetry       | topU3l: $U(2)^2$    |
| Input Parameter Scheme | $\{m_W, m_Z, G_F\}$ |

### Wilson Coefficients

Mix of different sets.

- For the production modes derived using SMEFTsim we use the recommendation from Ilaria Brivio's [talk](https://indico.cern.ch/event/1030068/contributions/4408848/) at Higgs 2021. 

chbox
chdd
chg
chw
chb
chwb
cuhre
cthre
cdhre
cbhre
ctgre
ctwre
ctbre
chj1
chq1
chj3
chq3
chu
cht
chd
chbq
chtbre
cehre
chl1
chl3
che
cll1

- For ggH SMEFTatNLO, we consider chg, ctg, cuh, chbox, chdd, cll1, chl3.
- For ggZH SMEFTatNLO, we consider all that contribute: chl3, chbox, cll1, chd, chdd, chq1, cht, chu, ctg, cth, chwb, chl1, che, chbw, cbb, chj1, chj3, chq3, chu, chbq.

- For the decay modes, all contributions operators are included.



### Derivation details

| Process           | Equation derivation method                     |
|-------------------|------------------------------------------------|
| ggH               | SMEFTsim                                       |
| qqH               | SMEFTsim                                       |
| WH_lep            | SMEFTsim                                       |
| ZH_lep            | SMEFTsim                                       |
| ggZH              | Use ZH_lep equations                           |
| ttH               | SMEFTsim                                       |
| tH                | SMEFTsim                                       |
|                   |                                                |
| All decay modes   | SMEFTsim


### Notes on acceptance
No acceptance corrections