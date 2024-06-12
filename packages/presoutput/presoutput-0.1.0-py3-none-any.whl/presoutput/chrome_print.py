import os
from pathlib import Path
from dotenv import load_dotenv
import shutil
import socket
import datetime
import subprocess
import time
import requests

from .util.util import filename_with_suffix
from .print_pdf.print_url import print_url
from .print_pdf.serve_html_file import LocalWebServer

import platform
if platform.system() == 'Windows': import winreg

def chrome_print(
  input_file:str,
  output_file:str=None,
  browser:str=None,
  verbose:int=0
  ):

  """
  Prints a local html file to PDF through chrome. 
  Designed print the output of a rendered quarto file.

  Args:
      input_filename (str): The name of the html file to be printed via chrome.
      output_filename (str, optional): The name of the output PDF file. Defaults to the same name as the input file.
      browser (str, optional): The path to chrome (or chrome based brower like chromium / edge). Defaults to the default location for the OS.
      verbose (bool, optional): If True, prints detailed status messages. Default is False.

  Returns:
      None

  Examples:
      >>> chrome_print('document.html')
      >>> chrome_print('document.html', 'output.html')

  """
  
  try: 
    ps = None #this is in case it errors before ps is created. if this happens the on close statement doesn't work correctly.
    load_dotenv() #load variables from .env if they exist

    #check if input file exists and is an html file
    if not Path(input_file).exists():
      raise Exception("Input file doesn't exist")
    if input_file[-5:] != '.html':
      raise Exception("Input file is not a html file")
    
    input_file = str(Path(input_file).resolve())

    #create output file from input file
    if output_file is None:
      output_file = filename_with_suffix(input_file, 'pdf')

    #get chrome browser
    if browser is None:
      if os.getenv('QUARTO_CHROME') is not None:
        browser = browser = os.getenv('QUARTO_CHROME')
      else:
        browser = find_chrome()
    else: 
      if Path(browser).exists() == False:
        browser = shutil.which(browser)
    if os.access(browser, os.X_OK) == False:
      raise Exception("The browser is not executable: " +  browser)
    if verbose >= 1:
      print('Using browser: ' + browser)

    #get a free port on your system
    debug_port = find_free_port()

    #create list of args to be passed into chrome print
    extra_args = []
    extra_args.extend(proxy_args())
    if platform.system() == "Windows":
        extra_args.append('--no-sandbox')
    extra_args.extend([
      '--headless',
      '--disable-dev-shm-usage',
      '--font-render-hinting=none',
      '--remote-allow-origins=*',
      '--disable-gpu',
      '--disable-translate',
      '--disable-extensions',
      '--disable-background-networking',
      '--safebrowsing-disable-auto-update',
      '--disable-sync',
      '--disable-default-apps',
      '--hide-scrollbars',
      '--metrics-recording-only',
      '--mute-audio',
      '--no-first-run',
      '--no-default-browser-check'
      ])

    extra_args = list(set(extra_args))
    extra_args.extend([
      f'--remote-debugging-port={debug_port}',
      ])
    
    log_file = f"chrome-stderr-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log" if os.getenv('pagedown.chrome.log', 'FALSE').upper() == 'TRUE' else None

    ps = subprocess.Popen(
      [browser] + extra_args,
      stderr=None if verbose >= 1 else subprocess.DEVNULL if log_file is None else open(log_file, 'w'),
      stdout=None if verbose >= 1 else subprocess.DEVNULL
      )
    
    remote_protocol_ok = is_remote_protocol_ok(debug_port, verbose = verbose)

    if remote_protocol_ok == False:
      raise Exception("A more recent version of Chrome is required.")
    
    websocket_url = get_entrypoint(debug_port, verbose)

    serve_html_port = find_free_port()
    web_server = LocalWebServer(input_file, port=int(serve_html_port), verbose=verbose) 
    web_server.start()

    print_url(websocket_url, f'http://127.0.0.1:{str(serve_html_port)}?print-pdf', output_file) 


  finally:
    kill_chrome(ps, web_server, verbose)


# supporting functions

def find_chrome() -> str:
  match platform.system():
    case 'Darwin': #macos
      return '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    case 'Linux':
      for browser in ['google-chrome', 'chromium-browser', 'chromium', 'google-chrome-stable']:
        result = shutil.which(browser)
        if result != None:
          return result
      #if gets to here it couldn't find anything
      raise Exception("can't find google chrome specify the path in the browser variable")
    case 'Windows':
      for browser in ['ChromeHTML', 'MSEdgeHTM']:
        try:
          result = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, browser + "\\shell\\open\\command", 0, winreg.KEY_READ), "")[0].split('"')[1]
        except:
          result = ''
        if result != '': return result
      raise Exception("can't find google chrome specify the path in the browser variable")
    case _:
      raise Exception("your os is not currently supported")
    
def proxy_args() -> str:
  # Get proxy environment variables in order of priority
  proxy_vars = ['https_proxy', 'HTTPS_PROXY', 'http_proxy', 'HTTP_PROXY']
  val = [os.getenv(var) for var in proxy_vars if os.getenv(var)]
  
  # If no non-empty proxy environment variable is found, return an empty list
  if not val:
    return []
  
  # Construct proxy arguments
  proxy_server_arg = f"--proxy-server={val[0]}"
  proxy_bypass_list_arg = "--proxy-bypass-list=" + ";".join(no_proxy_urls())
  
  return [proxy_server_arg, proxy_bypass_list_arg]

def no_proxy_urls() -> str:
  # Get no_proxy environment variable, split by ',' or ';' and include localhost and 127.0.0.1
  no_proxy_env = os.getenv('no_proxy') or os.getenv('NO_PROXY') or ""
  urls = [url.strip() for url in no_proxy_env.replace(",", ";").split(";") if url.strip()]
  urls.extend(['localhost', '127.0.0.1'])
  return list(set(urls))  # Return unique URLs

def find_free_port() -> str:
    with socket.socket() as s:
        s.bind(('', 0))            # Bind to a free port provided by the host.
        return str(s.getsockname()[1])  # Return the port number assigned.
  
def kill_chrome(ps, web_server, verbose:int=0):
  if verbose >= 1:
    print('Closing browser')

  # Check if the process is alive before attempting to kill it
  if ps is not None:
    if ps.poll() is None:
      ps.kill()

  if verbose >= 1:
    print('Closing webserver')

  if web_server is not None:
    web_server.close()

def is_remote_protocol_ok(debug_port:str, verbose:int=0) -> bool:
  url = f'http://127.0.0.1:{debug_port}/json/protocol'
  
  # Specify the maximum number of attempts and sleep time between attempts
  max_attempts = 20
  sleep_time = 0.5
  
  if verbose >= 1:
    print(f'Trying to find headless Chrome in {max_attempts} attempts')

  for i in range(1, max_attempts + 1):
    try:
      response = requests.get(url)
      response.raise_for_status()  # Raise an error for bad response status codes
      
      remote_protocol = response.json()
    except Exception as e:
      remote_protocol = None
    
    if remote_protocol:
      if verbose >= 1:
        print(f'Headless Chrome found at attempt {i}')
      break
    
    if i == max_attempts:
      raise RuntimeError(f'Cannot find headless Chrome after {max_attempts} attempts')
    
    time.sleep(sleep_time)
  
  # Define required commands and events
  required_commands = {
    'DOM': ['enable', 'getBoxModel', 'getDocument', 'querySelector'],
    'Network': ['enable'],
    'Page': ['addScriptToEvaluateOnNewDocument', 'captureScreenshot', 'enable', 'navigate', 'printToPDF'],
    'Runtime': ['enable', 'addBinding', 'evaluate'],
    'Target': ['attachToTarget', 'createTarget']
  }
  
  required_events = {
    'Inspector': ['targetCrashed'],
    'Network': ['responseReceived'],
    'Page': ['loadEventFired'],
    'Runtime': ['bindingCalled', 'exceptionThrown']
  }
  
  # Extract remote domains, commands, and events
  remote_domains = [domain['domain'] for domain in remote_protocol['domains']]
  remote_commands = {
      domain: [
          command['name']
          for d in remote_protocol['domains'] if d['domain'] == domain
          for command in d['commands']
      ]
      for domain in required_commands.keys()
  }
  remote_events = {
      domain: [
          event['name']
          for d in remote_protocol['domains'] if d['domain'] == domain
          for event in d['events']
      ]
      for domain in required_events.keys()
  }
  
  # Check if all required commands and events are available in the remote protocol
  if not all(set(required_commands[domain]) <= set(remote_commands[domain]) for domain in required_commands):
    return False
  if not all(set(required_events[domain]) <= set(remote_events[domain]) for domain in required_events):
    return False
  
  # Check if printToPDF supports streaming
  print_to_pdf_params = [param for param in remote_protocol['domains'][remote_domains.index('Page')]['commands'] if param['name'] == 'printToPDF'][0]['parameters']
  stream_pdf_available = 'transferMode' in [param['name'] for param in print_to_pdf_params]

  return stream_pdf_available

def get_entrypoint(debug_port:str, verbose:int=0) -> str:
  url = f'http://127.0.0.1:{debug_port}/json/version'
  response = requests.get(url)
  version_infos = response.json()

  browser = version_infos.get('webSocketDebuggerUrl')
  if not browser:
    raise Exception("Cannot find 'Browser' websocket URL. Please retry.")

  if verbose >= 1:
    print('Browser version:', version_infos.get('Browser'))

  return browser