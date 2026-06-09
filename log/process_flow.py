from pathlib import Path

import streamlit as st


# =========================================================
# 프로젝트 및 DataFlow 경로
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATAFLOW_DIR = PROJECT_ROOT / "quantmodel01_dataflow"
DATAFLOW_IMAGE_DIR = DATAFLOW_DIR / "images"
DATAFLOW_DOCUMENT_DIR = DATAFLOW_DIR / "documents"


# =========================================================
# DataFlow 이미지 경로
# =========================================================
TITLE_IMAGE = (
    DATAFLOW_IMAGE_DIR
    / "01_title.png"
)

FRAMEWORK_IMAGE = (
    DATAFLOW_IMAGE_DIR
    / "02_framework.png"
)

DATA_COLLECTION_IMAGE = (
    DATAFLOW_IMAGE_DIR
    / "03_data_collection.png"
)

PROXY_IMAGE = (
    DATAFLOW_IMAGE_DIR
    / "04_proxy_generation.png"
)

XGBOOST_IMAGE = (
    DATAFLOW_IMAGE_DIR
    / "05_xgboost_regression.png"
)

SIGN_IMAGE = (
    DATAFLOW_IMAGE_DIR
    / "06_sign_comparison.png"
)

DIRECTION_IMAGE = (
    DATAFLOW_IMAGE_DIR
    / "07_direction_accuracy.png"
)


# =========================================================
# DataFlow 문서 경로
# =========================================================
PLAN_DOCUMENT = (
    DATAFLOW_DOCUMENT_DIR
    / "투자자심리지수_주가예측_최종기획서_v2.docx"
)

DATAFLOW_DOCUMENT = (
    DATAFLOW_DOCUMENT_DIR
    / "DataFlow_탭_최종설명문_v2.docx"
)

MERMAID_DOCUMENT = (
    DATAFLOW_DOCUMENT_DIR
    / "DataFlow_Mermaid_최종본.md"
)

DOCUMENT_LIST = (
    DATAFLOW_DOCUMENT_DIR
    / "문서_정리_목록.md"
)


# =========================================================
# 화면에 표시할 이미지 순서
# =========================================================
DATAFLOW_SLIDES = [
    {
        "number": "01",
        "title": "모델 DataFlow 소개",
        "path": TITLE_IMAGE,
    },
    {
        "number": "02",
        "title": "가설 검증 중심의 연구 방법론",
        "path": FRAMEWORK_IMAGE,
    },
    {
        "number": "03",
        "title": "신뢰성 있는 원천 데이터 확보",
        "path": DATA_COLLECTION_IMAGE,
    },
    {
        "number": "04",
        "title": "Residual 추출 및 심리 proxy 생성",
        "path": PROXY_IMAGE,
    },
    {
        "number": "05",
        "title": "XGBoost 회귀모델 학습",
        "path": XGBOOST_IMAGE,
    },
    {
        "number": "06",
        "title": "예측값 부호 기반 방향 판정",
        "path": SIGN_IMAGE,
    },
    {
        "number": "07",
        "title": "공식 방향 정확도 비교",
        "path": DIRECTION_IMAGE,
    },
]


# =========================================================
# 다운로드 문서
# =========================================================
DOCUMENTS = [
    {
        "label": "최종 연구 기획서 다운로드",
        "path": PLAN_DOCUMENT,
        "mime": (
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
    },
    {
        "label": "DataFlow 최종 설명문 다운로드",
        "path": DATAFLOW_DOCUMENT,
        "mime": (
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
    },
    {
        "label": "DataFlow Mermaid 원문 다운로드",
        "path": MERMAID_DOCUMENT,
        "mime": "text/markdown",
    },
    {
        "label": "문서 정리 목록 다운로드",
        "path": DOCUMENT_LIST,
        "mime": "text/markdown",
    },
]


def _render_pipeline_summary() -> None:
    """
    DataFlow의 핵심 구조를 요약한다.
    """
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "예측 대상",
        "삼성전자",
    )

    col2.metric(
        "공통 가격 입력",
        "18개",
    )

    col3.metric(
        "공식 테스트",
        "58주",
    )

    col4.metric(
        "기간별 검증",
        "5개",
    )


def _render_core_definition() -> None:
    """
    연구 목적과 자동화 범위를 설명한다.
    """
    st.info(
        "본 연구는 삼성전자 다음 주 로그수익률을 연속형 값으로 예측하고, "
        "예측값과 실제값의 부호 일치 여부를 중심으로 방향 정확도를 평가합니다. "
        "투자심리와 주가의 인과관계를 증명하는 연구가 아니라, "
        "동일한 가격정보에 심리 proxy를 추가했을 때 "
        "추가 예측정보가 제공되는지를 검증하는 비교실험입니다."
    )

    st.warning(
        "공식 모델 학습과 백테스트 결과는 동일한 실험조건을 유지하기 위해 "
        "확정된 CSV와 pkl로 저장합니다. Streamlit 실행 시 모든 모델을 "
        "다시 학습하지 않으며, 저장된 Model B·C·D의 최근 1회 예측만 "
        "실행 시점의 최신 주봉 데이터로 별도 계산합니다."
    )


def _render_slide(
    number: str,
    title: str,
    image_path: Path,
) -> None:
    """
    DataFlow 소개 이미지를 순서대로 표시한다.
    """
    st.subheader(
        f"{number} · {title}"
    )

    if image_path.exists():
        st.image(
            str(image_path),
            use_container_width=True,
        )
    else:
        st.warning(
            "이미지 파일을 찾지 못했습니다: "
            f"{image_path.name}"
        )


def _render_dataflow_slides() -> None:
    """
    DataFlow 소개 이미지를 정해진 순서대로 렌더링한다.
    """
    st.divider()
    st.subheader("모델 처리과정 소개")

    st.caption(
        "아래 이미지는 데이터 수집부터 심리 proxy 생성, "
        "XGBoost 회귀 학습과 부호 기반 방향 평가까지의 "
        "전체 모델 흐름을 간단히 소개합니다. "
        "공식 실험 수치와 상세 결과는 모델링/검증 탭을 기준으로 확인합니다."
    )

    for slide in DATAFLOW_SLIDES:
        _render_slide(
            number=slide["number"],
            title=slide["title"],
            image_path=slide["path"],
        )

        st.markdown(
            "<div style='height: 32px;'></div>",
            unsafe_allow_html=True,
        )


def _render_dual_flow() -> None:
    """
    공식 실험과 최신 예측 흐름을 분리해 설명한다.
    """
    st.divider()
    st.subheader("공식 실험과 최신 예측의 분리 구조")

    official_col, prediction_col = st.columns(2)

    with official_col:
        st.markdown("### 공식 실험·백테스트")

        st.info(
            """
**1. 주봉 데이터 준비**  
삼성전자·KOSPI·Bitcoin

**2. 가격·심리 feature 생성**  
가격 feature 18개, residual 3개, PC1

**3. 실험별 XGBoost 학습**  
실험 1·2·3 비교모델 구성

**4. 백테스트 검증**  
동일한 58주와 5개 세부 기간 평가

**5. 공식 산출물 저장**  
성능 CSV, 기간별 CSV, 저장 모델 pkl

**6. Streamlit 표출**  
확정 CSV를 정적으로 불러와 표시
            """
        )

    with prediction_col:
        st.markdown("### 최신 데이터 기반 최근 1회 예측")

        st.success(
            """
**1. 최신 주봉 수집**  
삼성전자·KOSPI·Bitcoin

**2. 가격 feature 재생성**  
현재 종가와 과거 1~5주 로그수익률

**3. 삼성전자 심리 proxy 재계산**  
residual 3개와 PC1 생성

**4. 저장 모델 선택**  
Model B·C·D 중 선택

**5. 연속형 로그수익률 예측**  
저장 XGBoost 회귀모델 사용

**6. 방향 판정**  
예측값의 부호로 상승·하락 표시
            """
        )


def _render_automation_scope() -> None:
    """
    현재 파이프라인의 자동화 수준을 표시한다.
    """
    st.divider()
    st.subheader("현재 자동화 범위")

    automation_data = [
        {
            "단계": "최신 주봉 수집",
            "자동화 수준": "버튼 실행",
            "Streamlit 동작": "불러오기·새로고침 시 실행",
        },
        {
            "단계": "CSV 캐시 저장",
            "자동화 수준": "자동",
            "Streamlit 동작": "수집 직후 저장",
        },
        {
            "단계": "가격 feature 생성",
            "자동화 수준": "자동",
            "Streamlit 동작": "최근 예측 실행 시 생성",
        },
        {
            "단계": "Residual·PC1 생성",
            "자동화 수준": "자동",
            "Streamlit 동작": "최근 예측 실행 시 생성",
        },
        {
            "단계": "공식 XGBoost 재학습",
            "자동화 수준": "수동",
            "Streamlit 동작": "대시보드에서 재학습하지 않음",
        },
        {
            "단계": "전체·기간별 백테스트",
            "자동화 수준": "확정 산출물",
            "Streamlit 동작": "실행 시 재계산하지 않음",
        },
        {
            "단계": "공식 결과 표출",
            "자동화 수준": "자동 로드",
            "Streamlit 동작": "확정 CSV를 읽어 표시",
        },
        {
            "단계": "최근 1회 예측",
            "자동화 수준": "버튼 실행",
            "Streamlit 동작": "최신 데이터와 저장 pkl 사용",
        },
    ]

    st.dataframe(
        automation_data,
        use_container_width=True,
        hide_index=True,
    )


def _render_document_downloads() -> None:
    """
    DataFlow 관련 문서를 다운로드할 수 있게 한다.
    """
    st.divider()
    st.subheader("연구 기획서 및 DataFlow 문서")

    existing_documents = [
        document
        for document in DOCUMENTS
        if document["path"].exists()
    ]

    if not existing_documents:
        st.warning(
            "다운로드할 DataFlow 문서를 찾지 못했습니다."
        )
        return

    columns = st.columns(2)

    for index, document in enumerate(existing_documents):
        path = document["path"]

        button_key = (
            "dataflow_document_download_"
            f"{index}_"
            f"{path.stem}"
        )

        with columns[index % 2]:
            st.download_button(
                label=document["label"],
                data=path.read_bytes(),
                file_name=path.name,
                mime=document["mime"],
                use_container_width=True,
                key=button_key,
            )


def render_process_flow() -> None:
    """
    DataFlow 독립 탭 전체 화면을 렌더링한다.
    """
    st.header("프로젝트 DataFlow")

    st.caption(
        "조원들이 작성한 모델 소개 이미지와 최종 연구 문서를 기준으로 "
        "데이터 수집부터 공식 백테스트 및 최신 예측까지의 "
        "처리 구조를 설명합니다."
    )

    _render_pipeline_summary()
    _render_core_definition()
    _render_dataflow_slides()
    _render_dual_flow()
    _render_automation_scope()
    _render_document_downloads()


def log_process_flow(
    path: str = "process_flow.md",
) -> None:
    """
    DataFlow 설명을 Markdown 파일로 저장한다.
    """
    content = (
        "# 프로젝트 DataFlow\n\n"
        "1. 삼성전자·KOSPI·Bitcoin 주봉 데이터 수집\n"
        "2. 날짜 정렬·결측치 확인·워밍업 구간 확보\n"
        "3. 현재 종가와 과거 1~5주 로그수익률 생성\n"
        "4. 삼성전자 ATR·MFI·Stochastic 계산\n"
        "5. RET·MOM·VOL 통제 후 residual 3개 생성\n"
        "6. StandardScaler와 PCA를 이용해 PC1 생성\n"
        "7. 실험 1·2·3 XGBoost 회귀모델 학습\n"
        "8. 동일한 58주와 5개 기간별 백테스트\n"
        "9. R²·RMSE·MAE·DA 평가\n"
        "10. 모델 pkl·Scaler·PCA·결과 CSV 저장\n"
        "11. Streamlit에서 확정 백테스트와 최신 1회 예측 표출\n\n"
        "본 시스템은 공식 백테스트와 최신 추론을 분리한 "
        "부분 자동화·재현 가능 분석 파이프라인이다.\n"
    )

    Path(path).write_text(
        content,
        encoding="utf-8",
    )
