from datetime import datetime
from metadata import metadata

#global variables
register_num = 0
newArrival_num = 0

def checkRegistration(stdID, stdName):
  global register_num
  global newArrival_num
  #inner function to add user info to local data
  def addData(stdID, stdName, number):
    newMember = {
      "id": stdID,
      "name": stdName,
      "registered": False,
      "remark": "",
      "signed-in": True,
      "timestamp": str(datetime.fromtimestamp(datetime.now().timestamp())),
      "number": number
    }
    metadata.append(newMember)
    #sync new data to google spreadsheet
    """
    try:
      google_conn.insertData([f'{datetime.fromtimestamp(newMember["timestamp"])}', newMember["id"], newMember["name"],
        "True" if newMember["registered"] else "False", newMember["number"]
      ])
    except:
      print("Something went wrong, wait until update entire metadata")
    """
  #inner function to modify local data
  def modifyData(stdID, stdName, number, index):
    metadata[index]["id"] = stdID
    metadata[index]["name"] = stdName
    metadata[index]["signed-in"] = True
    metadata[index]["timestamp"] = str(datetime.fromtimestamp(datetime.now().timestamp())),
    metadata[index]["number"] = number
    #sync data to google spreadsheet
    """
    try:
      google_conn.insertData([
        f'{datetime.fromtimestamp(metadata[index]["timestamp"])}', stdID, stdName,
        "True" if metadata[index]["registered"] else "False", number
      ])
    except:
      print("Something went wrong, wait until update entire metadata")
    """
  print("[<Module>connection.py]Looking for matched user info in metadata......")
  #check if the user have registered.
  for i in range(len(metadata)):
    if stdID != "":
      if stdID == metadata[i]["id"]:
        #if this id is already signed-in.
        if metadata[i]["signed-in"]:
          print(f'[<Module>connection.py]{stdID}{stdName} are already signed-in.')
          return [metadata[i]["registered"], metadata[i]["remark"], metadata[i]["number"]]
        #stdID is not empty string and found metached data.
        print(f'[<Module>connection.py]found matching id: {stdID}')
        register_num+=1
        modifyData(metadata[i]["id"], stdName, register_num, i) #update: first parameter changed to stdName
        return [metadata[i]["registered"], metadata[i]["remark"], register_num]
      #else:
      #  print("no matching data found, looking for next one...")
    #if stdID is empty string, use stdName to verify instead.
    else:
      #if this name is already signed-in.
      if metadata[i]["signed-in"]:
        return [metadata[i]["registered"], metadata[i]["remark"], metadata[i]["number"]]
      if stdName == metadata[i]["name"]:
        #stdName is not empty string and found matched data.
        print(f'[<Module>connection.py]found matching stdName: {stdName}')
        register_num+=1
        modifyData(stdID, metadata[i]["name"], register_num, i) #update: first parameter changed to stdID
        return [metadata[i]["registered"], metadata[i]["remark"], register_num]
    #not matching data found, continue the for loop.
  #no matched data found in metadata at all, add new data to metadata.
  print("[<Module>connection.py]no data matched, add new data")
  newArrival_num+=1
  addData(stdID, stdName, newArrival_num)
  return [metadata[-1]["registered"], "", newArrival_num]

#12/17 update: Wait for test in CGU wifi enviorment.
#12/18 update: Still waiting for test. Updated google synchronization feature.
