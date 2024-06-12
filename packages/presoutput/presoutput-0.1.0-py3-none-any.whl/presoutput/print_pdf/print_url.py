import websocket
import json
import base64
import time

print_args = {
  #"landscape": False,
  "displayHeaderFooter": False,
  "printBackground": True,
  #"paperWidth": 8.27,  # inch
  #"paperHeight": 11.69,  # inch
  "marginTop": 0,  # 1cm
  "marginBottom": 0,
  "marginLeft": 0,
  "marginRight": 0,
  "pageRanges": "",
  "ignoreInvalidPageRanges": False,
  "headerTemplate": "",
  "footerTemplate": "",
  "preferCSSPageSize": True
}

def print_url(ws_url, url, output_file, ws_timeout=120, command_timeout=30, ):
  try:

    ws = websocket.create_connection(ws_url, suppress_origin=False)
    ws.settimeout(ws_timeout)

    #1 Target.createTarget (tab)
    ws.send(json.dumps({"id": 1, "method": "Target.createTarget", "params": {"url": "about:blank"}}))
    result = wait_result(ws, 1, command_timeout)

    #2 Target.attachToTarget in flat mode
    ws.send(json.dumps({"id": 2, "method": "Target.attachToTarget", "params": {"targetId": result['result']['targetId'], "flatten": True}}))
    result = wait_result(ws, 2, command_timeout)
    session_id = result['result']['sessionId']

    #3 Runtime.enable
    ws.send(json.dumps({"id": 3, "sessionId": session_id, "method": "Runtime.enable"}))
    result = wait_result(ws, 3, command_timeout)

    #4 Page.enable
    ws.send(json.dumps({"id": 4, "sessionId": session_id, "method": "Page.enable"}))
    result = wait_result(ws, 4, command_timeout)

    #5 Runtime.addBinding
    ws.send(json.dumps({"id": 5, "sessionId": session_id, "method": "Runtime.addBinding", "params": {"name": "pagedownListener"}}))
    result = wait_result(ws, 5, command_timeout)

    #6 Network.enable
    ws.send(json.dumps({"id": 6, "sessionId": session_id, "method": "Network.enable"}))
    result = wait_result(ws, 6, command_timeout)

    #7 Page.navigate
    ws.send(json.dumps({"id": 7, "sessionId": session_id, "method": "Page.navigate", "params": {"url": url}}))
    result = wait_result(ws, 7, command_timeout)

    error_on_page_nav = True if 'result' in result and 'error' in result['result'] else False
    if not error_on_page_nav: 
      error_on_page_nav = True if 'error' in result else False
    if error_on_page_nav:
      raise Exception("Can't nagivate to " + url)
    
    #wait for page to load
    result = wait_event(ws, 'Page.frameStoppedLoading', command_timeout)

    #8 Page.printToPDF
    ws.send(json.dumps({"id": 8, "sessionId": session_id, "method": "Page.printToPDF", "params": print_args}))
    result = wait_result(ws, 8, command_timeout)

    with open(output_file, 'wb') as f:
        f.write(base64.decodebytes(str.encode(result['result']['data'])))

  finally:
    ws.close()

def wait_event(ws, event, timeout=120):
  start_time = time.time()
  messages = []
  matching_message = None
  while True:
    now = time.time()
    if now-start_time > timeout:
      break
    try:
      message = ws.recv()
      parsed_message = json.loads(message)
      messages.append(parsed_message)
      if ('method' in parsed_message
          and parsed_message['method'] == event):
        matching_message = parsed_message
        break
    except websocket.WebSocketTimeoutException:
      continue
    except Exception:
      break
  return matching_message

def wait_result(ws, result_id, timeout=30):
  start_time = time.time()
  messages = []
  matching_result = None
  while True:
    now = time.time()
    if now-start_time > timeout:
      break
    try:
      message = ws.recv()
      parsed_message = json.loads(message)
      messages.append(parsed_message)
      if (('result' in parsed_message or 'error' in parsed_message)
          and parsed_message['id'] == result_id):
        matching_result = parsed_message
        break
    except websocket.WebSocketTimeoutException:
      continue
    except Exception:
      break
  return matching_result