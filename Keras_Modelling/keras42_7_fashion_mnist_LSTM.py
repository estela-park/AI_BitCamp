import time
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, LSTM, Input, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

# 1. data-set

(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

x_train = x_train.reshape(60000, 28 * 28 * 1)
x_test = x_test.reshape(10000, 28 * 28 * 1)

scaler = MinMaxScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

x_train = x_train.reshape(60000, 28, 28)
x_test = x_test.reshape(10000, 28, 28)

enc = OneHotEncoder()
y_train = y_train.reshape(-1,1)
y_test = y_test.reshape(-1,1)
y_train = enc.fit_transform(y_train).toarray()
y_test = enc.transform(y_test).toarray()

# 2. modeling

input_l = Input(shape=(28, 28))
hl = LSTM(32, activation='relu')(input_l)
hl = Dropout(0.2)(hl)
hl = Dense(64, activation='relu')(hl)                        
hl = Dense(32, activation='relu')(hl)
hl = Dropout(0.2)(hl)
hl = Flatten()(hl)
output_1 = Dense(10, activation='softmax')(hl) # KerasTensor (None, 10)


# 3. compilation & training
model = Model(inputs=[input_l], outputs=[output_1])
es = EarlyStopping(monitor='val_loss', mode='min', patience=8, verbose=2, restore_best_weights=True)

start = time.time()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
hist = model.fit(x_train, y_train, epochs=100, batch_size=32, verbose=2, validation_split=0.15, callbacks=[es]) 
end = time.time() - start


# 4. evaluation
loss = model.evaluate(x_test, y_test)
print('it took', end/60, 'minutes and', end%60,'seconds')
print('entropy:', loss)


'''
DNN w/o GAP 
    entropy: 1.6580204963684082 accuracy: 0.5427852272987366
DNN w/h GAP
    entropy: 1.115235447883606 accuracy: 0.7957000136375427
CNN  
    entropy: 0.6042917966842651 accuracy: 0.9204000234603882
* LSTM w/o GAP took 40 mins
    entropy: 0.35297292470932007 accuracy: 0.8691999912261963
'''