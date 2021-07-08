from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np


x = [1, 2, 3, 4, 5]
y = [1, 2, 4, 3, 5]
x_pred = [6]

x_input = np.array(x)
y_input = np.array(y)

model = Sequential()
model.add(Dense(1, input_dim=1))

model.compile(loss='mse', optimizer='adam')
model.fit(x_input, y_input, epochs=10000, batch_size=1)

loss = model.evaluate(x_input, y_input)
print('loss: ', loss)
result = model.predict([6])
print('result: ', result)