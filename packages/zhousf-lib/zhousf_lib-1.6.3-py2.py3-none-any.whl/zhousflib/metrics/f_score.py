# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Function:
# pip install scikit-learn
from sklearn.metrics import confusion_matrix as confusion_matrix_compute
from sklearn.metrics import fbeta_score


class FBetaScore(object):
    """
    适用于二分类的评估系统
    """

    def __init__(self, y_true: list, y_pre: list, f_beta: list):
        self.y_true = y_true
        self.y_pre = y_pre
        self.f_beta = f_beta if f_beta is not None else [1]
        self.tn, self.fp, self.fn, self.tp = self.confusion_matrix(y_true=self.y_true, y_pre=self.y_pre)
        self.recall = self.tp / (self.tp + self.fn)
        self.precision = self.tp / (self.tp + self.fp)
        self.f_beta_score = self.f_beta_score_compute(f_beta=self.f_beta, y_true=self.y_true, y_pre=self.y_pre)

    def print(self, is_print=True):
        from prettytable import PrettyTable
        table = PrettyTable(field_names=["confusion matrix", "recall", "precision", "f_beta_score"],
                            title="F_beta Score Statistical Table (total={0})".format(len(self.y_true)))
        row = ["tp={0}  fp={1}\nfn={2}  tn={3}".format(self.tp, self.fp, self.fn, self.tn),
               "tp/(tp+fn)={0}/{1}\nrecall={2}".format(self.tp, self.tp + self.fn, self.recall),
               "tp/(tp+fp)={0}/{1}\nprecision={2}".format(self.tp, self.tp + self.fp, self.precision)]
        union = []
        for i, beta in enumerate(self.f_beta):
            union.append("f_{0}={1}".format(beta, self.f_beta_score[i]))
        row.append("\n".join(union))
        table.add_row(row)
        table.align = "l"
        # table.align["confusion matrix"] = "c"
        if is_print:
            print(table)
        return table

    def confusion_matrix(self, y_true: list, y_pre: list):
        """
        1为正例，0为负例
        TP 预测为1，实际为1，预测正确
        FP 预测为1，实际为0，预测错误
        FN 预测为0，实际为1，预测错误
        TN 预测为0，实际为0，预测正确
        """
        self.tn, self.fp, self.fn, self.tp = confusion_matrix_compute(y_true=y_true, y_pred=y_pre).ravel()
        return self.tn, self.fp, self.fn, self.tp

    def f_beta_score_compute(self, f_beta: list, y_true: list = None, y_pre: list = None):
        """
        Fβ分数 = (1 + β^2) * (精确率 * 召回率) / (β^2 * 精确率 + 召回率)
        β参数决定了精确率和召回率的相对权重
        当 β = 0 时，则Fβ分数等于precision
        当 β < 1 时，则模型偏向精确率
        当 β = 1 时，则Fβ=F1，精确率权重等于召回率权重
        当 β > 1 时，则模型偏向召回率
        :param f_beta:
        :param y_true:
        :param y_pre:
        """
        if y_true is None:
            y_true = self.y_true
        if y_pre is None:
            y_pre = self.y_pre
        f_score = []
        for beta in f_beta:
            f_score.append(fbeta_score(y_true=y_true, y_pred=y_pre, beta=beta))
        # f_score = (1 + beta ** 2) * (precision * recall) / (beta ** 2 * precision + recall)
        return f_score


if __name__ == "__main__":
    actual_labels = [0, 1, 0, 1, 1, 0, 0, 0, 0, 0]
    predicted_labels = [0, 1, 0, 1, 0, 1, 1, 0, 0, 0]
    score = FBetaScore(y_true=actual_labels, y_pre=predicted_labels, f_beta=[1, 1.1, 2])
    score.print()

