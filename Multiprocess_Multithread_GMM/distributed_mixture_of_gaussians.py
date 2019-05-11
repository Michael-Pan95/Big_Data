import matplotlib.pyplot as plt
import numpy as np
import celery
import json
import pandas as pd
from copy import deepcopy
from sklearn.datasets import make_blobs

address='Michael-Jobs-bb79db6ae538412a.elb.us-east-2.amazonaws.com'
app = celery.Celery('GMM',broker='amqp://myguest:myguestpwd@'+address,backend='amqp://myguest:myguestpwd@'+address)

@app.task
def gmm_dispatcher(task, **kwargs):
    json_dump = kwargs['json_dump']
    json_load = json.loads(json_dump)
    if task == "expectation":
        data = np.array(json_load['data'])
        cov_M = np.array(json_load['cov_M'])
        p_cluster = np.array(json_load['p_cluster'])
        mean = np.array(json_load['mean'])
        result = expectation(data=data, mean=mean, cov_M=cov_M, p_cluster=p_cluster)
        return result
    elif task == "maximization":
        data = np.array(json_load['data'])
        mean = np.array(json_load['mean'])
        w_matrix = np.array(json_load['w_matrix'])
        r_matrix = np.array(json_load['r_matrix'])
        n_cluster = json_load['n_cluster']
        n_feature = json_load['n_feature']
        result = maximization(data=data, mean=mean, r_matrix=r_matrix, w_matrix=w_matrix, n_cluster=n_cluster,
                              n_feature=n_feature)
        return result
    else:
        raise ValueError("Unknow Task Name")




class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.int64):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


def gaussian_pdf(x, mean, cov_M):
    return np.power(2 * np.pi, -1 * cov_M.shape[0] / 2) * np.power(np.linalg.det(cov_M), -0.5) * np.exp(
        -0.5 * np.dot(np.dot(np.transpose(x - mean), np.linalg.inv(cov_M)), x - mean))


def expectation(data, mean, cov_M, p_cluster):
    # expectation
    gaussian_value = []
    for d in data:
        tmp = []
        for index in range(mean.shape[0]):
            tmp.append(gaussian_pdf(d, mean[index], cov_M[index]))
        gaussian_value.append(tmp)
    gaussian_value = np.array(gaussian_value)
    gaussian_value_prior = p_cluster * gaussian_value
    r_matrix = gaussian_value_prior / gaussian_value_prior.sum(axis=1)[:, np.newaxis]
    tmp_w = r_matrix.sum(axis=0)[np.newaxis, :]

    return json.dumps({'data': deepcopy(data), 'r_matrix': deepcopy(r_matrix), 'tmp_w': deepcopy(tmp_w)},
                      cls=NumpyEncoder)


def maximization(data, mean, r_matrix, w_matrix, n_cluster, n_feature):
    # Maximization
    cov_M = []
    for index in range(n_cluster):
        cov_M.append(np.dot(w_matrix[np.newaxis, :, index] * (data - mean[index]).T,
                            data - mean[index]) + np.finfo(np.float64).eps * np.identity(n_feature))
    cov_M = np.array(cov_M)
    p_cluster = r_matrix.mean(axis=0)[np.newaxis, :]

    return json.dumps({'tmp_cov_M': deepcopy(cov_M), 'tmp_p_cluster': deepcopy(p_cluster)}, cls=NumpyEncoder)


