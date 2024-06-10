import os
import shutil
from pathlib import Path
from typing import Dict, List

import pandas as pd
from autogluon.tabular import TabularPredictor

MODEL_DIR = Path.home().joinpath("wiseai_models")


class AutoBinaryML:
    def __init__(
        self,
        model_name: str,
        model_version: str,
        train_data: pd.DataFrame,
        label: str,
        path: str = None,
        presets: str = "best_quality",
        non_training_features: List[str] = [],
        eval_metric: str = "roc_auc",
        time_limit: int = None,
        excluded_model_types: List[str] = [
            "FASTTEXT",
            "AG_TEXT_NN",
            "TRANSF",
            "custom",
        ],
        keep_only_best =True,
        overwrite=True,
    ):
        """
        2024.06.01 v1 개발
        Contact : 이규남(kyunam@sk.com), 김태형(th0804@sk.com), 강예진(yejin.k@sk.com), 정유철(jungyc@sk.com), 진기훈(kh.jin@sk.com), 송지영(jiyoung.song@sk.com)

        AutoML을 통해 모델을 학습합니다.
        Class의 개수는 Multi가 아니라 2개 까지 지원합니다. 3개 이상의 Class는 타 함수를 참조바랍니다.

        ## 참고 사항
        - AutoML이 자동으로 학습합니다.
        - 성능 지표를 설정할 수 있으나, 분류 문제의 경우 기본값인 `roc_auc` 사용을 권장합니다.
        - 회귀 문제에 분류 성능 지표를 세팅하거나 분류 문제에 회귀 성능 지표를 세팅하면 에러가 발생합니다.
        ## Args
        - model_name: (str) 모델명
        - model_name: (str) 모델버전
        - train_data: (`pandas.DataFrame`) 학습에 사용할 데이터 프레임
        - label: (str) train_data 내 라벨 컬럼 이름
        - path: (str) Sub Models 저장 경로
        - preset: (str) Model 성능, 속도 관련 parameter
            - 가능한 값: `best_quality`|`high_quality`|`good_quality`|`medium_quality`|`optimize_for_deployment`
            best_quality : 예측 정확도를 최대화하며, 추론 시간이나 디스크 사용량은 거의 고려하지 않습니다. 큰 time_limit 값을 지정하여 더 나은 결과를 얻을 수 있습니다. 최고의 모델 정확도가 필요한 애플리케이션에 권장됩니다.
            high_quality : 빠른 추론과 높은 예측 정확도를 제공합니다. best_quality보다 추론이 약 10배-200배 빠르고 디스크 사용량이 약 10배-200배 적습니다. 합리적인 추론 속도 및/또는 모델 크기가 필요한 애플리케이션에 권장됩니다.
            good_quality : 매우 빠른 추론과 좋은 예측 정확도를 제공합니다. high_quality보다 추론이 약 4배 빠르고 디스크 사용량이 약 4배 적습니다. 빠른 추론 속도가 필요한 애플리케이션에 권장됩니다.
            medium_quality : 매우 빠른 추론 및 훈련 시간과 중간 수준의 예측 정확도를 제공합니다. good_quality보다 훈련이 약 20배 빠릅니다. 일반적으로 빠른 프로토타이핑 개발에만 사용 권장합니다. 
            optimize_for_deployment : 결과를 즉시 배포할 수 있도록 최적화합니다. medium_quality 대비 모델 정확도나 추론 속도에 부정적인 영향을 주지 않으면서 디스크 사용량을 약 2-4배 줄일 수 있습니다. 이는 여러 고급 기능을 비활성화하지만, 추론에는 영향을 미치지 않습니다. 
        - non_training_features: (optional) (str) 학습에서 제외할 피쳐 이름 리스트. 후처리 전용 피쳐 등을 명세할 때 사용 가능 (기본값: [])
        - eval_metric: (optional) (str) 성능 지표 (기본값: `roc_auc`)
            - 분류 모델 가능한 값: `accuracy`|`balanced_accuracy`|`f1`|`f1_macro`|`f1_micro`|`f1_weighted`|`roc_auc`|`average_precision`|`precision`|`precision_macro`|`precision_micro`|`precision_weighted`|`recall`|`recall_macro`|`recall_micro`|`recall_weighted`|`log_loss`|`pac_score`
        - time_limit: (optional) (int) 학습 시간 제한 시간 (단위: 초). n개의 모델을 학습하는 경우 1/n초씩 사용. None인 경우 무제한 (기본값: None)
        - excluded_model_types: (optional) (List[str]) Banned subset of model types to avoid training during fit(), even if present in hyperparameters. Reference hyperparameters documentation for what models correspond to each value.
        ## Example
        # 학습 및 테스트 데이터 준비
        train_data, test_data = train_test_split(df, test_size=0.2, random_state=0)
        # 학습
        my_model_v1 = AutoBinaryML(
            train_data=train_data,
            label="some_label"
        )
        my_model_v1.fit()
        # 성능 확인
        print(my_model_v1.evaluate(test_data))
        print(my_model_v1.get_feature_importance(test_data))
        # predict 테스트
        print(my_model_v1.batch_prediction(test_data, "predict"))
        """
        assert isinstance(model_name, str), "`model_name(는) str 타입이어야 합니다.`"
        assert isinstance(model_version, str), "`model_version(는) str 타입이어야 합니다.`"
        self.model_name = model_name
        self.model_version = model_version
        
        assert isinstance(
            train_data, pd.DataFrame
        ), "`train_data은(는) pd.DataFrame 타입이어야 합니다.`"
        assert isinstance(label, str), "`label(는) str 타입이어야 합니다.`"
        assert train_data[label].nunique() != 2, "`label(는) 2개 이어야 합니다.`"
        assert isinstance(
            non_training_features, list
        ), "`non_training_features은(는) list 타입이어야 합니다.`"
        assert isinstance(time_limit, int), "`time_limit(는) int 타입이어야 합니다.`"
        assert isinstance(
            excluded_model_types, list
        ), "`excluded_model_types은(는) list 타입이어야 합니다.`"
        if path == None:
            self.path = MODEL_DIR.joinpath(self.model_name, self.model_version)
        else:
            assert isinstance(path, str), "`path(는) str 타입이어야 합니다.`"
            self.path = path

        assert isinstance(presets, str), "`presets(는) str 타입이어야 합니다.`"
        assert presets in ['best_quality', 'high_quality', 'good_quality', 'medium_quality', 'optimize_for_deployment']
        
        assert isinstance(keep_only_best, bool), "`keep_only_best(는) bool 타입이어야 합니다.`"
        assert isinstance(overwrite, bool), "`overwrite(는) bool 타입이어야 합니다.`"
        
        self.train_data = train_data
        self.label = label
        self.presets = presets
        self.non_training_features = non_training_features
        self.eval_metric = eval_metric
        self.time_limit = time_limit
        self.excluded_model_types = excluded_model_types
        self.keep_only_best = keep_only_best
        self.overwrite = overwrite

    def fit(self):
        if self.overwrite == True:
            if os.path.isdir(self.path):
                shutil.rmtree(self.path)
                try:
                    self.models = self._fit()
                except Exception as e:
                    raise Exception(f"Error occured : {e}")
            else:
                try:
                    self.models = self._fit()
                except Exception as e:
                    raise Exception(f"Error occured : {e}")
        else:
            if os.path.isdir(self.path):
                raise Exception(f"Error occured : 이미 {self.path} 디렉토리가 존재합니다.")
            else:
                try:
                    self.models = self._fit()
                except Exception as e:
                    raise Exception(f"Error occured : {e}")
            
            
    def _fit(self):
        columns = [
            f for f in self.train_data.columns if f not in self.non_training_features
        ]
        predictor = TabularPredictor(
            label=self.label,
            eval_metric=self.eval_metric,
            path=self.path,
            sample_weight="balance_weight",
            verbosity=0,
        )
        return predictor.fit(
            train_data=self.train_data[columns],
            presets=self.presets,
            time_limit=self.time_limit,
            excluded_model_types=self.excluded_model_types,
            keep_only_best=self.keep_only_best,
        )

    def batch_prediction(self, batch_data: pd.DataFrame, predict_fn) -> pd.DataFrame:
        """
        학습한 모델의 배치 예측을 지원합니다.
        ## 참고 사항
        - `fit` 함수를 통해 학습이 된 경우에만 정상적으로 동작합니다.
        ## Args
        - batch_data: (optional) (`pandas.DataFrame`) 예측을 위한 테스트 데이터 프레임 (기본값: None)
        - predict_fn: (str) 예측 조건. `predict`와 `predict_proba`를 받을 수 있으며 각 조건 별 산출값은 아래와 같음.
            predict : 샘플 X에 대한 클래스 레이블 예측을 반환합니다.
            predict_proba :  모든 클래스에 대한 추정치(예측 확률)을 반환합니다.
        ## Example
        print(my_model_v1.batch_prediction(test_data, "predict"))
        """
        assert predict_fn in [
            "predict",
            "predict_proba",
        ], "배치 예측 시 `predict_fn`은 predict, predict_proba 중 하나의 값이어야 합니다."
        
        assert isinstance(
            batch_data, pd.DataFrame
        ), "`batch_data(는) pd.DataFrame 타입이어야 합니다.`"
        
        if predict_fn == "predict":
            return self.models.predict(batch_data)
        elif predict_fn == "predict_proba":
            return self.models.predict_proba(batch_data)

    def evaluate(self, test_data: pd.DataFrame) -> Dict[str, float]:
        """
        학습한 모델의 성능을 계산합니다.
        ## 참고 사항
        - `fit` 함수를 통해 학습이 된 경우에만 정상적으로 동작합니다.
        ## Args
        - test_data: (optional) (`pandas.DataFrame`) 모델 성능 측정을 위한 테스트 데이터 프레임 (기본값: None)
        ## Example
        # 성능 계산
        print(my_model_v1.evaluate(test_data))
        """
        assert isinstance(
            test_data, pd.DataFrame
        ), "`test_data(는) pd.DataFrame 타입이어야 합니다.`"
        
        columns = [f for f in self.models.features()] + [
            self.label
        ]
        return self.models.evaluate(test_data[columns], silent=True)

    def get_feature_importance(self, test_data: pd.DataFrame, feature_importance_time_limit = 60*60) -> pd.Series:
        """
        학습한 모델의 피쳐 중요도를 계산하여 `pandas.Series` 형식으로 리턴합니다.
        ## 참고 사항
        - `fit` 함수를 통해 학습이 된 경우에만 정상적으로 동작합니다.
        - `fit` 함수에서는 모델 학습 후 한 차례 본 함수를 실행하여 `self.feature_importance`에 저장합니다.
        ## Args
        - test_data: (optional) (`pandas.DataFrame`) 모델 성능 측정을 위한 테스트 데이터 프레임 (기본값: None)
        - feature_importance_time_limit: (optional) (`int`) 모델 성능 측정에 소모되는 시간. 적을 수록 연산이 적어 결과를 신뢰하기 어려움.
        ## Example
        # 계산
        print(my_model_v1.get_feature_importance(test_data, 60*60*3)) #3시간
        """
        assert isinstance(
            test_data, pd.DataFrame
        ), "`test_data(는) pd.DataFrame 타입이어야 합니다.`"
        assert isinstance(feature_importance_time_limit, int), "`feature_importance_time_limit(는) int 타입이어야 합니다.`"
        columns = [f for f in self.models.features()] + [
            self.label
        ]
        return self.models.feature_importance(time_limit = feature_importance_time_limit, data = test_data[columns], silent=True)[
            "importance"
        ]
