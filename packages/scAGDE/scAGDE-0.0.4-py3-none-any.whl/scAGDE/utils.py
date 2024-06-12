"""
@Project ：SCALE_Graph
@File    ：utils.py
@IDE     ：PyCharm
@Author  ：Hao Gaoyang
@Date    ：2022/9/28 8:25
@Content ：
"""
from scipy.sparse import issparse
from sklearn.neighbors import kneighbors_graph
from sklearn.decomposition import PCA
from scipy import sparse as sp
from torch.utils.data import Dataset
import scanpy as sc

def prepare_data(datapath,binary=True):
    print("Loading dataset from:%s"%datapath)
    adata = sc.read_h5ad(datapath)
    if not issparse(adata.X):
        adata.X = scipy.sparse.csr_matrix(adata.X)
    if binary:
        adata.X[adata.X>1] = 1
    return adata


def get_A_r_flex(adj, r, cumulative=False):
    # adj_d = adj.to_dense()
    adj_d = adj
    adj_c = adj_d           # A1, A2, A3 .....
    adj_label = adj_d

    for i in range(r-1):
        adj_c = adj_c@adj_d
        adj_label = adj_label + adj_c if cumulative else adj_c
    return adj_label
def degree_power(A, k):
    degrees = np.power(np.array(A.sum(1)), k).flatten()
    degrees[np.isinf(degrees)] = 0.
    if sp.issparse(A):
        D = sp.diags(degrees)
    else:
        D = np.diag(degrees)
    return D
def dopca(X, dim=10):
    if dim <=1:
        dim = float(dim)
    else:
        dim = int(dim)
    pcaten = PCA(n_components=dim)
    X_10 = pcaten.fit_transform(X)
    return X_10
def norm_adj(A):
    normalized_D = degree_power(A, -0.5)
    output = normalized_D.dot(A).dot(normalized_D)
    return output

def random_surf(cosine_sim_matrix, num_hops, alpha):
    num_nodes = len(cosine_sim_matrix)
    adj_matrix = cosine_sim_matrix
    P0 = np.eye(num_nodes, dtype='float32')
    P = np.eye(num_nodes, dtype='float32')
    A = np.zeros((num_nodes, num_nodes), dtype='float32')

    for i in range(num_hops):
        P = (alpha * np.dot(P, adj_matrix)) + ((1 - alpha) * P0)
        A = A + P

    return A

# PPMI Matrix
def PPMI_matrix(A):
    num_nodes = len(A)
    row_sum = np.sum(A, axis=1).reshape(num_nodes, 1)
    col_sum = np.sum(A, axis=0).reshape(1, num_nodes)
    D = np.sum(col_sum)
    PPMI = np.log(np.divide(np.multiply(D, A), np.dot(row_sum, col_sum)))
    PPMI[np.isinf(PPMI)] = 0.0
    PPMI[np.isneginf(PPMI)] = 0.0
    PPMI[PPMI < 0.0] = 0.0

    return PPMI



def get_ppmi(count, k=15, pca=50, mode="connectivity", s=2):
    if pca:
        countp = dopca(count, dim=pca)
    else:
        countp = count
    A = kneighbors_graph(countp, k, mode=mode, metric="euclidean", include_self=True)
    adj = A.A
    node = adj.shape[0]
    A = random_surf(adj, s, 0.98)
    ppmi = PPMI_matrix(A)
    for i in range(node):
        ppmi[i] = ppmi[i]/(np.max(ppmi[i]))
    adj = ppmi
    adj_n = norm_adj(adj)
    return adj,adj_n



def get_adj(count, k=15, pca=50, mode="connectivity",metric="euclidean"):
    if pca:
        countp = dopca(count, dim=pca)
    else:
        countp = count
    A = kneighbors_graph(countp, k, mode=mode, metric=metric, include_self=True)
    adj = A.A
    adj_n = norm_adj(A).A
    return adj, adj_n


class LoadDataset(Dataset):

    def __init__(self, data):
        self.x = data
    def __len__(self):
        return self.x.shape[0]

    def __getitem__(self, idx):
        return torch.from_numpy(np.array(self.x[idx])).float(), \
               torch.from_numpy(np.array(idx))


def getADJ(count,order,cumulative=True, k=15, pca=50, mode="connectivity"):
    if pca:
        countp = dopca(count, dim=pca)
    else:
        countp = count
    A = kneighbors_graph(countp, k, mode=mode, metric="euclidean", include_self=False)
    # 有向图变无向图
    adj = A.toarray()
    adj_n = norm_adj(adj)
    # adj = A + A.T.multiply(A.T > A) - A.multiply(A.T > A)
    # # normalize
    # adj = adj.toarray()
    # adj = adj + sp.eye(adj.shape[0])
    # adj = norm_adj(adj)
    # adj_d = adj.to_dense()
    adj_d = adj_n
    adj_c = adj_d  # A1, A2, A3 .....
    adj_label = adj_d

    for i in range(order - 1):
        adj_c = adj_c @ adj_d
        adj_label = adj_label + adj_c if cumulative else adj_c
    return adj_label


import torch
import random
import numpy as np
from munkres import Munkres
from sklearn import metrics
from sklearn.metrics import adjusted_rand_score as ari_score, silhouette_score, calinski_harabasz_score, \
    davies_bouldin_score
from sklearn.metrics.cluster import normalized_mutual_info_score as nmi_score


def adjust_learning_rate(optimizer, epoch):
    lr = 0.001 * (0.1 ** (epoch // 50))
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


def cluster_acc(y_true, y_pred):
    y_true = y_true - np.min(y_true)

    l1 = list(set(y_true))
    numclass1 = len(l1)

    l2 = list(set(y_pred))
    numclass2 = len(l2)

    ind = 0
    if numclass1 != numclass2:
        for i in l1:
            if i in l2:
                pass
            else:
                y_pred[ind] = i
                ind += 1

    l2 = list(set(y_pred))
    numclass2 = len(l2)

    if numclass1 != numclass2:
        print('error')
        return

    cost = np.zeros((numclass1, numclass2), dtype=int)
    for i, c1 in enumerate(l1):
        mps = [i1 for i1, e1 in enumerate(y_true) if e1 == c1]
        for j, c2 in enumerate(l2):
            mps_d = [i1 for i1 in mps if y_pred[i1] == c2]
            cost[i][j] = len(mps_d)

    m = Munkres()
    cost = cost.__neg__().tolist()
    indexes = m.compute(cost)

    new_predict = np.zeros(len(y_pred))
    for i, c in enumerate(l1):
        c2 = l2[indexes[i][1]]

        ai = [ind for ind, elm in enumerate(y_pred) if elm == c2]
        new_predict[ai] = c

    acc = metrics.accuracy_score(y_true, new_predict)
    f1_macro = metrics.f1_score(y_true, new_predict, average='macro')
    precision_macro = metrics.precision_score(y_true, new_predict, average='macro')
    recall_macro = metrics.recall_score(y_true, new_predict, average='macro')
    f1_micro = metrics.f1_score(y_true, new_predict, average='micro')
    precision_micro = metrics.precision_score(y_true, new_predict, average='micro')
    recall_micro = metrics.recall_score(y_true, new_predict, average='micro')
    return acc, f1_macro


def eva(y_true, y_pred, epoch=0):
    acc, f1 = cluster_acc(y_true, y_pred)
    nmi = nmi_score(y_true, y_pred, average_method='arithmetic')
    ari = ari_score(y_true, y_pred)
    # print('Epoch_{}'.format(epoch), ':acc {:.4f}'.format(acc), ', nmi {:.4f}'.format(nmi), ', ari {:.4f}'.format(ari),
    #       ', f1 {:.4f}'.format(f1))
    print('Epoch_{}'.format(epoch), ':acc {:.4f}'.format(acc), ', ari {:.4f}'.format(ari),  ', nmi {:.4f}'.format(nmi),
          ', f1 {:.4f}'.format(f1))
    return acc, nmi, ari, f1


def parameter(model):
    params = list(model.parameters())
    k = 0
    for i in params:
        l = 1
        for j in i.size():
            l *= j
        k = k + l
    print("sum:" + str(k))
    return str(k)

def target_distribution(q):
    weight = q ** 2 / q.sum(0)
    return (weight.t() / weight.sum(1)).t()
def setup_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


# !/usr/bin/env python
"""
# Author: Xiong Lei
# Created Time : Tue 24 Apr 2018 08:05:21 PM CST

# File Name: utils.py
# Description:

"""

import numpy as np
import pandas as pd
import scipy
import os
import torch
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import f1_score
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, scale
from sklearn.metrics import classification_report, confusion_matrix, adjusted_rand_score, normalized_mutual_info_score


# ============== Data Processing ==============
# =============================================

def read_labels(ref, return_enc=False):
    """
    Read labels and encode to 0, 1 .. k with class names
    """
    # if isinstance(ref, str):
    ref = pd.read_csv(ref, sep='\t', index_col=0, header=None)

    encode = LabelEncoder()
    ref = encode.fit_transform(ref.values.squeeze())
    classes = encode.classes_
    if return_enc:
        return ref, classes, encode
    else:
        return ref, classes


def gene_filter_(data, X=6):
    """
    Gene filter in SC3:
        Removes genes/transcripts that are either (1) or (2)
        (1). rare genes/transcripts:
            Expressed (expression value > 2) in less than X% of cells
        (2). ubiquitous genes/transcripts:
            Expressed (expression value > 0) in at least (100 - X)% of cells
    Input data:
        data is an array of shape (p,n)
    """
    total_cells = data.shape[1]
    count_1 = data[data >= 1].count(axis=1)
    count_2 = data[data > 0].count(axis=1)

    genelist_1 = count_1[count_1 > 0.01 * X * total_cells].index
    genelist_2 = count_2[count_2 < 0.01 * (100 - X) * total_cells].index
    genelist = set(genelist_1) & set(genelist_2)
    data = data.loc[genelist]
    return data


def sort_by_mad(data, axis=0):
    """
    Sort genes by mad to select input features
    """
    genes = data.mad(axis=axis).sort_values(ascending=False).index
    if axis == 0:
        data = data.loc[:, genes]
    else:
        data = data.loc[genes]
    return data


# =========== scATAC Preprocessing =============
# ==============================================
def peak_filter(data, x=10, n_reads=2):
    count = data[data >= n_reads].count(1)
    index = count[count >= x].index
    data = data.loc[index]
    return data


def cell_filter(data):
    thresh = data.shape[0] / 50
    # thresh = min(min_peaks, data.shape[0]/50)
    data = data.loc[:, data.sum(0) > thresh]
    return data


def sample_filter(data, x=10, n_reads=2):
    data = peak_filter(data, x, n_reads)
    data = cell_filter(data)
    return data


# =================== Other ====================
# ==============================================

from scipy.sparse.linalg import eigsh


def estimate_k(data):
    """
    Estimate number of groups k:
        based on random matrix theory (RTM), borrowed from SC3
        input data is (p,n) matrix, p is feature, n is sample
    """
    p, n = data.shape

    x = scale(data, with_mean=False)
    muTW = (np.sqrt(n - 1) + np.sqrt(p)) ** 2
    sigmaTW = (np.sqrt(n - 1) + np.sqrt(p)) * (1 / np.sqrt(n - 1) + 1 / np.sqrt(p)) ** (1 / 3)
    sigmaHatNaive = x.T.dot(x)

    bd = np.sqrt(p) * sigmaTW + muTW
    evals, _ = eigsh(sigmaHatNaive)

    k = 0
    for i in range(len(evals)):
        if evals[i] > bd:
            k += 1
    return k


# def estimate_k(data):
#     return min(data.shape[0]/100, 30)

def get_decoder_weight(model_file):
    state_dict = torch.load(model_file)
    weight = state_dict['decoder.reconstruction.weight'].data.cpu().numpy()
    return weight


def peak_selection(weight, weight_index, kind='both', cutoff=2.5):
    """
    Select represented peaks of each components of each peaks,
    correlations between peaks and features are quantified by decoder weight,
    weight is a Gaussian distribution,
    filter peaks with weights more than cutoff=2.5 standard deviations from the mean.

    Input:
        weight: weight of decoder
        weight_index: generated peak/gene index.
        kind: both for both side, pos for positive side and neg for negative side.
        cutoff: cutoff of standard deviations from mean.
    """
    std = weight.std(0)
    mean = weight.mean(0)  # 每一个zi，对所有输出节点的平均权重
    specific_peaks = []
    for i in range(10):
        w = weight[:, i]  # zi对应的权重，shape：1, n_input
        if kind == 'both':
            index = np.where(np.abs(w - mean[i]) > cutoff * std[i])[0]
        if kind == 'pos':
            index = np.where(w - mean[i] > cutoff * std[i])[0]
        if kind == 'neg':
            index = np.where(mean[i] - w > cutoff * std[i])[0]
        specific_peaks.append(weight_index[index])
    return specific_peaks


def pairwise_pearson(A, B):
    from scipy.stats import pearsonr
    corrs = []
    for i in range(A.shape[0]):
        if A.shape == B.shape:
            corr = pearsonr(A.iloc[i], B.iloc[i])[0]
        else:
            corr = pearsonr(A.iloc[i], B)[0]
        corrs.append(corr)
    return corrs


# ================= Metrics ===================
# =============================================

def reassign_cluster_with_ref(Y_pred, Y):
    """
    Reassign cluster to reference labels
    Inputs:
        Y_pred: predict y classes
        Y: true y classes
    Return:
        f1_score: clustering f1 score
        y_pred: reassignment index predict y classes
        indices: classes assignment
    """

    def reassign_cluster(y_pred, index):
        y_ = np.zeros_like(y_pred)
        # for (i, j) in index:
        for (i, j) in zip(index[0], index[1]):
            y_[np.where(y_pred == i)] = j
        return y_

    from scipy.optimize import linear_sum_assignment as linear_assignment
    # from sklearn.utils.linear_assignment_ import linear_assignment
    #     print(Y_pred.size, Y.size)
    assert Y_pred.size == Y.size
    D = max(Y_pred.max(), Y.max()) + 1
    w = np.zeros((D, D), dtype=np.int64)
    for i in range(Y_pred.size):
        w[Y_pred[i], Y[i]] += 1
    ind = linear_assignment(w.max() - w)

    return reassign_cluster(Y_pred, ind)


def cluster_report(ref, pred):
    print("\n## Clustering Evaluation Report ##")
    pred = reassign_cluster_with_ref(pred, ref)
    cm = confusion_matrix(ref, pred)
    print('# Confusion matrix: #')
    print(cm)
    ari = adjusted_rand_score(ref, pred)
    nmi = normalized_mutual_info_score(ref, pred)
    f1 = f1_score(ref, pred, average='micro')
    print('# Metric values: #')
    print("Adjusted Rand Index score: {:.4f}".format(ari))
    print("`Normalized Mutual Info score: {:.4f}".format(nmi))
    print("`f1 score: {:.4f}".format(f1))
    res = locals()
    res.pop("ref")
    res.pop("pred")
    return res


def binarization(imputed, raw):
    return scipy.sparse.csr_matrix((imputed.T > raw.mean(1).T).T & (imputed > raw.mean(0))).astype(np.int8)
def config_dump(dic,fpath,fname):
    import pickle as pkl
    import os
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    with open(os.path.join(fpath,fname),"wb") as f:
        pkl.dump(dic,f)
    return True
def normalize(A , symmetric=True):
    # A = A+I
    A = A + torch.eye(A.size(0))
    # 所有节点的度
    d = A.sum(1)
    if symmetric:
        #D = D^-1/2
        D = torch.diag(torch.pow(d , -0.5))
        return D.mm(A).mm(D)
    else :
        # D=D^-1
        D =torch.diag(torch.pow(d,-1))
        return D.mm(A)


if __name__ == '__main__':
    import scanpy as sc
    import anndata
    # adata=sc.read_h5ad("../../../data_processed/10XBlood.h5ad")
    # X=3
    # data=adata.to_df().T
    # total_cells = data.shape[1]
    # count_1 = data[data >= 1].count(axis=1)
    # count_2 = data[data > 0].count(axis=1)
    # genelist_1 = count_1[count_1 > 0.01 * X * total_cells].index
    # genelist_2 = count_2[count_2 < 0.01 * (100 - X) * total_cells].index
    # genelist = set(genelist_1) & set(genelist_2)
    # data = data.loc[genelist]
    # # data1 = gene_filter_(,X=3)
    # data = sample_filter(data,50,1)
    #
    # var = adata.var.loc[data.index]
    # obs = adata.obs.loc[data.columns]
    # adata = anndata.AnnData(X=data.T,var=var,obs=obs)
    # adata.X = scipy.sparse.csr_matrix(adata.X)
    #
    # outdir="../../../data_processed/10XBlood_filtered.h5ad"
    # try:
    #     adata.raw = None
    #     adata.write(outdir, compression='gzip')
    # except Exception:
    #     adata.__dict__['_raw'].__dict__['_var'] = adata.__dict__['_raw'].__dict__['_var'].rename(
    #         columns={'_index': 'features'})
    #     adata.raw = None
    #     adata.write(outdir, compression='gzip')
    #
    #
    # adata=sc.read_h5ad("../../../data_processed/DropBlood.h5ad")
    # X=3
    # data=adata.to_df().T
    # total_cells = data.shape[1]
    # count_1 = data[data >= 1].count(axis=1)
    # count_2 = data[data > 0].count(axis=1)
    # genelist_1 = count_1[count_1 > 0.01 * X * total_cells].index
    # genelist_2 = count_2[count_2 < 0.01 * (100 - X) * total_cells].index
    # genelist = set(genelist_1) & set(genelist_2)
    # data = data.loc[genelist]
    # # data1 = gene_filter_(,X=3)
    # data = sample_filter(data,50,1)
    #
    # var = adata.var.loc[data.index]
    # obs = adata.obs.loc[data.columns]
    # adata = anndata.AnnData(X=data.T,var=var,obs=obs)
    # adata.X = scipy.sparse.csr_matrix(adata.X)
    #
    # outdir="../../../data_processed/DropBlood_filtered.h5ad"
    # try:
    #     # adata.__dict__['_raw'].__dict__['_var'] = adata.__dict__['_raw'].__dict__['_var'].rename(
    #     #     columns={'_index': 'features'})
    #     adata.raw = None
    #     adata.write(outdir, compression='gzip')
    # except Exception:
    #     adata.__dict__['_raw'].__dict__['_var'] = adata.__dict__['_raw'].__dict__['_var'].rename(
    #         columns={'_index': 'features'})
    #     adata.raw = None
    #     adata.write(outdir, compression='gzip')
    #
    #
    # adata=sc.read_h5ad("../../../data_processed/Buenrostro2018.h5ad")
    # X=3
    # data=adata.to_df().T
    # total_cells = data.shape[1]
    # count_1 = data[data >= 1].count(axis=1)
    # count_2 = data[data > 0].count(axis=1)
    # genelist_1 = count_1[count_1 > 0.01 * X * total_cells].index
    # genelist_2 = count_2[count_2 < 0.01 * (100 - X) * total_cells].index
    # genelist = set(genelist_1) & set(genelist_2)
    # data = data.loc[genelist]
    # # data1 = gene_filter_(,X=3)
    # data = sample_filter(data,50,1)
    #
    # var = adata.var.loc[data.index]
    # obs = adata.obs.loc[data.columns]
    # adata = anndata.AnnData(X=data.T,var=var,obs=obs)
    # adata.X = scipy.sparse.csr_matrix(adata.X)
    #
    # outdir="../../../data_processed/Buenrostro2018_filtered.h5ad"
    # try:
    #     # adata.__dict__['_raw'].__dict__['_var'] = adata.__dict__['_raw'].__dict__['_var'].rename(
    #     #     columns={'_index': 'features'})
    #     adata.raw = None
    #     adata.write(outdir, compression='gzip')
    # except Exception:
    #     adata.__dict__['_raw'].__dict__['_var'] = adata.__dict__['_raw'].__dict__['_var'].rename(
    #         columns={'_index': 'features'})
    #     adata.raw = None
    #     adata.write(outdir, compression='gzip')
    #
    #
    # adata=sc.read_h5ad("../../../data_processed/MouseAtlas.h5ad")
    # X=3
    # data=adata.to_df().T
    # total_cells = data.shape[1]
    # count_1 = data[data >= 1].count(axis=1)
    # count_2 = data[data > 0].count(axis=1)
    # genelist_1 = count_1[count_1 > 0.01 * X * total_cells].index
    # genelist_2 = count_2[count_2 < 0.01 * (100 - X) * total_cells].index
    # genelist = set(genelist_1) & set(genelist_2)
    # data = data.loc[genelist]
    # # data1 = gene_filter_(,X=3)
    # data = sample_filter(data,50,1)
    #
    # var = adata.var.loc[data.index]
    # obs = adata.obs.loc[data.columns]
    # adata = anndata.AnnData(X=data.T,var=var,obs=obs)
    # adata.X = scipy.sparse.csr_matrix(adata.X)
    #
    # outdir="../../../data_processed/MouseAtlas_filtered.h5ad"
    # try:
    #     adata.raw = None
    #     adata.write(outdir, compression='gzip')
    # except Exception:
    #     adata.__dict__['_raw'].__dict__['_var'] = adata.__dict__['_raw'].__dict__['_var'].rename(
    #         columns={'_index': 'features'})
    #     adata.raw = None
    #     adata.write(outdir, compression='gzip')
    #
    #
    #
    # adata=sc.read_h5ad("../../../data_processed/BoneMarrow.h5ad")
    # X=3
    # data=adata.to_df().T
    # total_cells = data.shape[1]
    # count_1 = data[data >= 1].count(axis=1)
    # count_2 = data[data > 0].count(axis=1)
    # genelist_1 = count_1[count_1 > 0.01 * X * total_cells].index
    # genelist_2 = count_2[count_2 < 0.01 * (100 - X) * total_cells].index
    # genelist = set(genelist_1) & set(genelist_2)
    # data = data.loc[genelist]
    # # data1 = gene_filter_(,X=3)
    # data = sample_filter(data,50,1)
    #
    # var = adata.var.loc[data.index]
    # obs = adata.obs.loc[data.columns]
    # adata = anndata.AnnData(X=data.T,var=var,obs=obs)
    # adata.X = scipy.sparse.csr_matrix(adata.X)
    #
    # outdir="../../../data_processed/BoneMarrow_filtered.h5ad"
    # try:
    #     adata.raw = None
    #     adata.write(outdir, compression='gzip')
    # except Exception:
    #     adata.__dict__['_raw'].__dict__['_var'] = adata.__dict__['_raw'].__dict__['_var'].rename(
    #         columns={'_index': 'features'})
    #     adata.raw = None
    #     adata.write(outdir, compression='gzip')



    adata=sc.read_h5ad("../../../data_processed/myForebrain.h5ad")
    X=3
    data=adata.to_df().T
    total_cells = data.shape[1]
    count_1 = data[data >= 1].count(axis=1)
    count_2 = data[data > 0].count(axis=1)
    genelist_1 = count_1[count_1 > 0.01 * X * total_cells].index
    genelist_2 = count_2[count_2 < 0.01 * (100 - X) * total_cells].index
    genelist = set(genelist_1) & set(genelist_2)
    data = data.loc[genelist]
    # data1 = gene_filter_(,X=3)
    data = sample_filter(data,50,1)

    var = adata.var.loc[data.index]
    obs = adata.obs.loc[data.columns]
    adata = anndata.AnnData(X=data.T,var=var,obs=obs)
    adata.X = scipy.sparse.csr_matrix(adata.X)

    outdir="../../../data_processed/myForebrain_filtered.h5ad"
    try:
        adata.raw = None
        adata.write(outdir, compression='gzip')
    except Exception:
        adata.__dict__['_raw'].__dict__['_var'] = adata.__dict__['_raw'].__dict__['_var'].rename(
            columns={'_index': 'features'})
        adata.raw = None
        adata.write(outdir, compression='gzip')



    adata=sc.read_h5ad("../../../data_processed/myLeukemia.h5ad")
    X=3
    data=adata.to_df().T
    total_cells = data.shape[1]
    count_1 = data[data >= 1].count(axis=1)
    count_2 = data[data > 0].count(axis=1)
    genelist_1 = count_1[count_1 > 0.01 * X * total_cells].index
    genelist_2 = count_2[count_2 < 0.01 * (100 - X) * total_cells].index
    genelist = set(genelist_1) & set(genelist_2)
    data = data.loc[genelist]
    # data1 = gene_filter_(,X=3)
    data = sample_filter(data,50,1)

    var = adata.var.loc[data.index]
    obs = adata.obs.loc[data.columns]
    adata = anndata.AnnData(X=data.T,var=var,obs=obs)
    adata.X = scipy.sparse.csr_matrix(adata.X)

    outdir="../../../data_processed/myLeukemia_filtered.h5ad"
    try:
        adata.raw = None
        adata.write(outdir, compression='gzip')
    except Exception:
        adata.__dict__['_raw'].__dict__['_var'] = adata.__dict__['_raw'].__dict__['_var'].rename(
            columns={'_index': 'features'})
        adata.raw = None
        adata.write(outdir, compression='gzip')


    adata=sc.read_h5ad("../../../data_processed/myLeukemia.h5ad")
    X=3
    data=adata.to_df().T
    total_cells = data.shape[1]
    count_1 = data[data >= 1].count(axis=1)
    count_2 = data[data > 0].count(axis=1)
    genelist_1 = count_1[count_1 > 0.01 * X * total_cells].index
    genelist_2 = count_2[count_2 < 0.01 * (100 - X) * total_cells].index
    genelist = set(genelist_1) & set(genelist_2)
    data = data.loc[genelist]
    # data1 = gene_filter_(,X=3)
    data = sample_filter(data,10,1)

    var = adata.var.loc[data.index]
    obs = adata.obs.loc[data.columns]
    adata = anndata.AnnData(X=data.T,var=var,obs=obs)
    adata.X = scipy.sparse.csr_matrix(adata.X)

    outdir="../../../data_processed/myLeukemia_filtered.h5ad"
    try:
        adata.raw = None
        adata.write(outdir, compression='gzip')
    except Exception:
        adata.__dict__['_raw'].__dict__['_var'] = adata.__dict__['_raw'].__dict__['_var'].rename(
            columns={'_index': 'features'})
        adata.raw = None
        adata.write(outdir, compression='gzip')




    adata=sc.read_h5ad("/home/haogaoyang/data/ATAC/GSE192772_HumanBrain/HumanBrain.h5ad")
    X=3
    data=adata.to_df().T
    total_cells = data.shape[1]
    count_1 = data[data >= 1].count(axis=1)
    count_2 = data[data > 0].count(axis=1)
    genelist_1 = count_1[count_1 > 0.01 * X * total_cells].index
    genelist_2 = count_2[count_2 < 0.01 * (100 - X) * total_cells].index
    genelist = set(genelist_1) & set(genelist_2)
    data = data.loc[genelist]
    # data1 = gene_filter_(,X=3)
    data = sample_filter(data,10,1)

    var = adata.var.loc[data.index]
    obs = adata.obs.loc[data.columns]
    adata = anndata.AnnData(X=data.T,var=var,obs=obs)
    adata.X = scipy.sparse.csr_matrix(adata.X)

    outdir="/home/haogaoyang/data/ATAC/GSE192772_HumanBrain/HumanBrain_filtered.h5ad"
    try:
        adata.raw = None
        adata.write(outdir, compression='gzip')
    except Exception:
        adata.__dict__['_raw'].__dict__['_var'] = adata.__dict__['_raw'].__dict__['_var'].rename(
            columns={'_index': 'features'})
        adata.raw = None
        adata.write(outdir, compression='gzip')


    adata=sc.read_h5ad("/home/haogaoyang/data/ATAC/GSE164439_MouseTestes/HumanBrain_IN.h5ad")
    X=3
    data=adata.to_df().T
    total_cells = data.shape[1]
    count_1 = data[data >= 1].count(axis=1)
    count_2 = data[data > 0].count(axis=1)
    genelist_1 = count_1[count_1 > 0.01 * X * total_cells].index
    genelist_2 = count_2[count_2 < 0.01 * (100 - X) * total_cells].index
    genelist = set(genelist_1) & set(genelist_2)
    data = data.loc[genelist]
    # data1 = gene_filter_(,X=3)
    data = sample_filter(data,10,1)

    var = adata.var.loc[data.index]
    obs = adata.obs.loc[data.columns]
    adata = anndata.AnnData(X=data.T,var=var,obs=obs)
    adata.X = scipy.sparse.csr_matrix(adata.X)

    outdir="/home/haogaoyang/data/ATAC/GSE192772_HumanBrain/HumanBrain_IN_filtered.h5ad"
    try:
        adata.raw = None
        adata.write(outdir, compression='gzip')
    except Exception:
        adata.__dict__['_raw'].__dict__['_var'] = adata.__dict__['_raw'].__dict__['_var'].rename(
            columns={'_index': 'features'})
        adata.raw = None
        adata.write(outdir, compression='gzip')


    adata=sc.read_h5ad("/home/haogaoyang/data/ATAC/GSE164439_MouseTestes/HumanBrain_EX.h5ad")
    X=3
    data=adata.to_df().T
    total_cells = data.shape[1]
    count_1 = data[data >= 1].count(axis=1)
    count_2 = data[data > 0].count(axis=1)
    genelist_1 = count_1[count_1 > 0.01 * X * total_cells].index
    genelist_2 = count_2[count_2 < 0.01 * (100 - X) * total_cells].index
    genelist = set(genelist_1) & set(genelist_2)
    data = data.loc[genelist]
    # data1 = gene_filter_(,X=3)
    data = sample_filter(data,10,1)

    var = adata.var.loc[data.index]
    obs = adata.obs.loc[data.columns]
    adata = anndata.AnnData(X=data.T,var=var,obs=obs)
    adata.X = scipy.sparse.csr_matrix(adata.X)

    outdir="/home/haogaoyang/data/ATAC/GSE192772_HumanBrain/HumanBrainEX_filtered.h5ad"
    try:
        adata.raw = None
        adata.write(outdir, compression='gzip')
    except Exception:
        adata.__dict__['_raw'].__dict__['_var'] = adata.__dict__['_raw'].__dict__['_var'].rename(
            columns={'_index': 'features'})
        adata.raw = None
        adata.write(outdir, compression='gzip')



    adata=sc.read_h5ad("/home/haogaoyang/data/ATAC/GSE192772_HumanBrain/HumanBrain_sub.h5ad")
    X=3
    data=adata.to_df().T
    total_cells = data.shape[1]
    count_1 = data[data >= 1].count(axis=1)
    count_2 = data[data > 0].count(axis=1)
    genelist_1 = count_1[count_1 > 0.01 * X * total_cells].index
    genelist_2 = count_2[count_2 < 0.01 * (100 - X) * total_cells].index
    genelist = set(genelist_1) & set(genelist_2)
    data = data.loc[genelist]
    # data1 = gene_filter_(,X=3)
    data = sample_filter(data,10,1)

    var = adata.var.loc[data.index]
    obs = adata.obs.loc[data.columns]
    adata = anndata.AnnData(X=data.T,var=var,obs=obs)
    adata.X = scipy.sparse.csr_matrix(adata.X)

    outdir="/home/haogaoyang/data/ATAC/GSE192772_HumanBrain/HumanBrain_sub_filtered.h5ad"
    try:
        adata.raw = None
        adata.write(outdir, compression='gzip')
    except Exception:
        adata.__dict__['_raw'].__dict__['_var'] = adata.__dict__['_raw'].__dict__['_var'].rename(
            columns={'_index': 'features'})
        adata.raw = None
        adata.write(outdir, compression='gzip')

    # sc.pp.subsample

