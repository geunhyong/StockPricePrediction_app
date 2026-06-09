from log.introduction import render_introduction
from log.process_flow import render_process_flow
from tabs import data_preprocessing, modeling_validation, sentiment_proxy
from log.process_flow import render_process_flow
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import streamlit as st

# 1. 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, 'fonts', 'MALGUN.TTF')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'stock_data.csv')

# 2. 폰트 설정 함수 정의
def setup_environment():
    try:
        if os.path.exists(FONT_PATH):
            fm.fontManager.addfont(FONT_PATH)
            plt.rcParams['font.family'] = 'Malgun Gothic'
        else:
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = ['NanumGothic', 'DejaVu Sans']
    except Exception as e:
        st.warning(f"폰트 설정 오류: {e}")
    plt.rcParams['axes.unicode_minus'] = False


# 3. 함수 실행 (들여쓰기 없이 맨 앞에 위치해야 함)
setup_environment()


# =========================================================
# 프로젝트 공통 설정
# =========================================================

APP_TITLE = "투자자 심리지수 기반 주가 예측 대시보드"
    
PREDICTION_TARGET = "삼성전자"

DATA_ASSETS = [
    "삼성전자",
    "코스피",
    "비트코인",
]


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 공통 세션 상태
# =========================================================
def initialize_session_state() -> None:
    """
    대시보드 전체에서 공유하는 기본 session_state를 설정한다.

    데이터 전처리 탭에서는 삼성전자·코스피·비트코인을 선택할 수 있고,
    심리지표 및 모델링/검증 탭의 분석 대상은 삼성전자로 고정한다.
    """
    if "asset_name" not in st.session_state:
        st.session_state.asset_name = PREDICTION_TARGET

    st.session_state.prediction_target = PREDICTION_TARGET

    if "raw_data_by_asset" not in st.session_state:
        st.session_state.raw_data_by_asset = {}

    if "sentiment_data_by_asset" not in st.session_state:
        st.session_state.sentiment_data_by_asset = {}

    if "explained_variance_by_asset" not in st.session_state:
        st.session_state.explained_variance_by_asset = {}


# =========================================================
# 사이드바
# =========================================================
def render_default_sidebar() -> None:
    """
     데이터 전처리 탭에서만 사용하는 자산 선택 사이드바입니다.
    """
    st.sidebar.header("주봉 데이터 준비")

    asset_name = st.sidebar.selectbox(
        "불러올 주봉 데이터",
        options=DATA_ASSETS,
        key="sidebar_asset_name",
    )

    st.session_state.asset_name = asset_name

    st.sidebar.caption(
        "선택한 자산의 주봉 데이터와 "
        "기술지표 계산 결과를 확인합니다."
    )

def render_overview_sidebar() -> None:
    """
    프로젝트 소개 탭에서 사용하는 고정 안내 사이드바입니다.

    자산 선택 기능은 제공하지 않고,
    프로젝트의 최종 예측 대상과 외생 보조 입력만 안내합니다.
    """
    st.session_state.asset_name = PREDICTION_TARGET

    st.sidebar.header("프로젝트 안내")

    st.sidebar.markdown("**최종 예측 대상**")
    st.sidebar.markdown("### 삼성전자")

    st.sidebar.markdown("**외생 보조 입력**")
    st.sidebar.write("KOSPI · Bitcoin")

    st.sidebar.caption(
        "프로젝트 소개 탭에서는 연구 목적과 "
        "실험 1·2·3의 전체 구조를 설명합니다."
    )
    
def render_dataflow_sidebar() -> None:
    """DataFlow 탭 전용 사이드바를 표시한다."""
    st.session_state.asset_name = PREDICTION_TARGET

    st.sidebar.header("DataFlow")

    st.sidebar.metric(
        "최종 예측 대상",
        "삼성전자",
    )

    st.sidebar.markdown("**외생 보조 입력**")
    st.sidebar.write("KOSPI · Bitcoin")

    st.sidebar.markdown("**예측 방식**")
    st.sidebar.write(
        "XGBoost 회귀 → 로그수익률 예측 → 부호로 방향 평가"
    )

    st.sidebar.markdown("**파이프라인 구조**")
    st.sidebar.write(
        "수집 → 저장 → Feature → 심리 proxy → "
        "학습 → 백테스트 → 표출"
    )

    st.sidebar.caption(
        "공식 백테스트와 최신 데이터 기반 최근 1회 예측을 "
        "분리한 부분 자동화 구조입니다."
    )
    
def render_sentiment_sidebar() -> None:
    """
    심리지표 탭에서 사용하는 삼성전자 고정 사이드바입니다.
    """
    st.session_state.asset_name = PREDICTION_TARGET

    st.sidebar.header("주봉 데이터 준비")
    st.sidebar.markdown("**분석 대상**")
    st.sidebar.markdown("### 삼성전자")

    st.sidebar.caption(
        "심리지표 탭에서는 삼성전자 주봉 데이터를 기준으로 "
        "ATR·MFI·Stochastic residual과 PC1을 확인합니다."
    )


def render_modeling_sidebar() -> None:
    """
    모델링/검증 탭에서 사용하는 고정 안내 사이드바입니다.
    """
    st.session_state.asset_name = PREDICTION_TARGET

    st.sidebar.header("분석 대상")

    st.sidebar.markdown("**최종 예측 대상**")
    st.sidebar.markdown("### 삼성전자")

    st.sidebar.markdown("**시장 보조 입력**")
    st.sidebar.write("KOSPI · Bitcoin")

    st.sidebar.caption(
        "삼성전자의 다음 주 로그수익률 방향을 예측하며, "
        "KOSPI와 Bitcoin은 시장 흐름을 반영하는 "
        "보조 입력자료로 사용합니다."
    )


# =========================================================
# 대시보드 상단
# =========================================================
def render_dashboard_header() -> None:
    """
    프로젝트의 목적을 간결하게 소개한다.
    """
    st.title(APP_TITLE)

    st.caption(
        "시장 데이터와 심리 proxy를 활용한 "
        "삼성전자 다음 주 로그수익률 방향 예측"
    )

    st.info(
        "본 프로젝트는 삼성전자를 최종 예측 대상으로 설정합니다. "
        "KOSPI와 Bitcoin의 주봉 데이터는 삼성전자 방향 예측을 위한 "
        "시장학습 보조자료로 사용합니다."
    )


# =========================================================
# 프로젝트 소개 탭의 실험 구성
# =========================================================

def render_experiment_summary() -> None:
    """
    프로젝트 소개 탭에서 최종 실험 구조를 요약한다.
    """
    st.subheader("최종 실험 구성")

    st.markdown(
        """
### 실험 1 · 심리 proxy 구성 비교

삼성전자·KOSPI·Bitcoin의 현재 주봉 종가 3개와  
각 자산의 과거 1~5주 로그수익률 15개를 합친  
공통 가격 feature 18개를 사용합니다.

- **Price-only**: 공통 가격 feature 18개
- **Model B**: 공통 가격 feature + PC1
- **Model C**: 공통 가격 feature + residual 3개
- **Model D**: 공통 가격 feature + PC1 + residual 3개

### 실험 2 · 개별 residual 기여도 검증

실험 1과 동일한 공통 가격 feature 18개에  
residual을 하나씩만 추가합니다.

- **Model A-1**: ATR residual 추가
- **Model A-2**: MFI residual 추가
- **Model A-3**: Stochastic residual 추가

### 실험 3 · Bitcoin 보조 입력 효과 검증

- **KOSPI-only Baseline**: 삼성전자·KOSPI의 현재 종가 2개와  
  두 자산의 과거 1~5주 로그수익률 10개, 총 12개
- **Price-only**: 삼성전자·KOSPI·Bitcoin의 현재 종가 3개와  
  세 자산의 과거 1~5주 로그수익률 15개, 총 18개

Bitcoin 관련 feature 6개를 추가했을 때  
삼성전자 다음 주 방향 예측 성능이 달라지는지 확인합니다.
        """
    )

    st.caption(
        "모든 실험은 삼성전자 다음 주 로그수익률 방향을 예측하며, "
        "동일한 58주 테스트 구간에서 Directional Accuracy를 중심으로 비교합니다."
    )




# =========================================================
# 메인 화면
# =========================================================
def main() -> None:
    initialize_session_state()
    render_dashboard_header()

    overview_tab, dataflow_tab, data_tab, sentiment_tab, modeling_tab = st.tabs(
        [
            "프로젝트 소개",
            "DataFlow",
            "데이터 전처리",
            "심리지표",
            "모델링/검증",
        ],
        key="dashboard_tabs",
        on_change="rerun",
    )

    
    if modeling_tab.open:
        render_modeling_sidebar()
    
    elif sentiment_tab.open:
        render_sentiment_sidebar()
    
    elif data_tab.open:
        render_default_sidebar()
    
    elif dataflow_tab.open:
        render_dataflow_sidebar()
    
    else:
        render_overview_sidebar()

    # -----------------------------------------------------
    # 프로젝트 소개
    # -----------------------------------------------------
    with overview_tab:
        render_introduction()

        st.markdown(
            "<div style='height: 24px;'></div>",
            unsafe_allow_html=True,
        )

        render_experiment_summary()
    
    with dataflow_tab:
        render_process_flow()
    
    # -----------------------------------------------------
    # 데이터 전처리
    # -----------------------------------------------------
    with data_tab:
        data_preprocessing.run()

    # -----------------------------------------------------
    # 심리지표
    # -----------------------------------------------------
    with sentiment_tab:
        sentiment_proxy.run()

    # -----------------------------------------------------
    # 모델링 / 검증
    # -----------------------------------------------------
    with modeling_tab:
        modeling_validation.run()


if __name__ == "__main__":
    main()
