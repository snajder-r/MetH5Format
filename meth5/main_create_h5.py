from typing import List
import argparse
import tqdm
from pathlib import Path
from meth5.meth5 import MetH5File


def main(
    chunk_size: int, input_dir: Path, output_file: Path, compression: str, allowed_chromosomes: List[str], quiet: bool
):
    if compression == "None":
        compression = None
    
    if allowed_chromosomes is not None and len(allowed_chromosomes) == 0:
        allowed_chromosomes = None
    
    input_files = list(input_dir.iterdir())
    
    if len(input_files) == 0:
        raise ValueError(f"No input files found in input directory f{str(input_dir)}")
    
    with MetH5File(output_file, chunk_size=chunk_size, mode="w", compression=compression) as m5_out:
        for input_file in tqdm.tqdm(input_files) if not quiet else input_files:
            m5_out.parse_and_add_nanopolish_file(
                input_file, postpone_sorting_until_close=True, include_chromosomes=allowed_chromosomes
            )
        m5_out.create_chunk_index()
