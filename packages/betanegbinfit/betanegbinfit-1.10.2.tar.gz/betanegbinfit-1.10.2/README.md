# BetaNegBinFit
## A very brief manual
The cornerstones (or rather, to be more precise, parts that are supposed to be used by a user, rather than a developer) of **BetaNegBinFit** are *model* classes that do model certain distribution and do some heavy lifting. At the moment, there are 2 models available:
* `ModelMixture` -- a model that models counts at a certain slice as a mixture of 2 binomial-alike distributions;
* `ModelLine` -- this can be thought of as a composition of a lot of `ModelMixture`s (their number is equal to a number of slices), but they are linked via constraining *r* parameter to a linear function of slice.

Both models can use either negative-binomial or beta-negative-binomial distribution (see `model` argument of their `__init__` methods).
### Use example: *ModelMixture"

Running `ModelMixture` is as simple as:
```
from betanegbinfit import ModelMixture
m = ModelMixture(bad=2, left=4)
res = m.fit(some_slice)
```

Then, you can inspect parameters through examining the `res` variable which is a fairly self-explanotory `dict`.


#### Some_slice?
Assume that we want to get slice of refs with fix__c = 23 for BAD=3 for our *chipseq*-dataset, `some_slice`. We suggest doing it this way:

```
data_folder = 'Data'
data_file = os.path.join(data_folder, 'chipseq.tsv')

bad = 3
fix_c = 23
dfo = pd.read_csv(data_file, sep='\t')
dfo = dfo[dfo.BAD == bad]
refs = dfo.REF_COUNTS
alts = dfo.ALT_COUNTS
some_slice = refs[alts == c]
```

### Use example: *ModelLine*

`ModelLine` is ran similarly, but this time we pass whole data to the `fit` method instead of a single slice:
```
from betanegbinfit import ModelLine
m = ModelLine(bad=2, left=4)
res = m.fit(data)
```
We advise that data is a n x 2 numpy array rather than pandas DataFrame (where the 1st column stands for reference allele counts and the 2nd for alt counts), however if that is not the case, `ModelLine` will try to guess ref count, alt count and BAD columns from the dataframe.

### Statistics
`stats` module has a number of functions that can be of interest to a prospective user:
1. `rmsea` - calculate RMSEA goodness-of-fit statistic;
2. `calc_pvalues` - calculate p-value for each of snp;
3. `calc_eff_sizes` - calculate "effect sizes" for each of snp;
4. `calc_adjusted_loglik` - calcualte adjusted loglikelihood: adjusted loglikelihood is just a likelihood correct for its parameters geometry. It is done vis subtracting logdet of Fisher information matrix.

#### Automatic everything & multiprocessing

However, instead of manually creating instances of model classes and working through **BetaNegBinFit** methods, it might be much more preferential to run a single to-use function. The package has `utils.run` function that is very easy to use and also does parallelization. See *test.py* for a real (and a very short one) example. Most importantly, it produces tabular data that can be easily analyzed in a downstream analysis.

Also, it has plenty of arguments that can be taked advantage of to do some preprocessing which might be crucial for some datasets.


**Please note, that all functions have plenty of optional arguments and they all are documented, so please consider reading through `help(function of interest)`.**


### A note on performance
As far as we are concerned, **BetaNegBinFit** should work within a manageable amounts of time. For insance, when `ModelLine` with `model='BetaNB'` ran against *chipseq.tsv* dataset, it finishes in 6 minutes when ran at Ryzen 5600U. It does so under 2 minutes with `model='NB'`.
