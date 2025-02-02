import numpy as np

#%% array
a = np.array([2, 3, 4])
b = np.array([(1.5, 2, 3), (4, 5, 6)])
c = np.array([[1, 2], [3, 4]], dtype=complex)

np.zeros((3, 4)) # all zero
np.ones((2, 3, 4), dtype=np.int16) # all 1
np.empty((2, 3)) # garbage values
#%% random
np.random.seed(19680801) # 처음 랜덤값과 동일한 값을 사용하고 싶으면 고정 seed를 사용
r = np.random.randn(4, 100) # row, column count
r = np.random.randint(4, 100, 50) # row, column count, maximum int
ry = np.random.normal(loc=1.5, scale=0.4, size=1000) # loc에서 scale만큼의 표준편차를 가지는 랜덤
#%% linespace
# create 100 values array from 0 to 2
x = np.linspace(0, 2, 100)

#%% matrix
np.matrix([[1, 2], [3, 4]])

#%% array range
# 0 <= x < 5까지의 범위에서 0.2의 간격으로 array생성
t = np.arange(0., 5., 0.2)
t2 = np.arange(50) # 0~ 49


#%% from function
def f(x, y):
    return 10 * x + y
np.fromfunction(f, (5, 4), dtype=int)