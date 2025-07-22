import numpy as np

import pandas as pd
import copy


def cross_entropy_err(y : np.ndarray, t : np.ndarray) -> float:
    """
    交差エントロピー誤差を計算する関数
    :param y: 出力層の出力値（確率）
    :param t: 教師データ（正解ラベル）
    :return: 交差エントロピー誤差
    """
    delta = 1e-7

    if  y.ndim == 1:
        y  = y.reshape(1, y.size)
    #     t  = t.reshape(1, t.size)   # これらがないと次元1がきたときresult計算でインデックス指定がおかしくなる
    
    # batch_size = y.shape[0]
    batch_size = 1

    #正解ラベルがone-hot
    result = -np.sum(t * np.log(y + delta)) / batch_size
    #正解ラベルがラベル例えばインデックス

    # result = -np.sum( np.log( y[np.arange(batch_size), t] + delta) ) / batch_size


    return result

# array = np.array([0.1, 0.2, 0.3])
# print(array.shape)  # (3, 3)
# label = np.array([0, 1, 0])


# print(cross_entropy_err(array, label))


# array = np.arange(9).reshape(3, 3)
# print(array)  # (10, 10)

# print(array.sum())
# print(array.sum(axis = 0, keepdims=True))
# print(array.sum(axis = 1, keepdims=True))
# print(np.tile(array, 2))  # (20, 10)　#行方向（縦）に2回、（列方向（横）に1回）繰り返す
# print(np.tile(array, (1, 2)))  # (20, 10) #行方向（縦）に1回、列方向（横）に2回繰り返す
# print("\n\n\n\n")
# print(np.tile(array, (3, 4, 2)))  #奥に３回、行方向に4回、列方向に2回繰り返す
# print(np.tile(array, (3, 4, 2)).shape)  
# # 320e2 は32000
# print(320e2)
# print(3.1e-2)# e-nは10の-n乗
# print(array.size)




def numerical_gradient(f, x):
    h = 1 # 0.0001
    grad = np.zeros_like(x)
    
    it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite'])
    while not it.finished:
        idx = it.multi_index
        tmp_val = x[idx]
        x[idx] = tmp_val + h
        fxh1 = f(x) # f(x+h)
        
        grad[idx] = fxh1
        
        x[idx] = tmp_val # 値を元に戻す
        it.iternext()   
        
    return grad




def f(x) :
    return np.sum(x)


x = np.array([[1, 2], [3, 4]])
print(numerical_gradient(f, x) )