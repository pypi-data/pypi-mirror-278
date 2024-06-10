from typing import Any, Dict, List, Union
import random
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularPredictor


class MultiClassImbalanceChain:  # 추후 수정 필요. 급해서 학습 시 마다 split 하게 만들지 않음. 정해진 조건 하에서만 제대로 동작.
    def __init__(
        self,
        X: None,
        y: None,
        base_model=TabularPredictor,
        random_state=2024,
        order=None,
        time_limit=60 * 15,
        test_size=0.8,
    ):
        """
        2024.03.04 v1 개발
        Contact : 이규남(kyunam@sk.com)

        Parameters
        ----------
        X : 학습 데이터
        y : 학습을 위한 정답 데이터
        base_model : 학습에 사용할 기초 모델
        random_state : 시드 값. 모델 교육이 아닌 분할 프로세스에만 영향을 미침.
        order : multi label 정답의 학습 순서
         - 기본 값은 순서대로, random 값과 정해진 학습 순서([1, 2, 3])를 받음
        time_limit : 학습에 걸리는 시간, default 는 모델 당 15분
        ----------
        """
        assert isinstance(X, pd.DataFrame), "`X은(는) pd.DataFrame 타입이어야 합니다.`"
        assert isinstance(y, pd.DataFrame), "`y은(는) pd.DataFrame 타입이어야 합니다.`"

        assert base_model is not None, "`모델은(는) None이 아니어야 합니다.`"
        if order == "random":
            pass
        elif type(order) == list:
            assert (
                len(order) == y.shape[1]
            ), "`order로 입력된 길이와 정답 수가 일치하지 않습니다.`"

        assert isinstance(
            random_state, int
        ), "`random_state은(는) int 타입이어야 합니다.`"
        self.random_state = random_state
        assert isinstance(
            test_size, float
        ), "`test_size는(은) float 타입이어야 합니다.`"
        self.test_size = test_size

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, shuffle=True, random_state=self.random_state
        )  # , stratify=y

        self.base_model = base_model
        self.order = order
        self.X_train = pd.DataFrame(X_train, columns=X.columns)
        self.X_test = pd.DataFrame(X_test, columns=X.columns)
        self.y_train = pd.DataFrame(y_train, columns=y.columns)
        self.y_test = pd.DataFrame(y_test, columns=y.columns)
        self.time_limit = time_limit

    def fit(self):
        if self.order is None:
            self.order = list(range(self.y_train.shape[1]))
        elif self.order == "random":
            self.order = list(range(self.y_train.shape[1]))
            random.shuffle(self.order)
        else:
            if len(self.order) == self.y_train.shape[1]:
                self.order = [o - 1 for o in self.order]

        self.models = []

        for val in self.order:
            X_joined = pd.concat(
                [self.X_train, self.y_train.iloc[:, self.order]], axis=1
            )

        print(f"number of ground true is {self.y_train.shape[1]}")
        for chain_index in range(0, self.y_train.shape[1]):
            print(f"\n{chain_index}th Prepare running")
            y_vals = self.y_train.iloc[:, self.order[chain_index]]
            t_X = X_joined.iloc[:, : (self.X_train.shape[1] + chain_index)]
            print(f"{chain_index}th running Start")
            predictor = self.base_model(
                label=self.y_train.columns[self.order[chain_index]],
                sample_weight="balance_weight",
                verbosity=0,
            ).fit(
                pd.concat([t_X, y_vals], axis=1),
                time_limit=self.time_limit,
                presets="best_quality",  # [‘best_quality’, ‘high_quality’, ‘good_quality’, ‘medium_quality’, ‘optimize_for_deployment’, ‘interpretable’, ‘ignore_text’]
                excluded_model_types=[
                    "FASTAI",
                    "FASTTEXT",
                    "AG_TEXT_NN",
                    "TRANSF",
                    "KNN",
                ],  #'RF', 'CAT', 'XGB', 'XT',
                keep_only_best=True,
            )
            self.models.append(predictor)
            print(f"{chain_index}th running Done")

    def evaluate(self):
        evaluation = []
        for val in self.order:
            X_joined = pd.concat([self.X_test, self.y_test.iloc[:, self.order]], axis=1)

        for chain_index in range(0, self.y_test.shape[1]):
            y_vals = self.y_test.iloc[:, self.order[chain_index]]
            t_X = X_joined.iloc[:, : (self.X_test.shape[1] + chain_index)]
            evaluation.append(
                self.models[chain_index].evaluate(pd.concat([t_X, y_vals], axis=1))
            )
        return evaluation

    def predict_proba(self, X_data):
        assert isinstance(
            X_data, pd.DataFrame
        ), "`X은(는) pd.DataFrame 타입이어야 합니다.`"

        pred_chain = pd.DataFrame(columns=[self.y_train.columns[i] for i in self.order])
        self.pred_probs = pd.DataFrame(
            columns=[self.y_train.columns[i] for i in self.order]
        )

        for chain_index, model in enumerate(self.models):
            prev_preds = pred_chain.iloc[:, :chain_index]
            X_joined = pd.concat([X_data, prev_preds], axis=1)
            pred_proba = self.models[chain_index].predict_proba(X_joined)[[1]]
            self.pred_probs[self.y_train.columns[chain_index]] = pred_proba.squeeze()
        return self.pred_probs

    def evaluate_new_data(self, test_X, test_y):
        evaluation = []

        test_X = test_X[self.X_train.columns]
        test_y = test_y[self.y_train.columns]

        for val in self.order:
            X_joined = pd.concat([test_X, test_y.iloc[:, self.order]], axis=1)

        for chain_index in range(0, test_y.shape[1]):
            y_vals = test_y.iloc[:, self.order[chain_index]]
            t_X = X_joined.iloc[:, : (test_X.shape[1] + chain_index)]
            evaluation.append(
                self.models[chain_index].evaluate(pd.concat([t_X, y_vals], axis=1))
            )
        return evaluation
