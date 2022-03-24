## Preliminary CMS equations produced by Matthew Knight (matthew.knight@cern.ch)

### Model details

|                        |                     |
|------------------------|---------------------|
| Model                  | SMEFT               |
| Flavour Symmetry       | topU3l: $U(2)^2$    |
| Input Parameter Scheme | $\{m_W, m_Z, G_F\}$ |

### Wilson Coefficients

Mix of different sets.

- For the production modes derived using SMEFTsim we consider all CP-even operators.

- For ggH SMEFTatNLO, we consider chg, ctg, cuh, chbox, chdd, cll1, chl3.
- For ggZH SMEFTatNLO, we consider all that contribute: chl3, chbox, cll1, chd, chdd, chq1, cht, chu, ctg, cth, chwb, chl1, che, chbw, cbb, chj1, chj3, chq3, chu, chbq.

- For the decay modes, we consider all CP-even operators.

### Derivation details

| Process           | Equation derivation method                     |
|-------------------|------------------------------------------------|
| ggH               | SMEFTatNLO                                     |
| qqH               | SMEFTsim                                       |
| WH_lep            | SMEFTsim                                       |
| ZH_lep            | SMEFTsim                                       |
| ggZH              | SMEFTatNLO                                     |
| ttH               | SMEFTsim                                       |
| tH                | SMEFTsim                                       |
|                   |                                                |
| H->gamgam         | [Analytic loop-level](https://arxiv.org/abs/1807.11504)   |
| H->Zgam           | [Analytic loop-level](https://arxiv.org/abs/1801.01136)   |
| All other decay modes   | SMEFTsim


### Notes on acceptance
H->4l has an acceptance corrected scaling equation derived with the eventID skimming + Standalone reweighting method. Propagator corrections included.

### Additional notes