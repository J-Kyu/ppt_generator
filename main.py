from pathlib import Path
from typing import List, Dict

from common.lyric import load_round, LyricData
from common.presentation import SinglePresentation


def create_ppt(round: int):
    pptx_output_path: Path = Path(
        f"C:\\kyu_universe\\dev\\ppt_generator\\workspace\\army7000_r{round}.pptx"
    )
    assert pptx_output_path.exists()

    wow = SinglePresentation(ref_pptx=pptx_output_path)

    round_path: Path = Path(
        f"C:\\kyu_universe\\dev\\ppt_generator\\lyric\\round_{round}"
    )
    assert round_path.exists()
    lyric_data_list: List[LyricData] = load_round(round_path)

    for lyric_data in lyric_data_list:

        title: str = lyric_data.title
        song_form: List[str] = lyric_data.song_form
        lyric_dict: Dict[str, List[str]] = lyric_data.lyric_dict

        print(f"---> {title}")

        for form in song_form:
            lyric_list: List[str] = lyric_dict[form]
            for lyric_line in lyric_list:
                wow.add_song_layout(title=title, text=lyric_line)

        wow.add_none_layout()

    wow.save(pptx_output_path)
    print(f"[Done] {pptx_output_path.as_posix()}")


if __name__ == "__main__":

    for r in range(4):
        create_ppt(r + 1)
