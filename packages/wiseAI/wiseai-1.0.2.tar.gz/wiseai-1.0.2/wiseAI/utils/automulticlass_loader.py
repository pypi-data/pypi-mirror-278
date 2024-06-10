import os
import shutil
from pathlib import Path
from typing import Dict, List

import pandas as pd
from autogluon.tabular import TabularPredictor

MODEL_DIR = Path.home().joinpath("wiseai_models")

class AutoMultiClassLoader:
    def __init__(
        self,
        model_name: str,
        model_version: str,
        path: str = None,
    ):
        """
        학습한 모델을 불러옵니다.
        ## 참고 사항
        - `fit` 함수를 통해 학습이 된 경우에만 정상적으로 동작합니다.
        ## Args
        - model_name: (str) 모델명
        - model_name: (str) 모델버전
        - path: (str) Sub Models 저장 경로
        ## Example
        print(my_model_v1.batch_prediction(test_data, "predict"))
        """
        assert isinstance(model_name, str), "`model_name(는) str 타입이어야 합니다.`"
        assert isinstance(model_version, str), "`model_version(는) str 타입이어야 합니다.`"
        self.model_name = model_name
        self.model_version = model_version
        if path == None:
            self.path = MODEL_DIR.joinpath(self.model_name, self.model_version)
        else:
            assert isinstance(path, str), "`path(는) str 타입이어야 합니다.`"
            self.path = path
        
    def load_models(self):
        self.models = TabularPredictor.load(self.path)
        self.label = self.models.label
        self.features = self.models.features()
        self.eval_metric = self.models.eval_metric
        
    def batch_prediction(self, batch_data: pd.DataFrame, predict_fn) -> pd.DataFrame:
        """
        학습한 모델의 배치 예측을 지원합니다.
        ## 참고 사항
        - `fit` 함수를 통해 학습이 된 경우에만 정상적으로 동작합니다.
        ## Args
        - batch_data: (optional) (`pandas.DataFrame`) 예측을 위한 테스트 데이터 프레임 (기본값: None)
        ## Example
        kyu_models = AutoBinaryLoader(model_name= 'kyu_test_model', model_version = 'v1')
        kyu_models.load_models()
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