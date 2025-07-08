import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict


@dataclass
class LyricData:
    title: str
    song_form: List[str]
    lyric_dict: Dict[str, List[str]]


def load_round(round_path: Path) -> List[LyricData]:
    lyric_data_list: List[LyricData] = []

    lyric_file_list: List[Path] = list(round_path.glob("*.json"))
    sorted_lyric_file_list: List[Path] = sorted(lyric_file_list, key=lambda x: x.name)

    for lyric_file in sorted_lyric_file_list:  # type: Path
        with open(lyric_file, "r", encoding="utf8") as lf:
            lyric_json: dict = json.load(lf)

        title: str = lyric_json.get("title")
        song_form: List[str] = lyric_json.get("song_form")
        lyric_dict: Dict[str, List[str]] = lyric_json.get("lyric")

        lyric_data: LyricData = LyricData(
            title=title,
            song_form=song_form,
            lyric_dict=lyric_dict,
        )

        lyric_data_list.append(lyric_data)

    return lyric_data_list
