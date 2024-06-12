from pathlib import Path

from .quarto_render import quarto_render_html
from .chrome_print import chrome_print
from .util.util import filename_with_suffix

from .pdf_to_pptx import pdf_to_pptx

def qmd_to_pdf(
  input_filename:str, 
  output_filename:str=None, 
  delete_intermediate:bool=True,
  browser:str=None,
  verbose:int=0
  ):
  
  """
  Renders a Quarto (qmd) revealjs presentation and converts this to a pdf file. 

  pptx is generated via rendering the presentation in html and printing html to pdf. 

  Args:
      input_filename (str): Path to the input qmd file.
      output_filename (str): Path to save the output PDF file.
      delete_intermediate (bool, optional): If True, delete the html outputs after pdf is generated. Default is True.
      browser (str, optional): The path to chrome (or chrome based brower like chromium / edge). Defaults to the default location for the OS.
      verbose (bool, optional): If True, show progress messages. Default is True.

  Retuns:
      None

  Examples:
      >>> qmd_to_pptx('document.qmd', 'output.pdf')
  """

  if output_filename is None:
    output_filename = filename_with_suffix(input_filename, 'pdf')

  filename_qmd = filename_with_suffix(input_filename, 'qmd')
  filename_html = filename_with_suffix(output_filename, 'html')
  filename_pdf = filename_with_suffix(output_filename, 'pdf')

  quarto_render_html(
    input_filename=filename_qmd, 
    output_filename=filename_html, 
    verbose=verbose
    )

  chrome_print(
    input_file=filename_html, 
    output_file=filename_pdf,
    browser=browser, 
    verbose=verbose
    )

  if delete_intermediate:
    Path(filename_html).unlink()


def qmd_to_pptx(
  input_filename:str, 
  output_filename:str=None, 
  delete_intermediate:bool=True,
  browser:str=None,
  dpi:int=300,
  pptx_height:float=7.5,
  pptx_width:float=13.33,
  verbose:int=0
  ):

  """
  Renders a Quarto (qmd) revealjs presentation and converts this to a pptx file. 

  pptx is generated via rendering the presentation in html, printing html to pdf and then taking a screenshot of each page and inserting into a blank pptx. 

  Args:
      input_filename (str): Path to the input qmd file.
      output_filename (str): Path to save the output PowerPoint presentation.
      delete_intermediate (bool, optional): If True, delete both the html and pdf outputs after pptx is generated. Default is True.
      browser (str, optional): The path to chrome (or chrome based brower like chromium / edge). Defaults to the default location for the OS.
      dpi (int, optional): DPI (dots per inch) for image conversion. Default is 300.
      pptx_height(float, optional): PPTX height in inches. Default is 7.5 (standard widescreen presentation size)
      pptx_width(float, optional): PPTX width in inches. Default is 13.33 (standard widescreen presentation size)
      verbose (bool, optional): If True, show progress messages. Default is True.

  Retuns:
      None

  Examples:
      >>> qmd_to_pptx('document.qmd', 'output.pptx', dpi=500)
  """
  
  if output_filename is None:
    output_filename = filename_with_suffix(input_filename, 'pptx')

  filename_qmd = filename_with_suffix(input_filename, 'qmd')
  filename_html = filename_with_suffix(output_filename, 'html')
  filename_pdf = filename_with_suffix(output_filename, 'pdf')
  filename_pptx = filename_with_suffix(output_filename, 'pptx')

  quarto_render_html(
    input_filename=filename_qmd, 
    output_filename=filename_html, 
    verbose=verbose
    )

  chrome_print(
    input_file=filename_html, 
    output_file=filename_pdf,
    browser=browser, 
    verbose=verbose
    )
  
  pdf_to_pptx(
    input_pdf_path=filename_pdf,
    output_pptx_path=filename_pptx,
    dpi=dpi,
    pptx_height=pptx_height,
    pptx_width=pptx_width,
    verbose=verbose
  )

  if delete_intermediate:
    Path(filename_html).unlink()
    Path(filename_pdf).unlink()