# coding: utf-8

import os
import argparse
from pathlib import Path

from pykakasi import kakasi


class StringConverter:
    def __init__(self):
        self.converter = self.setup_converter()

    @staticmethod
    def setup_converter():
        kakasi_ = kakasi()
        kakasi_.setMode('H', 'H')  # H(Hiragana) to a(roman)
        kakasi_.setMode('K', 'H')  # K(Katakana) to a(roman)
        kakasi_.setMode('J', 'H')  # J(Kanji) to a(roman)
        converter = kakasi_.getConverter()
        return converter

    def convert(self, text):
        return self.converter.do(text)


class FileNameObject:
    converter = StringConverter()

    def __init__(self, path):
        self.dirname = path.parent
        self.filename = path.name
        self.hira_name = self.converter.convert(self.filename)

    def new_name(self):
        if self.filename[0] == self.hira_name[0]:
            new_name = self.filename
        else:
            new_name = self.hira_name[0] + "_" + self.filename
        return os.path.join(self.dirname, new_name)


class FileRenamer:
    @staticmethod
    def run(input_path):
        for path in Path(input_path).glob("*"):
            new_name = FileNameObject(path).new_name()
            if str(path) != new_name:
                path.rename(new_name)
                print("変換しました：{}\t→\t{}".format(path, new_name))


def main():
    parser = argparse.ArgumentParser(
        description='指定されたフォルダに入っている漢字から始まるファイルの名前を、<ひらがな1文字>_<元ファイル名>に変換します。※念の為元ファイルはコピーを取っておいてください')
    parser.add_argument("input_path", help="変換したいファイルの入ったフォルダ名（絶対パス）")
    args = parser.parse_args()
    if not os.path.exists(args.input_path):
        raise RuntimeError("指定されたフォルダが存在しません")
    FileRenamer.run(args.input_path)


if __name__ == "__main__":
    main()
