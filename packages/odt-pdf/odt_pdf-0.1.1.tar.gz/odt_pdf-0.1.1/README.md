# ODT To PDF Converter

This is a simple python script that converts Open Document Text (ODT) files to PDF. It is based on the `pypdf` package.

## Installation

`pip install odt_pdf`

## Usage

### Convert an ODT file to a PDF file

```python
>>> from odt_pdf.odt_to_pdf import convert_odt_to_pdf
>>> convert_odt_to_pdf("input.odt", "data/output")
```

### Convert a PDF file to text
```python
>>> from odt_pdf.pdt_to_text import pdf_to_text
>>> text, attributes = pdf_to_text("example.pdf")
```


## Contributions

Contributions are welcome! If you have any improvements or bug fixes for the ODT to PDF Converter, feel free to submit a pull request on the GitHub repository. Please make sure to follow the contribution guidelines outlined in the repository's `CONTRIBUTING.md` file.

Happy coding!


