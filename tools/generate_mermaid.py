"""
Mermaid 다이어그램을 PNG 이미지로 변환하는 도구.

사용법:
    python generate_mermaid.py --input diagram.mmd --output output.png
    python generate_mermaid.py --code "graph TD; A-->B;" --output output.png

필요 패키지:
    pip install requests

Mermaid.ink API를 사용하여 서버 설치 없이 이미지를 생성합니다.
"""

import argparse
import base64
import sys
import urllib.request
import urllib.error


def mermaid_to_png(mermaid_code: str, output_path: str) -> None:
    """Mermaid 코드를 PNG 이미지로 변환하여 저장한다."""
    encoded = base64.urlsafe_b64encode(mermaid_code.encode("utf-8")).decode("ascii")
    url = f"https://mermaid.ink/img/{encoded}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as response:
            image_data = response.read()

        with open(output_path, "wb") as f:
            f.write(image_data)

        print(f"이미지 저장 완료: {output_path}")
    except urllib.error.URLError as e:
        print(f"이미지 생성 실패: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Mermaid 다이어그램을 PNG로 변환")
    parser.add_argument("--input", "-i", help="Mermaid 코드가 담긴 .mmd 파일 경로")
    parser.add_argument("--code", "-c", help="Mermaid 코드 문자열 (직접 입력)")
    parser.add_argument("--output", "-o", required=True, help="출력 PNG 파일 경로")

    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            mermaid_code = f.read()
    elif args.code:
        mermaid_code = args.code
    else:
        print("--input 또는 --code 중 하나를 지정해야 합니다.", file=sys.stderr)
        sys.exit(1)

    mermaid_to_png(mermaid_code, args.output)


if __name__ == "__main__":
    main()
