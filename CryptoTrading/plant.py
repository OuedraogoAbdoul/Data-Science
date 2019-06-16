import pandas as pd
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/plants/plants.data', error_bad_lines=False, encoding = "ISO-8859-1");
print(df.tail())