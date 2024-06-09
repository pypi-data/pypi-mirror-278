import numpy as np

def Precision_Recall_f1score(Reals, Preds):
    TP, TN, FP, FN = 0, 0, 0, 0
    for real, pred in zip(Reals, Preds):
        if [real, pred] == [0, 0] : TN += 1
        elif [real, pred] == [0, 1] : FP += 1
        elif [real, pred] == [1, 0] : FN += 1
        else: TP += 1

    if TP+FN+FP==0:
        return [0,0,0]
    elif TP+FN==0:
        P = TP/(TP+FP)
        return [P,0,0]
    elif TP+FP==0:
        R = TP/(TP+FN)
        return [0,R,0]

    R = TP / (TP + FN)
    P = TP / (TP + FP)
    if R + P == 0:
        return [R,P,0]

    F1 = 2 * R * P / (R + P)
    return [P, R, F1]

def return_PRF_values(r, p, t1, t2):
    precision, recall, f1score = Precision_Recall_f1score(r, p)
    Time = round(t2 - t1, 3)
    num_real, num_pred = len(np.where(r==1)[0]), sum(p)
    return [num_real, num_pred, precision, recall, f1score, Time]

