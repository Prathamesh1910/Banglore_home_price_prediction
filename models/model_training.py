import pandas as pd
import numpy as np
# from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error
import pickle


# path: Path = Path(__file__).parent.parent

df = pd.read_csv('../data/bhp_data.csv')
df.drop(columns=['Unnamed: 0'], inplace = True)

inputs = df.drop('price_per_sqft', axis = 'columns')
target = df['price_per_sqft']

x_train, x_test, y_train, y_test = train_test_split(inputs.values, target, test_size = 0.2)

model_en = ElasticNet(alpha = 0.0001, l1_ratio = 0.01)
model_en.fit(x_train, y_train)

y_pred1 = model_en.predict(x_train)
y_pred2 = model_en.predict(x_test)

print(f'train score: {model_en.score(x_train, y_train)}')
print(f'test score: {model_en.score(x_test, y_test)}')
print(f'train error: {mean_absolute_error(y_train, y_pred1)}')
print(f'test error: {mean_absolute_error(y_test, y_pred2)}')

# with open('./artifacts/bhp_model_en.pickle', 'wb') as f:
#     pickle.dump(model_en, f)
