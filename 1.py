import numpy as np

# 生成随机整数数组
a = np.random.randint(1, 101, size=100)

# 将一维数组变形为二维数组
b = a.reshape(20, 5)

# 输出二维数组的最大值和最小值
c = b.max()
d = b.min()
print("二维数组的最大值:", c)
print("二维数组的最小值:", d)

# 沿纵轴求每列的最小值
e = b.min(axis=0)
print("每列的最小值:", e)

# 沿横轴求每行的最大值
f = b.max(axis=1)
print("每行的最大值:", f)

# 计算二维数组的中位数、算术平均值、加权平均值和方差
g = np.median(b)
h = np.mean(b)
i = np.average(b)
j = np.var(b)
print("二维数组的中位数:", g)
print("二维数组的算术平均值:", h)
print("二维数组的加权平均值:", i)
print("二维数组的方差:", j)
