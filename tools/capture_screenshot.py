"""
웹 페이지 스크린샷을 캡처하여 neuron/images/에 저장하는 도구.

사용법:
    python capture_screenshot.py --url "https://example.com" --name "example_page_01.png"

필요 패키지:
    pip install selenium webdriver-manager

Chrome 브라우저가 설치되어 있어야 합니다.
"""

import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_IMAGE_DIR = os.path.join(SCRIPT_DIR, "..", "neuron", "images")


def capture_screenshot(url: str, output_path: str, width: int = 1280, height: int = 720) -> None:
    """웹 페이지 스크린샷을 캡처하여 저장한다."""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
        print(
            "필요 패키지가 없습니다. 설치하세요:\n"
            "  pip install selenium webdriver-manager",
            file=sys.stderr,
        )
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        driver.implicitly_wait(3)
        driver.save_screenshot(output_path)
        print(f"스크린샷 저장 완료: {output_path}")
    finally:
        driver.quit()


def main():
    parser = argparse.ArgumentParser(description="웹 페이지 스크린샷 캡처")
    parser.add_argument("--url", "-u", required=True, help="캡처할 웹 페이지 URL")
    parser.add_argument("--name", "-n", required=True, help="저장할 파일명 (예: docs_page_01.png)")
    parser.add_argument("--output", "-o", help="저장 디렉토리 (기본: neuron/images/)")
    parser.add_argument("--width", "-w", type=int, default=1280, help="브라우저 너비 (기본: 1280)")
    parser.add_argument("--height", type=int, default=720, help="브라우저 높이 (기본: 720)")

    args = parser.parse_args()

    output_dir = args.output or DEFAULT_IMAGE_DIR
    output_path = os.path.join(output_dir, args.name)

    capture_screenshot(args.url, output_path, args.width, args.height)


if __name__ == "__main__":
    main()
