from sklearn.datasets import load_boston
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
import numpy as np

dataset = load_boston()

x = dataset.data 
y = dataset.target 

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.85, random_state=82)

scaler = StandardScaler()
scaler.fit(x_train)
x_train_processed = scaler.transform(x_train)
x_test_processed = scaler.transform(x_test)

input1 = Input(shape=(13, ))
hl = Dense(128, activation='relu')(input1)
hl = Dense(64, activation='relu')(hl)
hl = Dense(64, activation='relu')(hl)
hl = Dense(64, activation='relu')(hl)
hl = Dense(32, activation='relu')(hl)
output1 = Dense(1)(hl)

model = Model(inputs=input1, outputs=output1)

model.compile(loss='mse', optimizer='adam')
model.fit(x_train, y_train, batch_size=13, epochs=300, verbose=2, validation_split=0.15)

loss = model.evaluate(x_test, y_test)
predict = model.predict(x_test)
r2 = r2_score(y_test, predict)

print('loss:', loss, 'r2:', r2)

'''
un-scaled, epochs=300, w/h activation fn, 
loss: 16.838380813598633 r2: 0.8446910074225141

standard-scaler: marginally better accuracy
loss: 13.52721881866455 r2: 0.8752315461584774
loss: 15.420316696166992 r2: 0.8577705383927378
loss: 16.71699333190918 r2: 0.8458106290985014
'''