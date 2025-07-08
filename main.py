from pathlib import Path
from typing import List, Dict

from common.lyric import load_round, LyricData
from common.presentation import SinglePresentation

if __name__ == "__main__":
    pptx_path: Path = Path(
        "C:\\kyu_universe\\dev\\ppt_generator\\workspace\\army7000.pptx"
    )
    json_path: Path = Path(
        "C:\\kyu_universe\\dev\\ppt_generator\\workspace\\layout.json"
    )
    pptx_output_path: Path = Path(
        "C:\\kyu_universe\\dev\\ppt_generator\\workspace\\army7000_output.pptx"
    )

    # pptx_to_json(pptx_path=pptx_path, json_path=json_path)
    # json_to_pptx(pptx_output_path=pptx_output_path, json_path=json_path)
    wow = SinglePresentation(ref_pptx=pptx_output_path)

    round_1_path: Path = Path("C:\\kyu_universe\\dev\\ppt_generator\\lyric\\round_1")
    lyric_data_list: List[LyricData] = load_round(round_1_path)

    for lyric_data in lyric_data_list:
        title: str = lyric_data.title
        song_form: List[str] = lyric_data.song_form
        lyric_dict: Dict[str, List[str]] = lyric_data.lyric_dict

        for form in song_form:
            lyric_list: List[str] = lyric_dict[form]
            for lyric_line in lyric_list:
                wow.add_song_layout(title=title, text=lyric_line)

        wow.add_none_layout()

    wow.save(pptx_output_path)
