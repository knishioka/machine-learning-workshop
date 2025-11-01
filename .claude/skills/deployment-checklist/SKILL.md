---
name: deployment-checklist
description: 機械学習モデルを本番環境にデプロイする前のチェックリストとコードを生成。モデルの保存、推論API、モニタリング、テストなど本番運用に必要な要素を網羅します。
---

# Deployment Checklist

このスキルは、機械学習モデルを本番環境にデプロイする際のチェックリストとサンプルコードを提供します。

## When to Use

以下のような場合にこのスキルを使用してください：
- モデルを本番環境にデプロイする準備をしている
- デプロイ前のチェック項目を確認したい
- 推論APIを作成したい
- モデルのモニタリング設定が必要
- 本番運用の準備をしたい

## Instructions

### 1. デプロイメント準備チェックリスト

ユーザーと一緒に以下の項目を確認：

```markdown
## デプロイ前チェックリスト

### モデルの品質
- [ ] モデルの性能が要件を満たしている
- [ ] テストデータでの評価完了
- [ ] 本番環境と同等のデータで検証済み
- [ ] エッジケースのテスト完了
- [ ] バイアス・公平性の評価完了

### モデルの保存とバージョニング
- [ ] モデルが適切な形式で保存されている
- [ ] モデルのバージョン管理ができている
- [ ] モデルのメタデータ（精度、学習日時など）を記録
- [ ] 依存ライブラリのバージョンを固定
- [ ] モデルの再現性を確保（学習スクリプト、データ、パラメータ）

### 推論環境
- [ ] 推論APIの実装完了
- [ ] レスポンス時間が要件を満たしている
- [ ] バッチ推論/リアルタイム推論の選択が適切
- [ ] エラーハンドリングの実装
- [ ] ログ出力の設定

### インフラ・スケーラビリティ
- [ ] 予想されるトラフィックに対応できる
- [ ] オートスケーリングの設定
- [ ] ロードバランシングの設定
- [ ] リソース使用量（CPU、メモリ、GPU）の見積もり
- [ ] コスト試算の完了

### セキュリティ
- [ ] 入力バリデーションの実装
- [ ] 認証・認可の設定
- [ ] データの暗号化（転送時・保管時）
- [ ] API rate limitingの設定
- [ ] セキュリティ脆弱性のスキャン

### モニタリング・アラート
- [ ] モデル性能のモニタリング設定
- [ ] データドリフトの検出設定
- [ ] システムメトリクス（レイテンシ、スループット）の監視
- [ ] アラート設定（性能劣化、エラー率上昇など）
- [ ] ログの集約と分析

### ドキュメント
- [ ] APIドキュメントの作成
- [ ] モデルカード/モデル説明書の作成
- [ ] 運用マニュアルの作成
- [ ] ロールバック手順の文書化
- [ ] トラブルシューティングガイド

### テスト
- [ ] 単体テストの実装
- [ ] 統合テストの実装
- [ ] 負荷テストの実施
- [ ] A/Bテスト計画の策定
- [ ] カナリアデプロイ/ブルーグリーンデプロイの準備
```

### 2. モデル保存とロード

```python
import joblib
import json
from datetime import datetime
from pathlib import Path

class ModelArtifact:
    """モデルと関連情報を保存・ロードするクラス"""

    def __init__(self, model, metadata=None):
        self.model = model
        self.metadata = metadata or {}

    def save(self, output_dir):
        """モデルと メタデータを保存"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # モデルの保存
        model_path = output_dir / 'model.pkl'
        joblib.dump(self.model, model_path)

        # メタデータの保存
        self.metadata.update({
            'saved_at': datetime.now().isoformat(),
            'model_path': str(model_path),
        })

        metadata_path = output_dir / 'metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)

        print(f"モデルを {output_dir} に保存しました")

        return output_dir

    @classmethod
    def load(cls, model_dir):
        """モデルとメタデータをロード"""
        model_dir = Path(model_dir)

        # モデルのロード
        model_path = model_dir / 'model.pkl'
        model = joblib.load(model_path)

        # メタデータのロード
        metadata_path = model_dir / 'metadata.json'
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        return cls(model, metadata)

# 使用例
metadata = {
    'model_type': 'RandomForest',
    'accuracy': 0.95,
    'training_date': '2025-01-15',
    'features': ['feature1', 'feature2', 'feature3'],
}

artifact = ModelArtifact(model, metadata)
artifact.save('models/production/v1.0.0')
```

### 3. 推論APIの実装（FastAPI）

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import numpy as np
from typing import List, Dict, Any
import logging

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# アプリケーション初期化
app = FastAPI(title="ML Model API", version="1.0.0")

# モデルのロード
model_artifact = ModelArtifact.load('models/production/v1.0.0')
model = model_artifact.model
metadata = model_artifact.metadata

# リクエスト/レスポンスのスキーマ
class PredictionRequest(BaseModel):
    features: List[float]

    @validator('features')
    def validate_features(cls, v):
        expected_n_features = len(metadata['features'])
        if len(v) != expected_n_features:
            raise ValueError(
                f"Expected {expected_n_features} features, got {len(v)}"
            )
        return v

class PredictionResponse(BaseModel):
    prediction: float
    probability: float = None
    model_version: str
    timestamp: str

# ヘルスチェック
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_version": metadata.get('model_version', 'unknown'),
        "model_type": metadata.get('model_type', 'unknown')
    }

# モデル情報
@app.get("/model/info")
async def model_info():
    return metadata

# 推論エンドポイント
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        # 入力データの準備
        features = np.array(request.features).reshape(1, -1)

        # 推論
        prediction = model.predict(features)[0]

        # 確率（分類モデルの場合）
        probability = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(features)[0]
            probability = float(proba.max())

        logger.info(f"Prediction: {prediction}, Probability: {probability}")

        return PredictionResponse(
            prediction=float(prediction),
            probability=probability,
            model_version=metadata.get('model_version', '1.0.0'),
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# バッチ推論
@app.post("/predict/batch")
async def predict_batch(requests: List[PredictionRequest]):
    try:
        features_list = [np.array(req.features) for req in requests]
        features_array = np.vstack(features_list)

        predictions = model.predict(features_array)

        results = [
            {
                "prediction": float(pred),
                "model_version": metadata.get('model_version', '1.0.0')
            }
            for pred in predictions
        ]

        return {"predictions": results, "count": len(results)}

    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# アプリケーションの起動
# uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### 4. モニタリングの実装

```python
import time
from functools import wraps
from collections import defaultdict
import prometheus_client as prom

# Prometheusメトリクス
PREDICTION_COUNTER = prom.Counter(
    'ml_predictions_total',
    'Total number of predictions',
    ['model_version', 'status']
)

PREDICTION_LATENCY = prom.Histogram(
    'ml_prediction_latency_seconds',
    'Prediction latency in seconds',
    ['model_version']
)

PREDICTION_VALUE = prom.Histogram(
    'ml_prediction_value',
    'Distribution of prediction values',
    ['model_version']
)

def monitor_prediction(func):
    """推論をモニタリングするデコレータ"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        model_version = metadata.get('model_version', '1.0.0')

        try:
            # 推論実行
            result = await func(*args, **kwargs)

            # メトリクスの記録
            latency = time.time() - start_time
            PREDICTION_LATENCY.labels(model_version=model_version).observe(latency)
            PREDICTION_COUNTER.labels(
                model_version=model_version,
                status='success'
            ).inc()

            if hasattr(result, 'prediction'):
                PREDICTION_VALUE.labels(
                    model_version=model_version
                ).observe(result.prediction)

            return result

        except Exception as e:
            PREDICTION_COUNTER.labels(
                model_version=model_version,
                status='error'
            ).inc()
            raise

    return wrapper

# メトリクスエンドポイント
@app.get("/metrics")
async def metrics():
    return prom.generate_latest()
```

### 5. データドリフト検出

```python
from scipy import stats
import pandas as pd

class DriftDetector:
    """データドリフトを検出するクラス"""

    def __init__(self, reference_data):
        """
        Parameters:
        -----------
        reference_data : pd.DataFrame
            参照データ（学習時のデータ）
        """
        self.reference_data = reference_data
        self.reference_stats = self._compute_stats(reference_data)

    def _compute_stats(self, data):
        """データの統計量を計算"""
        stats_dict = {}
        for col in data.columns:
            if data[col].dtype in ['int64', 'float64']:
                stats_dict[col] = {
                    'mean': data[col].mean(),
                    'std': data[col].std(),
                    'min': data[col].min(),
                    'max': data[col].max(),
                }
        return stats_dict

    def detect_drift(self, new_data, threshold=0.05):
        """
        Kolmogorov-Smirnov検定でドリフトを検出

        Parameters:
        -----------
        new_data : pd.DataFrame
            新しいデータ
        threshold : float
            有意水準（デフォルト: 0.05）

        Returns:
        --------
        dict : ドリフトが検出された列とp値
        """
        drift_results = {}

        for col in self.reference_data.columns:
            if col not in new_data.columns:
                continue

            if self.reference_data[col].dtype in ['int64', 'float64']:
                # KS検定
                statistic, p_value = stats.ks_2samp(
                    self.reference_data[col].dropna(),
                    new_data[col].dropna()
                )

                if p_value < threshold:
                    drift_results[col] = {
                        'p_value': p_value,
                        'statistic': statistic,
                        'drift_detected': True
                    }

        return drift_results

# 使用例
# drift_detector = DriftDetector(training_data)
# drift_results = drift_detector.detect_drift(production_data)
```

### 6. テストコード

```python
import pytest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_check():
    """ヘルスチェックのテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_prediction():
    """推論のテスト"""
    # 正常なリクエスト
    request_data = {
        "features": [1.0, 2.0, 3.0, 4.0]
    }
    response = client.post("/predict", json=request_data)
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_invalid_features():
    """不正な入力のテスト"""
    # 特徴量の数が違う
    request_data = {
        "features": [1.0, 2.0]  # 足りない
    }
    response = client.post("/predict", json=request_data)
    assert response.status_code == 422  # Validation Error

def test_prediction_latency():
    """レイテンシのテスト"""
    import time

    request_data = {
        "features": [1.0, 2.0, 3.0, 4.0]
    }

    start = time.time()
    response = client.post("/predict", json=request_data)
    latency = time.time() - start

    assert response.status_code == 200
    assert latency < 1.0  # 1秒以内
```

### 7. Docker化

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコピー
COPY . .

# ポートの公開
EXPOSE 8000

# アプリケーションの起動
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=/app/models/production/v1.0.0
    volumes:
      - ./models:/app/models
    restart: unless-stopped

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    restart: unless-stopped

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    restart: unless-stopped
```

## Best Practices

1. **段階的デプロイ**: カナリアリリースやブルーグリーンデプロイメントを活用
2. **モニタリング**: 本番投入直後は特に注意深く監視
3. **ロールバック計画**: 問題発生時に即座に戻せる準備
4. **ドキュメント**: すべての手順を文書化
5. **自動化**: CI/CDパイプラインで自動テスト・デプロイ

## Examples

### Example 1: AWS SageMakerへのデプロイ

```python
import sagemaker
from sagemaker.sklearn import SKLearnModel

# モデルのアップロード
model = SKLearnModel(
    model_data='s3://bucket/model.tar.gz',
    role=role,
    entry_point='inference.py',
    framework_version='1.0-1'
)

# エンドポイントのデプロイ
predictor = model.deploy(
    instance_type='ml.m5.large',
    initial_instance_count=1,
    endpoint_name='my-ml-endpoint'
)
```

### Example 2: ローカルでのテスト実行

```bash
# APIサーバーの起動
uvicorn api:app --reload

# 別のターミナルでテスト
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0, 4.0]}'
```

## Notes

- **コスト管理**: リソースの無駄遣いを避ける
- **セキュリティ**: 本番環境では必ず認証を設定
- **法令遵守**: GDPR、個人情報保護法などを考慮
- **継続的改善**: デプロイ後もモデルの再学習と更新を計画
