from pathlib import Path
import subprocess as sp

from .util.util import sanitize_input

def quarto_render_html(
    input_filename:str, 
    output_filename:str, 
    verbose:int=0
    ):
  
  """
  Renders a quarto (qmd) file.

  Args:
      input_filename (str): The name of the file to be rendered.
      output_filename (str): The name of the output file.
      verbose (bool, optional): If True, prints detailed status messages. Default is False.

  Returns:
      None

  Examples:
      >>> quarto_render_html('example.qmd', 'output.html')
  """
  
  #if file doesn't end with .qmd we want to add this here
  if input_filename[-4:] != '.qmd':
    input_filename = input_filename + '.qmd'

  #sanitise filenames as will be used in command line
  input_filename = sanitize_input(input_filename)
  output_filename = sanitize_input(output_filename)

  #check if the file exists if not then quit the function
  if Path(input_filename).is_file() == False:
    raise Exception("input_filename '" + input_filename + "' does not reference a qmd file")

  sp.run(['quarto', 'render', input_filename, '--output=' + output_filename],
    capture_output = False if verbose >= 1 else True
    )
  
  #check if the output html file was created if not then quit the function
  if Path(output_filename).is_file() == False:
    raise Exception("failed to generate html file from '" + input_filename + "'")
