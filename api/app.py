from flask import Flask, render_template, request
from connection import checkRegistration
import re
import google_conn
from threading import Lock
import time
from flask_socketio import SocketIO

app = Flask(__name__)
sio = SocketIO(app)

thread = None
thread_lock = Lock()

def syncMetadata():
  while True:
    try:
      print("[<Main>background process]Start syncing metadata...")
      google_conn.updateMetadata()
      time.sleep(60)
    except:
      print("[<Main>background process]Something went wrong, stop syncing metadata.")
      break

@app.route("/", methods=['POST'])
def sign_in():
  #background process
  global thread
  with thread_lock:
    if thread is None:
      thread = sio.start_background_task(syncMetadata)
  #main process
  stdID = request.form["stdID"].upper()
  stdName = request.form["stdName"].lower()
  regex = re.compile('[_!#$%^&*()<>?/\|}{~:]')

  #check if the info is valid
  if stdID == "" and stdName == "":
    return render_template("error.html", status="both string are empty")
  elif len(stdID) > 0 and len(stdID) < 8  or len(stdID) > 20:
    return render_template("error.html", status="invalid student ID length")
  elif len(stdName) == 1:
    return render_template("error.html", status="invalid student name length")
  elif regex.search(stdID) != None and regex.search(stdName) != None:
      return render_template("error.html", status="invalid regex found")
  
  #recevice user info [優先／備取]
  result = checkRegistration(stdID, stdName)
  isRegistered = result[0]
  remark = result[1]
  num = result[2]

  if isRegistered:
    return render_template('signed_in.html', id=stdID, name=stdName, number=num, status=isRegistered, remark=remark)
  else:
    return render_template('signed_in.html', id=stdID, name=stdName, number=num, status=isRegistered, remark=remark)

#Run the script with $flask run -h 172.31.114.168
if __name__ == '__main__':
  sio.run(app)