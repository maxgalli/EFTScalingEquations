# CMS-ForDiff-230530-FullDecay# CMS-ForDiff-230530

In general, the folders starting with ```CMS-ForDiff-230530*``` contain the
parametrizations for differential cross sections. 
For production details refer
to [this gist](https://gist.github.com/maxgalli/7407c634d7d5fa2ab5043ee0e434ba7c).
Differences mostly come from production and decay. 

## Production

In each decay channel, the equations inside JSON files called
```FullProduction_*``` are produced by merging the ones from all the different
production modes. The important aspect is that the ones for gluon fusion are
produced with SMEFT@NLO, which does not contain ```chgtil```.

## Decay

The ```gamgam``` part of the decay is derivedwith the standalone reweight and contains ```chbtil```, ```chwtil``` and ```chwbtil```.
