# saving model, params with pickle is supported by python

import time
import pickle
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score
from xgboost import XGBRegressor


# 1. Data-prep
datasets = load_boston()
x = datasets['data']
y = datasets['target']

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.85, random_state=78)

scaler_mm = MinMaxScaler()
x_train_mm = scaler_mm.fit_transform(x_train)
x_test_mm = scaler_mm.transform(x_test)

# 2. Modelling
model = XGBRegressor(n_estimators=240, learning_rate=0.01, n_jobs=1)


# Training & Evaluation
start = time.time()
model.fit(x_train_mm, y_train, verbose=1, eval_metric='rmse', eval_set=[(x_test_mm, y_test)], early_stopping_rounds=8)
end = time.time() - start

score = model.score(x_test_mm, y_test)
predict = model.predict(x_test_mm)
r2 = r2_score(y_test, predict)
print('it took', end//60, 'minutes and', end%60,'seconds')
print('model.score:', score, '& model.R2score:', r2)

pickle.dump(model, open('../_save/_XGB/m21_pickle.dat', 'wb'))