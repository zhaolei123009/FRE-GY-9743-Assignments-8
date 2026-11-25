"""Execute every notebook cell in a fresh in-process IPython session.

No network sockets are needed. Run from the repository root.
"""
from pathlib import Path
import nbformat
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output

path = Path(__file__).resolve().parent / 'hw8_sofr_ois_calibration_and_risk.ipynb'
if Path.cwd() != path.parent:
    raise RuntimeError('Run this script from the repository root.')
nb = nbformat.read(path, as_version=4)
shell = InteractiveShell.instance()
count = 0
for i, cell in enumerate(nb.cells):
    if cell.cell_type != 'code':
        continue
    count += 1
    with capture_output(stdout=True, stderr=True, display=True) as captured:
        result = shell.run_cell(cell.source, store_history=True)
    result.raise_error()
    cell.execution_count = count
    cell.outputs = []
    for name, value in [('stdout', captured.stdout), ('stderr', captured.stderr)]:
        if value:
            cell.outputs.append(nbformat.v4.new_output('stream', name=name, text=value))
    for output in captured.outputs:
        cell.outputs.append(nbformat.v4.new_output(
            'display_data', data=output.data, metadata=output.metadata))
    print(f'Cell {i}: passed')
    if captured.stdout:
        print(captured.stdout)
nbformat.validate(nb)
nbformat.write(nb, path)
print(f'Saved {count} successfully executed code cells to {path.name}.')
