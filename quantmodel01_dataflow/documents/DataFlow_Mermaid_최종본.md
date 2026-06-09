# DataFlow Mermaid 최종본

## 1. 공식 학습·백테스트 흐름

```mermaid
flowchart TD
    A[삼성전자·KOSPI·Bitcoin<br/>주봉 OHLCV 수집] --> B[날짜 정렬·결측 확인<br/>워밍업 확보]
    B --> C[세 자산 가격 feature 생성<br/>현재 종가 + 로그수익률 lag1~5]
    B --> D[삼성전자 기술지표 계산<br/>ATR_10 · MFI_10 · STOCHk_10_3_3]
    D --> E[통제변수 생성<br/>RET · MOM · VOL]
    E --> F[삼성전자 OLS residual 생성]
    F --> F1[ATR_10_res]
    F --> F2[MFI_10_res]
    F --> F3[STOCHk_10_3_3_res]
    F1 --> G[StandardScaler]
    F2 --> G
    F3 --> G
    G --> H[PCA]
    H --> I[Investor_Sentiment_PC1]
    C --> J[실험별 최종 데이터셋]
    F1 --> J
    F2 --> J
    F3 --> J
    I --> J
    J --> K[Target_Log_Return<br/>다음 주 삼성전자 로그수익률]
    K --> L[시간순 학습·테스트 분할]
    L --> M[XGBoost 회귀 학습]
    M --> N1[실험 1<br/>Price-only · B · C · D]
    M --> N2[실험 2<br/>A-1 · A-2 · A-3]
    M --> N3[실험 3<br/>KOSPI-only · Price-only]
    N1 --> O[58주 전체·5개 기간 백테스트]
    N2 --> O
    N3 --> O
    O --> P[R² · RMSE · MAE · DA]
    P --> Q[공식 결과 CSV 저장]
```

## 2. 최신 데이터 기반 최근 1회 예측 흐름

```mermaid
flowchart TD
    A[Streamlit 모델링·검증 탭] --> B[저장 Model B·C·D 선택]
    B --> C[QuantPredictor 로드]
    C --> D[최신 삼성전자·KOSPI·Bitcoin<br/>주봉 수집]
    D --> E[삼성전자 기술지표·RET·MOM·VOL]
    E --> F[삼성전자 residual 3개]
    F --> G[저장 scaler.pkl 적용]
    G --> H[저장 pca.pkl 적용]
    H --> I[Investor_Sentiment_PC1]
    D --> J[세 자산 종가·lag1~5 생성]
    J --> K[삼성전자 기준일에 정렬]
    I --> L[최신 feature frame]
    K --> L
    L --> M[model.feature_names_in_ 기준 정렬]
    M --> N[XGBoost 연속형 로그수익률 예측]
    N --> O{pred_log_return > 0?}
    O -- 예 --> P[UP]
    O -- 아니오 --> Q[DOWN]
    P --> R[최근 1회 결과 표출]
    Q --> R
```

## 사용 원칙
- 공식 A-1~D 성능은 확정 CSV로 표시합니다.
- 최근 1회 예측은 실제 저장된 B/C/D pkl만 선택합니다.
- residual은 삼성전자에서만 생성합니다.
- 모델은 확률 분류기가 아니라 로그수익률 회귀모델입니다.
