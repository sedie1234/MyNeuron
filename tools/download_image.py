"""
URL에서 이미지를 다운로드하여 neuron/images/에 저장하는 도구.

사용법:
    python download_image.py --url "https://example.com/image.png" --name "transformer_architecture_01.png"

이미지는 기본적으로 neuron/images/에 저장됩니다.
--output 옵션으로 다른 경로를 지정할 수 있습니다.
"""

import argparse
import os
import sys
import urllib.request
import urllib.error


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_IMAGE_DIR = os.path.join(SCRIPT_DIR, "..", "neuron", "images")


def download_image(url: str, output_path: str) -> None:
    """URL에서 이미지를 다운로드하여 저장한다."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "MyNeuron-ImageDownloader/1.0"},
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            image_data = response.read()

        with open(output_path, "wb") as f:
            f.write(image_data)

        print(f"이미지 저장 완료: {output_path}")
    except urllib.error.URLError as e:
        print(f"다운로드 실패: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="URL에서 이미지 다운로드")
    parser.add_argument("--url", "-u", required=True, help="이미지 URL")
    parser.add_argument("--name", "-n", required=True, help="저장할 파일명 (예: transformer_arch_01.png)")
    parser.add_argument("--output", "-o", help="저장 디렉토리 (기본: neuron/images/)")

    args = parser.parse_args()

    output_dir = args.output or DEFAULT_IMAGE_DIR
    output_path = os.path.join(output_dir, args.name)

    download_image(args.url, output_path)


if __name__ == "__main__":
    main()
