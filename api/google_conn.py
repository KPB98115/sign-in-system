import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
from metadata import metadata

# 設定 json 檔案路徑及程式操作範圍
Json = '/Library/WebServer/Documents/api/fifa-world-cup-event-sign-in-148770a2ee34.json'
Url = ['https://spreadsheets.google.com/feeds']

# 連線至資料表
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)

def updateData():
  # 開啟資料表及工作表
  Sheet = GoogleSheets.open_by_key('1V61T89K9LPdJJw7wxAqhgqyoYqenlhV0vS7eAjecqWs')
  Sheets = Sheet.get_worksheet(1)
  #update entire metadata to spreadsheets
  signed_data = []
  for i in range(len(metadata)):
    signed_data.append([
      metadata[i]["id"],
      metadata[i]["name"],
      metadata[i]["remark"],
      "True" if metadata[i]["registered"] else "False"
    ])
  Sheets.update("A2:D110", signed_data)

  #Sheets.append_row(data, table_range="A2:D2")
  print("[<Module>google_conn.py]寫入成功")

def insertData(data):
  # 開啟資料表及工作表
  Sheet = GoogleSheets.open_by_key('1V61T89K9LPdJJw7wxAqhgqyoYqenlhV0vS7eAjecqWs')
  Sheets = Sheet.get_worksheet(2)
  #insert new signed-in info to spreadsheets
  print(data)
  Sheets.append_row(data, table_range="A2:D2")
  return print("Data append successfully.")

def updateMetadata():
  Sheet = GoogleSheets.open_by_key('1V61T89K9LPdJJw7wxAqhgqyoYqenlhV0vS7eAjecqWs')
  Sheets = Sheet.get_worksheet(3)

  data = []
  for i in range(len(metadata)):
    data.append([
      metadata[i]["id"],
      metadata[i]["name"],
      "True" if metadata[i]["registered"] else "False",
      metadata[i]["remark"],
      "True" if metadata[i]["signed-in"] else "False",
      str(metadata[i]["timestamp"]),
      metadata[i]["number"],
    ])
  Sheets.update(f'A2:G{len(metadata)+10}', data)
  print("[<Module>google_conn.py]寫入成功")

# 讀取資料
#print(Sheets.get_all_values())