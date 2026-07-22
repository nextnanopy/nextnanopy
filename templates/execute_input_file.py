import nextnanopy as nn
from pathlib import Path

this_dir = Path(__file__).parent
input_file_path = this_dir / "input files" / "DoubleQuantumWell_6nm_demo.nnp"


# execute input file
input_file = nn.InputFile(input_file_path)

input_file.execute()

