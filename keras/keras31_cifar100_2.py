import time
from tensorflow.keras.datasets import cifar100
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPool2D
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler


# 1. data-set
(x_train, y_train), (x_test, y_test) = cifar100.load_data() 
# x: (50000, 32, 32, 3) (10000, 32, 32, 3)
# y: (50000, 1) (10000, 1)

x_train = x_train.reshape(50000, 32 * 32 * 3)
x_test = x_test.reshape(10000, 32 * 32 * 3)

scaler = MinMaxScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

x_train = x_train.reshape(50000, 32, 32, 3)
x_test = x_test.reshape(10000, 32, 32, 3)

enc = OneHotEncoder()
y_train = y_train.reshape(-1,1)
y_test = y_test.reshape(-1,1)
y_train = enc.fit_transform(y_train).toarray()
y_test = enc.transform(y_test).toarray()

# 2. modeling

model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(2, 2), padding='same', activation='relu', input_shape=(32, 32, 3))) 
model.add(Conv2D(32, (2, 2), padding='same', activation='relu'))                   
model.add(MaxPool2D())                                         
model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))                   
model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))    
model.add(MaxPool2D())                                         
model.add(Conv2D(128, (4, 4), activation='relu'))                   
model.add(Conv2D(256, (4, 4), activation='relu'))
model.add(MaxPool2D())                                         
model.add(Flatten())                                              
model.add(Dense(1024, activation='relu'))
model.add(Dense(512, activation='relu'))
model.add(Dense(256, activation='relu'))
model.add(Dense(100, activation='softmax'))

# 3. comple fit // metrics 'acc'
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])

es = EarlyStopping(monitor='val_acc', patience=16, mode='max', verbose=2)

start = time.time()
hist = model.fit(x_train, y_train, epochs=100, batch_size=64, verbose=2, validation_split=0.15, callbacks=[es])
end = time.time() - start

# 4. evaluation

loss = model.evaluate(x_test, y_test)
print('it took', end/60, 'minutes and', end%60,'seconds')
print('entropy:', loss[0],'accuracy:', loss[1])

'''
epochs=100, batch_size=64, without ES
it took 21 minutes and 19 seconds
entropy: 8.375273704528809 accuracy: 0.011610584333539009
epochs=27, batch_size=64, stopped early
it took 2 minutes and 48 seconds
entropy: 4.211299896240234 accuracy: 0.32280001044273376
'''