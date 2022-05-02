## Preliminary CMS equations produced by Matthew Knight (matthew.knight@cern.ch)

### Model details

|                        |                     |
|------------------------|---------------------|
| Model                  | SMEFT               |
| Flavour Symmetry       | topU3l: $U(2)^2$    |
| Input Parameter Scheme | $\{m_W, m_Z, G_F\}$ |

### Wilson Coefficients

We consider the all CP-even and CP-odd operators except in GGH where we neglect contributions from four-fermion operators

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
No acceptance corrections

### Additional notes
Changes with respect to the last [iteration](../CMS-prelim-SMEFT-topU3l_22_03_24) include:
- Inclusion of CP-odd operators
- Correcting mistakes made in the ggZH Wilson coefficient conversion
- Using looser gen-level cuts 
- Validation (and corrections) of the direct integration used in the H->4f channels