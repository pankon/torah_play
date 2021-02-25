import os

import requests

from src.letter import Letter


def parse(raw: requests.Response):
    lines = raw.text.split("\n")
    idx = 0
    length = len(lines)
    out = []

    print(lines[idx])

    # skip preamble
    while idx < length and not lines[idx].startswith("Chapter"):
        idx += 1

    idx += 2

    while idx < length:
        while idx < length and not lines[idx].startswith("Chapter"):
            current = ''.join(''.join(char for char in word if char in Letter.all_letters) for word in lines[idx].split(" "))
            out.append(current)
            idx += 1

        idx += 2

    return ''.join(out)


def download(book: str):
    url = "https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/txt/Tanakh/Torah/{}/Hebrew/Tanach%20with%20Text%20Only.txt".format(book)
    return requests.get(url)

def download_all() -> list:
    #goyish names
    books = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]

    out = []

    for book in books:
        raw = download(book)
        out.append(parse(raw))

    return out

def download_all_to_file(filename: str):
    if os.path.exists(filename):
        print("already exists:", filename)
        return

    with open(filename, "w", encoding="utf-8") as fp:
        for data in download_all():
            fp.write(data)

if __name__ == "__main__":
    download_all_to_file("data/torah.txt")
