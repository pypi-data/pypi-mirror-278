# presoutput

A package designed to automatically convert your [Quarto](https://quarto.org/) (qmd) documents into pdf or pptx files for sharing. 

The package has been designed to work by default with [revealjs](https://quarto.org/docs/presentations/revealjs/index.html) presenstations created through Quarto but should work with any html format created with Quarto.

## Installation

You can install presoutput via pip:

```bash
pip install presoutput
```

This package requires Google Chrome (or a chromium based browser like Edge) to be installed on the machine that is running the code so that it can print to PDF the html file generated from the quarto document.

## Usage

You can use the `qmd_to_pdf` or `qmd_to_pptx` functions to convert your Quarto (.qmd) file to either pdf or pptx. 

Note that when converting to either format it follows the pattern below and the pptx file is made up of png copies of the original slides.

    qmd
     |
     |--> html
           |
           |--> pdf
                 |
                 |--> png
                       |
                       |--> pptx



