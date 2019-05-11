import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def data_gen(m, n):
    points = np.linspace(-1, 1, m)
    tiled_points = np.tile(points, [m, 1])
    data_1 = np.stack([tiled_points.T, tiled_points], axis=-1).reshape([n, -1])
    return data_1


def euclidian_distance_calculator(selected_point_index, data_2d):
    side_square, dimension = data_2d.shape
    side = int(np.sqrt(side_square))
    target_value = np.array([data_2d[:, i][selected_point_index] for i in range(dimension)])
    distance = np.power(data_2d - target_value, 2)
    distance_list = []
    for data_point in distance:
        distance_list.append(np.sqrt(np.sum(data_point)))
    distance_list = np.array(distance_list).reshape((side, side))
    return distance_list
    pass


def increase_dim(ori_data, new_dim):
    data_size, ori_dim = ori_data.shape
    assert (ori_dim <= new_dim)
    result = np.zeros((data_size, new_dim))
    result[:, :ori_dim] = ori_data
    # use orthogonal matrix to support dimension increase
    B = stats.ortho_group.rvs(d)
    result = np.dot(result, B)
    return result


def gen_random_proj_matrix(k, d, method):
    assert (method in ['Gaussian', 'Discrete'])
    transform_M = None
    if method == 'Gaussian':
        transform_M = np.random.normal(size=(k, d), loc=0, scale=1)
    elif method == 'Discrete':
        transform_M = np.random.randint(low=0, high=2, size=(k, d))
    return transform_M


if __name__ == "__main__":
    np.random.seed(10601)
    m = 10
    n = m * m
    d = 100
    data_2d = data_gen(m, n)
    # random selection of a point
    selected_index = np.random.randint(low=0, high=m * m - 1)
    distance_map = euclidian_distance_calculator(selected_index, data_2d)
    fig = plt.figure(figsize=(m, m))
    im = plt.imshow(distance_map, cmap='gist_heat')
    cb = fig.colorbar(im)
    plt.title('Heatmap', fontsize=50)
    plt.savefig('heatmap.jpg')
    # plt.show()

    # increase data dim
    k_list = [2, 10, 50]
    A_list = ['Gaussian', 'Discrete']

    distance_map[selected_index // m, selected_index % m] = 1  # avoid i=j / divided by 0

    # map real value
    incre_dim_data = increase_dim(data_2d, d)
    for k in k_list:
        for method in A_list:
            plt.clf()
            fig = plt.figure(figsize=(2 * m, m))
            transform_M = gen_random_proj_matrix(k, d, method)
            transformed_D = np.dot(incre_dim_data, transform_M.T) / np.sqrt(k)  # f(x) = Ax/k^0.5
            # for ever i != j, we calculate |f(x_i) - f(x_j)| / |f(x_i) - f(x_j)|
            distance_map_transform = euclidian_distance_calculator(selected_index, transformed_D)
            plt.subplot(121)
            im_tmp = plt.imshow(distance_map_transform, cmap='gist_heat')
            plt.colorbar(im_tmp)
            r_i_j = (distance_map_transform / distance_map).reshape(-1)
            r_i_j = np.array([a for i, a in enumerate(r_i_j) if i != selected_index])
            mean_rij = np.mean(np.power(r_i_j - 1, 2))
            plt.subplot(122)
            plt.hist(r_i_j)
            fig.suptitle(
                'Distance HeatMap & Histogram for K={}, Transform Type: {}, Mean (rij-1)^2 = {}'.format(k, method,
                                                                                                        round(mean_rij,
                                                                                                              2)),
                fontsize=30)
            plt.savefig('K={}_Transform_Type_{}.jpg'.format(k, method))

    distance_map[selected_index // m, selected_index % m] = 0

    # map one hot
    plt.clf()
    one_hot_data = np.identity(n)
    distance_map_oh = euclidian_distance_calculator(selected_index, one_hot_data)

    distance_map_oh[selected_index // m, selected_index % m] = 1
    im = plt.imshow(distance_map_oh, cmap='gist_heat')
    plt.colorbar(im)
    plt.title('One-hot heatmap', fontsize=30)
    plt.savefig('OHheatmap.jpg')
    for k in k_list:
        for method in A_list:
            plt.clf()
            fig = plt.figure(figsize=(2 * m, m))
            transform_M = gen_random_proj_matrix(k, d, method)
            transformed_D = np.dot(one_hot_data, transform_M.T) / np.sqrt(k)  # f(x) = Ax/k^0.5
            # for ever i != j, we calculate |f(x_i) - f(x_j)| / |f(x_i) - f(x_j)|
            distance_map_transform = euclidian_distance_calculator(selected_index, transformed_D)
            r_i_j = (distance_map_transform / distance_map_oh).reshape(-1)
            r_i_j = np.array([a for i, a in enumerate(r_i_j) if i != selected_index])
            mean_rij = np.mean(np.power(r_i_j - 1, 2))
            plt.hist(r_i_j)
            fig.suptitle(
                'Distance HeatMap & Histogram for K={}, Transform Type: {}, Mean (rij-1)^2 = {}'.format(k, method,
                                                                                                        round(mean_rij,
                                                                                                              2)),
                fontsize=30)
            plt.savefig('OH_K={}_Transform_Type_{}_Ratio_only.jpg'.format(k, method))

    distance_map_oh[selected_index // m, selected_index % m] = 0

    # map one hot
    plt.clf()
    one_hot_data = np.identity(n)
    distance_map_oh = euclidian_distance_calculator(selected_index, one_hot_data)

    distance_map_oh[selected_index // m, selected_index % m] = 1
    im = plt.imshow(distance_map_oh, cmap='gist_heat')
    plt.colorbar(im)
    plt.title('One-hot heatmap', fontsize=30)
    plt.savefig('OHheatmap.jpg')
    for k in k_list:
        for method in A_list:
            plt.clf()
            fig = plt.figure(figsize=(2 * m, m))
            transform_M = gen_random_proj_matrix(k, d, method)
            transformed_D = np.dot(one_hot_data, transform_M.T) / np.sqrt(k)  # f(x) = Ax/k^0.5
            # for ever i != j, we calculate |f(x_i) - f(x_j)| / |f(x_i) - f(x_j)|
            distance_map_transform = euclidian_distance_calculator(selected_index, transformed_D)
            plt.subplot(121)
            im_tmp = plt.imshow(distance_map_transform, cmap='gist_heat')
            plt.colorbar(im_tmp)
            r_i_j = (distance_map_transform / distance_map_oh).reshape(-1)
            r_i_j = np.array([a for i, a in enumerate(r_i_j) if i != selected_index])
            mean_rij = np.mean(np.power(r_i_j - 1, 2))
            plt.subplot(122)
            plt.hist(r_i_j)
            fig.suptitle(
                'Distance HeatMap & Histogram for K={}, Transform Type: {}, Mean (rij-1)^2 = {}'.format(k, method,
                                                                                                        round(mean_rij,
                                                                                                              2)),
                fontsize=30)
            plt.savefig('OH_K={}_Transform_Type_{}.jpg'.format(k, method))

    distance_map_oh[selected_index // m, selected_index % m] = 0
