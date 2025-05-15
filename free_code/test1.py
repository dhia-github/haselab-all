# import numpy as np

# import pandas as pd

# df = pd.DataFrame([[1,2,3], [4,5,6], [7,8,9]], columns=['A', 'B', 'C'])
# print(df)


# def step(arr):
#     return np.where(arr > 0, 1, 0)


# arr = np.arange(-5, 5, 0.1)  # -5から5まで0.1刻みで配列を作成])

# print(arr)
# print(step(arr))
# #np.arrayy はastype()を使って型変換することができる


# import matplotlib.pyplot as plt

# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# ax.plot(arr, step(arr))#
# ax.set_xlabel('x')
# ax.set_ylabel('y')

# plt.show()


import numpy as np

x = np.arange(6).reshape(2, 3)
print("元の配列:\n", x)

it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite'])
while not it.finished:
    # 現在の要素の値を取得
    element = it[0]
    # 現在の要素の多次元インデックスを取得
    idx = it.multi_index

    print(f"インデックス {idx} の要素: {element}")

    # 例: 要素の値を2倍にする
    it[0] = element * 2

    
    # 次の要素へ進む
    it.iternext()
    print("\n処理後の配列:\n", x)
print("\n処理後の配列:\n", x)