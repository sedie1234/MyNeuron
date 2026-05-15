"""
5대 기본맛의 농도-쾌감 반응 곡선을 시각화하는 도구.

문헌 데이터(Yamaguchi, Stevens' power law, Bartoshuk 등)를 기반으로
감칠맛의 plateau 특성과 다른 맛의 피크-감쇠 패턴을 비교.

출력: neuron/images/taste_hedonic_curves.png
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def setup_korean_font():
    """Windows 표준 한글 폰트 설정."""
    candidates = ["Malgun Gothic", "Nanum Gothic", "AppleGothic", "Noto Sans CJK KR"]
    available = {f.name for f in fm.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False


def asymmetric_bell(x_log, peak_log, sigma_left, sigma_right, amplitude=100):
    """피크 좌우 폭이 다른 비대칭 종형 곡선."""
    return np.where(
        x_log < peak_log,
        amplitude * np.exp(-((x_log - peak_log) / sigma_left) ** 2 / 2),
        amplitude * np.exp(-((x_log - peak_log) / sigma_right) ** 2 / 2),
    )


def main():
    setup_korean_font()

    # x축: 검지역치 대비 배수 (로그 스케일)
    x = np.logspace(-1, 2.7, 400)
    xl = np.log(x)

    # 각 맛의 hedonic 곡선
    sweet = asymmetric_bell(xl, np.log(30), 1.3, 1.0, amplitude=95)
    salty = asymmetric_bell(xl, np.log(20), 1.0, 0.55, amplitude=90) - 20 * np.maximum(
        0, xl - np.log(80)
    )
    sour = asymmetric_bell(xl, np.log(10), 0.7, 0.55, amplitude=75) - 25 * np.maximum(
        0, xl - np.log(60)
    )
    bitter = -30 * np.log(x + 0.2) + 10
    bitter = np.clip(bitter, -60, 10)

    # 감칠맛: 빠른 상승 + 완만한 plateau + 매우 느린 감쇠
    umami_rise = 90 / (1 + np.exp(-1.8 * (xl - np.log(10))))
    umami_decline = np.where(x > 80, -8 * (xl - np.log(80)), 0)
    umami = umami_rise + umami_decline

    # 플롯
    fig, ax = plt.subplots(figsize=(11, 6.5))

    styles = [
        ("단맛 (Sweet)", sweet, "#E91E63", "-"),
        ("짠맛 (Salty)", salty, "#2196F3", "-"),
        ("신맛 (Sour)", sour, "#689F38", "-"),
        ("쓴맛 (Bitter)", bitter, "#6D4C41", "-"),
        ("감칠맛 (Umami)", umami, "#FB8C00", "-"),
    ]
    for label, y, color, linestyle in styles:
        ax.plot(x, y, label=label, linewidth=2.8, color=color, linestyle=linestyle)

    ax.set_xscale("log")
    ax.axhline(0, color="gray", linewidth=0.7, linestyle="--", alpha=0.7)
    ax.axvline(1, color="gray", linewidth=0.7, linestyle=":", alpha=0.5)
    ax.text(
        1.05,
        -55,
        "검지역치",
        fontsize=9,
        color="gray",
        rotation=90,
        va="bottom",
    )

    ax.set_xlabel("농도 (검지역치 대비 배수, 로그 스케일)", fontsize=12)
    ax.set_ylabel("쾌감 반응 (Hedonic Response, 상대값)", fontsize=12)
    ax.set_title(
        "5대 기본맛의 농도에 따른 쾌감 반응 곡선\n"
        "(문헌 데이터 기반 도식 — 실험 조건·개인차에 따라 변동)",
        fontsize=13,
        pad=15,
    )
    ax.set_ylim(-65, 110)
    ax.legend(loc="lower left", fontsize=11, framealpha=0.95)
    ax.grid(True, alpha=0.3, which="both")

    # 특징 레이블
    ax.annotate(
        "Plateau형\n(혐오 전환 약함)",
        xy=(100, 78),
        xytext=(180, 95),
        arrowprops=dict(arrowstyle="->", color="#FB8C00", lw=1.5),
        fontsize=10,
        color="#FB8C00",
        fontweight="bold",
        ha="center",
    )
    ax.annotate(
        "Cloying\n(급격 감쇠)",
        xy=(250, 25),
        xytext=(250, 65),
        arrowprops=dict(arrowstyle="->", color="#E91E63", lw=1.3),
        fontsize=9,
        color="#E91E63",
        ha="center",
    )
    ax.annotate(
        "고농도 강한\n혐오 전환",
        xy=(200, -15),
        xytext=(200, -45),
        arrowprops=dict(arrowstyle="->", color="#2196F3", lw=1.3),
        fontsize=9,
        color="#2196F3",
        ha="center",
    )
    ax.annotate(
        "쾌감 피크 부재",
        xy=(50, -50),
        xytext=(10, -60),
        arrowprops=dict(arrowstyle="->", color="#6D4C41", lw=1.3),
        fontsize=9,
        color="#6D4C41",
        ha="center",
    )

    plt.tight_layout()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(
        script_dir, "..", "neuron", "images", "taste_hedonic_curves.png"
    )
    output_path = os.path.normpath(output_path)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"이미지 저장 완료: {output_path}")


if __name__ == "__main__":
    main()
