from sklearn.datasets import load_boston
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
import numpy as np

dataset = load_boston()

x = dataset.data 
y = dataset.target 

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.85, random_state=82)

# reminder! in real life, test data is always not given while training
scaler = MinMaxScaler()
scaler.fit(x_train)
x_train_processed = scaler.transform(x_train)
# test data should be normalized to train-set's scale
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
model.fit(x_train, y_train, batch_size=13, epochs=300, verbose=0, validation_split=0.15)

loss = model.evaluate(x_test, y_test)
predict = model.predict(x_test)
r2 = r2_score(y_test, predict)

print('loss:', loss, 'r2:', r2)

'''
un-scaled
loss: 15.694770812988281 r2: 0.8552390879201758

performance for scaler : slightly lowered r2 value
loss: 24.760156631469727 r2: 0.7716244218183297
loss: 16.58163070678711 r2: 0.8470591407013782
loss: 34.3520622253418 r2: 0.6831533805858843

with larger(320 -> 3200) epochs
loss: 12.336901664733887 r2: 0.886210456873193
 > not much of difference with un-scaled data
'''