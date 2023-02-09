# KNN Imputation
# Author: Jameel Kaba

import pandas as pd
import numpy as np
from fancyimpute import KNN

# Load file
draft_data = pd.read_csv(r"file_directory.csv")

# Fill missing values in Age feature with each class’s median value of Age 
draft_data['draft_age'].fillna(draft_data.groupby('class')['draft_age'].transform("median"), inplace=True)

# impute removes column names.
draft_data_float = draft_data.select_dtypes(include=[np.float])

# Use k nearest rows which have a feature to fill in each row's missing features
draft_data = pd.DataFrame(KNN(k=7).fit_transform(draft_data_float))
draft_data.to_csv('dumpfile.csv')