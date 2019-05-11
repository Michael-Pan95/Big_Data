import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle


def data_Generator(n=100):
    label_0_p, label_1_p = int(n * 0.5), int(0.5 * n)
    label_0 = np.zeros((label_0_p, 1))
    label_1 = np.zeros((label_1_p, 1)) + 1

    co_var = [[0.2 ** 2, 0], [0, 0.2 ** 2]]

    data_0_part1 = np.random.multivariate_normal([-1, 0], co_var, (label_0_p // 2))
    data_0_part2 = np.random.multivariate_normal([1, 0], co_var, (label_0_p // 2))
    data_0 = np.concatenate((data_0_part1, data_0_part2), axis=0)

    data_1 = np.random.multivariate_normal([0, 0], co_var, label_1_p)

    data = np.concatenate((data_0, data_1), axis=0)
    label = np.concatenate((label_0, label_1), axis=0)

    return data, label.ravel()


def random_Fourier_feature(data, m, std=0.1):
    phi_x = []
    n, dim = data.shape
    w = np.random.randn(dim, m) / std
    b = np.random.uniform(low=0, high=2 * np.pi, size=m)
    for d in data:
        # w = np.random.normal(0, 1 / 0.1, 2)
        phi_x.append(np.cos(np.dot(d, w) + b))
    phi_x = np.array(phi_x)
    phi_x *= np.sqrt(2 / m)

    return phi_x


def diff_cal(gram, gram_approx):
    diff = np.abs(gram - gram_approx)
    err_1 = diff.sum() / np.power(gram.shape[0], 2)
    err_max = diff.max()
    return err_1, err_max


def cal_rbf_gram(data, std=0.1):
    x_tmp = np.sum(np.power(data, 2), axis=1, keepdims=1)
    k0 = x_tmp + x_tmp.T - 2 * np.dot(data, data.T)
    gram_rbf = np.exp(-k0 / (2 * std ** 2))
    return gram_rbf


data, label = data_Generator()
print('Data shape, Label shape\n', data.shape, label.shape)

gram_rbf = cal_rbf_gram(data)

m_list = [10, 50, 100, 500, 1000]
err_1_list = []
err_max_list = []
for m in m_list:
    phi_x = random_Fourier_feature(data, m)
    phi_gram = np.dot(phi_x, phi_x.T)
    err_1, err_max = diff_cal(gram_rbf, phi_gram)
    err_1_list.append([m, err_1])
    err_max_list.append([m, err_max])
    print('m:{}\terr_1:{:.3f}\terr_max:{:.3f}'.format(m, err_1, err_max))
err_1_list = np.array(err_1_list)
err_max_list = np.array(err_max_list)

plt.plot(err_1_list[:, 0], err_1_list[:, 1])
plt.xlabel('m')
plt.ylabel('e_1')
plt.suptitle('e_1 vs m')
plt.savefig('./err_1.png')
plt.show()
#
plt.plot(err_max_list[:, 0], err_max_list[:, 1])
plt.suptitle('e_max vs m')
plt.xlabel('m')
plt.ylabel('e_max')
plt.savefig('./err_max.png')
plt.show()

n = data.shape[0]
data, label = shuffle(data, label)
train_x, test_x = data[:n // 2, :], data[n // 2:, :]
train_y, test_y = label[:n // 2], label[n // 2:]

clf = LogisticRegression(solver='lbfgs').fit(train_x, train_y)
print('\nLogistic Regression\n--------------------')
print('Train Acc', clf.score(train_x, train_y))
print('Test Acc', clf.score(test_x, test_y))

data_rbf = cal_rbf_gram(data)
train_rbf_x, test_rbf_x = data_rbf[:n // 2, :], data_rbf[n // 2:, :]
clf_rbf = LogisticRegression(solver='lbfgs').fit(train_rbf_x, train_y)
print('\nLogistic Regression (RBF)\n--------------------')
print('Train Acc', clf_rbf.score(train_rbf_x, train_y))
print('Test Acc', clf_rbf.score(test_rbf_x, test_y))

for m in m_list:
    data_rff = random_Fourier_feature(data, m)
    train_rff_x, test_rff_x = data_rff[:n // 2, :], data_rff[n // 2:, :]

    clf_tmp = LogisticRegression(solver='lbfgs').fit(train_rff_x, train_y)
    print('\nLogistic Regression (RFF) m={}\n--------------------'.format(m))
    print('Train Acc', clf_tmp.score(train_rff_x, train_y))
    print('Test Acc', clf_tmp.score(test_rff_x, test_y))
