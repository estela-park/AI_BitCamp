import time
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN
from tensorflow.keras.callbacks import EarlyStopping

# Data setting
x = np.array([[1,2,3],[2,3,4],[3,4,5],[4,5,6],[5,6,7],[6,7,8],[7,8,9],[8,9,10],[9,10,11],[10,11,12],[20,30,40],[30,40,50],[40,50,60]])
y = np.array([4,5,6,7,8,9,10,11,12,13,50,60,70])
x_test = np.array([[[50],[60],[70]]])

x = x.reshape(13, 3, 1)

# Modeling
model = Sequential()
model.add(SimpleRNN(units=32, input_shape=(3, 1), activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1))

model.summary()

'''
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
simple_rnn (SimpleRNN)       (None, 32)                1088
_________________________________________________________________
dense (Dense)                (None, 32)                1056
_________________________________________________________________
dense_1 (Dense)              (None, 16)                528
_________________________________________________________________
dense_2 (Dense)              (None, 16)                272
_________________________________________________________________
dense_3 (Dense)              (None, 8)                 136
_________________________________________________________________
dense_4 (Dense)              (None, 1)                 9
=================================================================
'''

# Compilation & Training
start = time.time()
es = EarlyStopping(monitor='val_loss', mode='min', patience=24, verbose=2)
model.compile(loss='mse', optimizer='adam')
model.fit(x, y, epochs=1000, batch_size=3, validation_split = 0.15, callbacks=[es])
end = time.time() - start

# Prediction
result = model.predict(x_test)
print(f'prediction for [50 60 70]: {result}')
print(end)

'''
-epochs=100, without ES
prediction for [50 60 70]: [[72.59906]]
-with actF='relu' for SimpleRNN layer, with ES
prediction for [50 60 70]: [[80.65686]] * stopped at 160
** first RNN layer amplifies unnecessary signal without relu in position **
'''