from doscon_tb_api.doscon_tb_api import tb_connector
import json
import os
base_path = os.path.dirname(__file__)




with open("credentials.json") as infile:
    credentials = json.load(infile)
test_device_id = "0115de80-271d-11ef-acb6-b12209568c62"            

def test_connect_incorrect_credentials():
    connector = tb_connector(credentials["url"],credentials["username"],"wrongpassword")
    assert connector.connect() == False

def test_connect_correct_credentials():
    connector = tb_connector(credentials["url"],credentials["username"],credentials["password"])
    assert connector.connect() == True

def test_getUserDevicesUsingGet():
    connector = tb_connector(credentials["url"],credentials["username"],credentials["password"])
    connector.connect()
    result = connector.getUserDevicesUsingGet()
    assert result.status_code == 200

def test_getTimeSeriesKeys():
    connector = tb_connector(credentials["url"],credentials["username"],credentials["password"])
    connector.connect()
    result = connector.getTimeSeriesKeys(test_device_id)
    assert result.status_code == 200

def test_readCsv():
    connector = tb_connector(credentials["url"],credentials["username"],credentials["password"])
    filePath = os.path.join(base_path,"testfiles","standard_csv_us_latin1.csv")
    dataFrame = connector.readCsv(filePath,datetimeColumn="Timeline",encoding="latin-1")
    assert "æøå" in dataFrame.columns