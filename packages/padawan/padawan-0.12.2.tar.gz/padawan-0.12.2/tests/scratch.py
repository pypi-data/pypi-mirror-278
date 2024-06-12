import polars as pl
import padawan
import numpy as np

np.random.seed(0)
df = pl.DataFrame({'ix': np.random.randint(1, 5, 10), 'val': range(10)})
df = padawan.from_polars(df, index_columns=('ix',))
df= df.repartition(2)
df = df.repartition(1, sample_fraction=0.1)
df = df.collect()
