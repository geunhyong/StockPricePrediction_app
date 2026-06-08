
import streamlit as st


def render_introduction() -> None:
    """프로젝트 소개 화면을 렌더링한다."""
    st.title(
        "🎯 Samsung Electronics Sentiment Analysis"
    )

    st.markdown(
        """
### 📊 프로젝트 개요

- **연구 목표**: 시장 가격정보로 설명되지 않는 투자자 반응을 심리 proxy로 구성하고, 삼성전자 다음 주 로그수익률 방향 예측에 추가 정보를 제공하는지 검증
- **최종 예측 대상**: 삼성전자
- **외생 보조 입력**: KOSPI, Bitcoin
- **분석 주기**: 주봉
- **평가 대상**: 삼성전자 다음 주 로그수익률의 상승·하락 방향

### 🔬 분석 도구

- **공통 가격 feature**: 현재 주봉 종가와 과거 1~5주 로그수익률
- **기술지표**: ATR_10, MFI_10, STOCHk_10_3_3
- **통제변수**: RET, MOM, VOL
- **개별 심리 proxy**: 통제변수로 설명되는 부분을 제거한 residual 3개
- **통합 심리 proxy**: residual 3개를 표준화한 뒤 PCA로 생성한 PC1
- **예측모델**: XGBoost
- **평가 지표**: R², RMSE, MAE, Directional Accuracy

### 🧪 실험 1 · 심리 proxy 구성 비교

삼성전자·KOSPI·Bitcoin의 현재 주봉 종가 3개와  
각 자산의 과거 1~5주 로그수익률 15개를 합친  
공통 가격 feature 18개를 사용합니다.

- **Price-only**: 공통 가격 feature 18개
- **Model B**: 공통 가격 feature + PC1
- **Model C**: 공통 가격 feature + residual 3개
- **Model D**: 공통 가격 feature + PC1 + residual 3개

### 🧪 실험 2 · 개별 residual 기여도 검증

실험 1과 동일한 공통 가격 feature 18개에  
residual을 하나씩만 추가합니다.

- **Model A-1**: 공통 가격 feature + ATR residual
- **Model A-2**: 공통 가격 feature + MFI residual
- **Model A-3**: 공통 가격 feature + Stochastic residual

### 🧪 실험 3 · Bitcoin 보조 입력 효과 검증

Bitcoin 관련 가격 feature 6개를 제외한 모델과  
Bitcoin까지 포함한 Price-only 모델을 비교합니다.

- **KOSPI-only Baseline**: 삼성전자·KOSPI 가격 feature 12개
- **Price-only**: 삼성전자·KOSPI·Bitcoin 가격 feature 18개

### 📈 현재 연결된 산출물

- **공식 심리 feature 산출물**: 삼성전자 107개 주봉
- **공식 전체 백테스트**: 동일한 58주 테스트 구간
- **공식 기간별 백테스트**: 5개 세부 기간
- **화면 표시 기준**: 프로젝트 루트의 최신 CSV 결과
- **최근 1회 예측**: 저장된 pkl 모델 B/C/D를 별도로 사용
        """
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Sentiment Rows",
        "107",
    )

    col2.metric(
        "Test Weeks",
        "58",
    )

    col3.metric(
        "Compared Rows",
        "10",
    )

    st.caption(
        "Compared Rows 10개는 Zero-return·Train-mean의 단순 기준선 2개와, "
        "KOSPI-only·Price-only·Model A-1~D의 실험 결과 8개를 합친 수입니다."
    )

