import numpy
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt

'''
numpy.array.method 모르는 자의 뻘 짓
    x1 = list(range(1, 11))
    x2 = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.5, 1.4, 1.3]
    temp = []
    for i in range(10):
        temp.append([x1[i], x2[i]])
    x_input = numpy.array(temp)
'''
x = [list(range(1, 11)), [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.5, 1.4, 1.3]]
x_col1 = numpy.array(x[0]).transpose()
x_col2 = numpy.array(x[1]).transpose()
x_input = numpy.array(x).transpose()
y = numpy.array(range(11, 21))
x_predict = numpy.array([x[0][7: 10], x[1][7: 10]]).transpose()

print(x_input)
print(y)

model = Sequential()
# 5x3x4 layers works better than 4x4x4 accuracy-wise
model.add(Dense(4, input_dim=2))
model.add(Dense(5))
model.add(Dense(3))
model.add(Dense(1))

model.compile(loss='mse', optimizer='adam')
'''
[Accuracy for batch size]
    1 >> 2 >> 5
'''
model.fit(x_input, y, epochs=2000, batch_size=1)

loss = model.evaluate(x_input, y)
result = model.predict(x_predict)
y_predict = model.predict(x_input)

model_col1 = Sequential()
model_col1.add(Dense(4, input_dim=1))
model_col1.add(Dense(5))
model_col1.add(Dense(3))
model_col1.add(Dense(1))

model_col1.compile(loss='mse', optimizer='adam')
model_col1.fit(x_col1, y, epochs=2000, batch_size=1)

loss = model_col1.evaluate(x_col1, y)
y_predict_col1 = model_col1.predict(x_col1)

model_col2 = Sequential()
model_col2.add(Dense(4, input_dim=1))
model_col2.add(Dense(5))
model_col2.add(Dense(3))
model_col2.add(Dense(1))

model_col2.compile(loss='mse', optimizer='adam')
model_col2.fit(x_col2, y, epochs=2000, batch_size=1)

loss = model_col2.evaluate(x_col2, y)
y_predict_col2 = model_col2.predict(x_col2)

print('loss: ',loss,', result for [[ 8. , 1.5], [ 9. , 1.4], [10. , 1.3]]: ', result)

# loss:  3.897296483046375e-05, 
# result for [[ 8. , 1.5]                     [[17.994087]
#             [ 9. , 1.4]         is           [18.989716]
#             [10. , 1.3]]                     [19.98534 ]]


plt.scatter(x_col1, y, color='blue')
plt.scatter(x_col2, y, color='red')
plt.plot(x_col1, y_predict_col1, color='blue')
plt.plot(x_col2, y_predict_col2, color='red')
plt.show()

'''
<Numbering the dimension for Matrix: not the shape of the table>
[[1], [2], [3]]  -> [1]    -> 3x1 
                    [2]
                    [3]
[1, 2, 3]        -> 1      -> 3x
                    2
                    3
[[1, 2, 3]]      -> 1 3 3  -> 1x3
[[1, 2], [3, 4], [5, 6]]   -> 3x2
[[[1, 2], [3, 4], [5, 6]]] -> 1x1x3x2
[[[1], [2]], [[3], [4]]]   -> 2x2x1
'''
'''
[x1, x2]: [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.5, 1.4, 1.3]]
order=Read the elements of a using this index order, and place the elements into the reshaped array using this index order. 
      ‘C’ means to read / write the elements using C-like index order, with the last axis index changing fastest, back to the first axis index changing slowest. 
      ‘F’ means to read / write the elements using Fortran-like index order, with the first index changing fastest, and the last index changing slowest. 
          * Note that the ‘C’ and ‘F’ options take no account of the memory layout of the underlying array, and only refer to the order of indexing. 
      ‘A’ means to read / write the elements in Fortran-like index order if a is Fortran contiguous in memory, C-like order otherwise
x_reshaped = numpy.reshape([x1, x2], (10, 2), order='C'): [[ 1.   2. ]
                                                           [ 3.   4. ]
                                                           [ 5.   6. ]
                                                           [ 7.   8. ]
                                                           [ 9.  10. ]
                                                           [ 1.   1.1]
                                                           [ 1.2  1.3]
                                                           [ 1.4  1.5]
                                                           [ 1.6  1.5]
                                                           [ 1.4  1.3]]

x_reshaped = numpy.reshape([x1, x2], (10, 2), order='F'): [[ 1.   6. ]
                                                           [ 1.   1.5]
                                                           [ 2.   7. ]
                                                           [ 1.1  1.6]
                                                           [ 3.   8. ]
                                                           [ 1.2  1.5]
                                                           [ 4.   9. ]
                                                           [ 1.3  1.4]
                                                           [ 5.  10. ]
                                                           [ 1.4  1.3]]

x_reshaped = numpy.reshape([x1, x2], (10, 2), order='A'): [[ 1.   2. ]
                                                           [ 3.   4. ]
                                                           [ 5.   6. ]
                                                           [ 7.   8. ]
                                                           [ 9.  10. ]
                                                           [ 1.   1.1]
                                                           [ 1.2  1.3]
                                                           [ 1.4  1.5]
                                                           [ 1.6  1.5]
                                                           [ 1.4  1.3]]
'''
'''
pd.DataFrame([[1, 2],[3, 4],[6, 7]], index=['a', 'b', 'c'], columns=['A', 'B'])
   A  B
a  1  2
b  3  4
c  6  7
pd.DataFrame([[1, 2, 3], [4, 5, 6]], index=['a', 'b'], columns=['A', 'B', 'C'])
   A  B  C
a  1  2  3
b  4  5  6
'''