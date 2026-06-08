from pathlib import Path

import streamlit as st


def render_process_flow() -> None:
    """프로젝트의 데이터 처리와 실험 흐름을 표시한다."""
    st.header("프로세스 흐름")

    st.markdown(
        """
1. **주봉 시장자료 수집**  
   삼성전자·KOSPI·Bitcoin의 주봉 가격 데이터를 수집합니다.

2. **공통 가격 feature 생성**  
   각 자산의 현재 주봉 종가와 과거 1~5주 로그수익률을 생성합니다.

3. **삼성전자 기술지표 계산**  
   ATR·MFI·Stochastic을 계산합니다.

4. **가격요인 통제 및 residual 생성**  
   RET·MOM·VOL을 통제하여 기술지표별 residual 3개를 생성합니다.

5. **통합 심리 proxy 생성**  
   residual 3개를 표준화한 뒤 PCA를 적용하여 PC1을 생성합니다.

6. **실험 1 · 심리 proxy 구성 비교**  
   Price-only와 Model B/C/D를 비교합니다.

7. **실험 2 · 개별 residual 기여도 검증**  
   동일한 가격 feature 18개에 residual을 하나씩 추가한  
   Model A-1/A-2/A-3을 비교합니다.

8. **실험 3 · Bitcoin 보조 입력 효과 검증**  
   삼성전자·KOSPI만 사용한 KOSPI-only Baseline과  
   Bitcoin까지 포함한 Price-only를 비교합니다.

9. **전체 및 기간별 성능 평가**  
   동일한 58주 테스트 구간과 5개 세부 기간에서  
   R²·RMSE·MAE·방향 정확도를 평가합니다.

10. **저장 모델 최근 1회 예측**  
    저장된 pkl 모델 B/C/D로 삼성전자 다음 주  
    로그수익률 방향을 예측합니다.
        """
    )

    st.caption(
        "공식 백테스트 성능은 최신 CSV를 기준으로 표시하고, "
        "최근 1회 예측은 저장된 pkl 모델과 현재 수집 데이터를 이용해 별도로 실행합니다."
    )


def log_process_flow(
    path: str = "process_flow.md",
) -> None:
    """현재 프로세스 흐름을 Markdown 파일로 저장한다."""
    content = (
        "# 프로세스 흐름\n\n"
        "1. 삼성전자·KOSPI·Bitcoin 주봉 가격 데이터 수집\n"
        "2. 현재 종가와 과거 1~5주 로그수익률 생성\n"
        "3. 삼성전자 ATR·MFI·Stochastic 계산\n"
        "4. RET·MOM·VOL 통제 후 residual 3개 생성\n"
        "5. residual 표준화 후 PCA 기반 PC1 생성\n"
        "6. 실험 1: Price-only와 Model B/C/D 비교\n"
        "7. 실험 2: Model A-1/A-2/A-3 비교\n"
        "8. 실험 3: KOSPI-only와 KOSPI+Bitcoin 비교\n"
        "9. 58주 전체 및 5개 기간별 성능 평가\n"
        "10. 저장 pkl 모델 B/C/D의 최근 1회 예측\n"
    )

    Path(path).write_text(
        content,
        encoding="utf-8",
    )

