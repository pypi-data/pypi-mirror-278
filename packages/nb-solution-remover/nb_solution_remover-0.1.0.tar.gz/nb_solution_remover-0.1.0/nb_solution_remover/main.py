import nbformat

def strip_cells(notebook_path, output_path, keyword='# Solution'):
    # Load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Filter out cells that contain the keyword
    new_cells = []
    for cell in nb.cells:
        if cell.cell_type == 'code' and '# Solution' in cell.source:
            continue
        new_cells.append(cell)
    
    # Update the notebook with the filtered cells
    nb.cells = new_cells
    
    # Write the modified notebook to a new file
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    
    print(f"Cells containing '{keyword}' have been stripped and saved to {output_path}")

# Example usage
strip_cells('test.ipynb', 'stripped_notebook.ipynb')