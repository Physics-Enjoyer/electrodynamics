import json
import re
from pathlib import Path

def edit_book():
    book_path = Path("./electrodynamics/content/book")
    file_list = list(book_path.glob("**/*.ipynb"))

    # Define patterns
    vec_pattern = r"__([a-zA-Z])__"
    vec_replace = r"$\\vec{\1}$"

    eq_pattern = r"Eq\. ([0-9]+)\.([0-9]+)"
    eq_replace = r"{eq}`eq\1.\2`"

    scaler_pattern = r"_([a-zA-Z])_"
    scaler_replace = r"$\1$"

    r_pattern = r"\Delta r"
    r_replace = r"\\mathcal{R}"

    vecr_pattern = r"\\Delta \vec{r}"
    vecr_replace = r"\\vec{\\mathcal{R}}"

    cal_pattern = r"\\mathscr"
    cal_replace = r"\\mathcal"

    rprime_pattern = r"\\vec{r'}"
    rprime_replace = r"\\vec{r}'"

    pdv_pattern = r"\pdv\{([^{}]+)\}\{([^{}]+)\}"
    pdv_replace = r"\frac{\partial \1}{\partial \2}"

    dv_pattern = r"\dv\{([^{}]+)\}\{([^{}]+)\}"
    dv_replace = r"\frac{d\1}{d\2}"


    for file_path in file_list:
        # Check if file is empty
        if file_path.stat().st_size == 0:
            print(f"Skipping {file_path.name} - it is empty!")
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                nb = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {file_path.name} is not a valid JSON/Notebook file.")
            continue

        # 1. Load the notebook as a dictionary
        with open(file_path, "r", encoding="utf-8") as f:
            nb = json.load(f)

        # 2. Iterate through cells and update text
        for cell in nb.get("cells", []):
            if cell["cell_type"] == "markdown":
                # Notebook 'source' can be a string or a list of strings
                source = "".join(cell["source"])

                # Apply replacements
                source = re.sub(vec_pattern, vec_replace, source)
                source = re.sub(eq_pattern, eq_replace, source)
                source = re.sub(scaler_pattern, scaler_replace, source)
                source = re.sub(r_pattern, r_replace, source)
                source = re.sub(pdv_pattern, pdv_replace, source)
                source = re.sub(dv_pattern, dv_replace, source)
                source = re.sub(rprime_pattern, rprime_replace, source)
                source = re.sub(cal_pattern, cal_replace, source)
                source = re.sub(vecr_pattern, vecr_replace, source)

                # Put it back as a list (standard for .ipynb)
                cell["source"] = [line + "\n" for line in source.split("\n")]
                # Remove the extra newline from the very last line
                if cell["source"]:
                    cell["source"][-1] = cell["source"][-1].rstrip("\n")

        # 3. Write the updated dictionary back to the file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)

        print(f"Updated: {file_path}")