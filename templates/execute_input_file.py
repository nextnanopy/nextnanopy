import nextnanopy as nn
from pathlib import Path

this_dir = Path(__file__).parent
input_file_path = this_dir / "input files" / "DoubleQuantumWell_6nm_demo.nnp"


# execute input file
input_file = nn.InputFile(input_file_path)

# by default the failed simulation does not raise an exception
# but you can change this behavior with the `convergenceCheck` argument
input_file.execute(convergenceCheck=True, convergence_check_mode="terminate")



