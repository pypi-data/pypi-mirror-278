#%%
import datetime  
# import calendar
# import time
from requests import get,post,delete
import json
import pandas as pd
import csv
import chardet # determine the csv file encoding


#%% class definition
class tb_connector():

    def __init__(self,url,username=None,password=None):
        self.COMMON_DATETIME_NAMES = {"Timeline","timeline","Datetime","datetime","Time","time","Timestamp","timestamp"}
        self.COMMON_DATETIME_FORMATS = {"%Y-%m-%d %H:%M:%S:%Z","%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M",
                                        "%d-%m-%Y %H:%M:%S:%Z","%d-%m-%Y %H:%M:%S","%d-%m-%Y %H:%M",
                                        "%m-%d-%Y %H:%M:%S:%Z","%m-%d-%Y %H:%M:%S","%m-%d-%Y %H:%M"}
        for datetime_format in list(self.COMMON_DATETIME_FORMATS):
            self.COMMON_DATETIME_FORMATS.add(datetime_format.replace("-", "/"))
            self.COMMON_DATETIME_FORMATS.add(datetime_format.replace("-", "."))

        self.JWT_token = None # access token
        self.auth_header = None
        self.url = url # url has protcol in front
        self.FQDN = None # FQDN does not have protocol in front. Some functions need FQDN and not url
        self.auth_header = None
        self.username = username
        self.password = password

    def _get_JWT_token(self) -> bool:
        
        JWT_token_response = post(self.url + "/api/auth/login", json={"username": self.username, "password": self.password},verify=True).json()
        if "token" in JWT_token_response:
            self.JWT_token = JWT_token_response["token"]
            self.auth_header = {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(self.JWT_token)}
            return True
        else:
            print("Status: {} Message: {}".format(JWT_token_response["status"],JWT_token_response["message"]))
            return False

    def connect(self) -> bool:
        return self._get_JWT_token()

    def getUserDevicesUsingGet(self,args: dict = None) -> dict:
        """Get all devices the currently logged in user has access to.
        args: dictionary with the following parameters
            pageSize : int 
            page : int
        """
        if args is None:
            params =  {"pageSize":1000,"page":0,"includeCustomers":None,"deviceProfileId":None,"active":None,"textSearch":None,"sortProperty":None,"sortOrder":None}
        else:
            params.update(args)
        #gets all devices currently logged in user has access to
        enpoint_url = self.url + "/api/user/devices"
        result = get(enpoint_url,headers=self.auth_header,params=params)
        return result

    def getTimeSeriesKeys(self,entityId: str,entityType: str = "DEVICE") -> dict:
        endpoint_url = self.url + f"/api/plugins/telemetry/{entityType}/{entityId}/keys/timeseries"
        result = get(endpoint_url,headers=self.auth_header)
        return result

    def gettimeSeriesData(self,entityId: str, keys: list, startTs: datetime, endTs: datetime, entityType: str = "DEVICE",limit: int = None,aggregate: str = None,useStrictDataTypes: bool = True):
        entpoint_url = self.url + f"""/api/plugins/telemetry/DEVICE/{entityId}/values/timeseries
        ?keys={','.join(keys)}
        &startTs={startTs.timestamp()*1000}
        &endTs={endTs.timestamp()*1000}
        &useStrictDataTypes={useStrictDataTypes}"""

        if limit is not None:
            entpoint_url += f"&limit={limit}"

        if aggregate is not None:
            endpoint_url += f"&agg={aggregate}"
    
    def deleteTimeSeriesData(self,entityId: str, keys: list, startTs: datetime, endTs: datetime, entityType: str = "DEVICE", all: bool = False,deleteLatest: bool = True,rewriteLatestIfDeleted: bool =True) -> dict:
        keys = ",".join(keys)
        startTs = int(startTs.timestamp()*1000)
        endTs = int(endTs.timestamp()*1000)
        endpoint_url = self.url + f"/api/plugins/telemetry/{entityType}/{entityId}/timeseries/delete?keys={keys}&deleteAllDataForKeys={all}&startTs={startTs}&endTs={endTs}&deleteLatest={deleteLatest}&rewriteLatestIfDeleted={rewriteLatestIfDeleted}"
        print(endpoint_url)
        result = delete(endpoint_url,headers=self.auth_header)
        return result

    def insertTimeSeriesData(self, entityId: str, data: dict, entityType: str = "DEVICE") -> dict:
        # Inserts time series data. Overwrites if there are duplicate timestamps and dataname
        scope = "ANY" # deprecated, but included for backwards compatibility
        endpoint_url = self.url + f"/api/plugins/telemetry/{entityType}/{entityId}/timeseries/{scope}?scope={scope}"
        result = post(endpoint_url,headers=self.auth_header,json=data)
        return result

    ################ Audit log implementation ##############################################

    def getAllAuditlogs(self,actionTypes: str,endTs: int,page: int,pagesize: int,sortOrder: str,sortProperty: str,startTs: int,textSearch:  str) -> dict:
        endpoint_url=self.url+f"""/api/audit/logs?
        actionTypes={actionTypes}
        &endTime={endTs}
        &page={page}
        &pageSize={pagesize}
        &sortOrder={sortOrder}
        &sortProperty={sortProperty}
        &startTime={startTs}
        &textSearch={textSearch}"""
        result = get(endpoint_url,headers=self.auth_header)

        return result
    
    def determineCsvFormat(self,filePath: str) -> dict:
        self.COMMON_ENCODINGS = ["utf-8","latin-1"]
        # determine column delimiter
        with open(filePath) as csvfile:
            columnSeparator = csv.Sniffer().sniff(csvfile.read()).delimiter

        # determine encoding. Note: This is prone to failures. 
        with open(filePath, 'rb') as csvfile:
            encoding = chardet.detect(csvfile.read())["encoding"]
            
        # determine decimal separator. TODO: Probably a better way of doing this.
        f = pd.read_csv(filePath,sep=columnSeparator,decimal=".",encoding=encoding)
        dotfails = 0
        for column_name in f.columns:
            try:
                pd.to_numeric(f[f.columns[1]])
            except:
                dotfails += 1

        f = pd.read_csv(filePath,sep=columnSeparator,decimal=",",encoding=encoding)
        commafails = 0
        for column_name in f.columns:
            try:
                pd.to_numeric(f[f.columns[1]])
            except:
                commafails += 1
        if dotfails > commafails:
            decimalSeparator = ","

        else:
            decimalSeparator = "."
            
        # determine datetime
        fileDataframe = pd.read_csv(filePath,sep=columnSeparator,decimal=decimalSeparator,parse_dates=True,encoding=encoding)
        timeStampColumn= self.COMMON_DATETIME_NAMES.intersection(fileDataframe.columns)

        return {"columnSeparator":columnSeparator,"decimalSeparator":decimalSeparator,"encoding":encoding,"timeStampColumn":timeStampColumn}

    def readCsv(self,filePath,datetimeColumn,columnSeparator=",",decimalSeparator=".",encoding=None,datetimeFormat: str = "%Y-%m-%d %H:%M:%S",determineFormat=True) -> pd.DataFrame: 
        if determineFormat:
            fileFormat = self.determineCsvFormat(filePath)
            if encoding is not None:
                fileFormat["encoding"] = encoding
            dataFrame = pd.read_csv(filePath,sep=fileFormat["columnSeparator"],decimal=fileFormat["decimalSeparator"],encoding=fileFormat["encoding"],parse_dates=True)
        # TODO: process all features if they are presented and determineFormat is False

        return dataFrame

    ########################################################################################
    
    def __repr__(self):
        return "TB connector: {}|{}".format(self.username,self.url)
#%% 
if __name__ == "__main__":
    import os
    base_path = os.path.dirname(__file__)
    credentials_path = os.path.join(base_path,"credentials.json")
    test_credentials_path = os.path.join(base_path,"test","credentials.json")
    if not os.path.exists(credentials_path):
        username = input("username: ")
        password = input("password: ")
        url = input("server url (with https://): ")
        test_id = input("test device id:")
        data = {"username":username,"password":password,"url":url}
        with open(credentials_path,"w") as outfile:
            outfile.write(json.dumps(data))
        with open(credentials_path,"w") as outfile:
            outfile.write(json.dumps(data))

    with open(credentials_path) as infile:
        credentials = json.load(infile)
    connector = tb_connector(credentials["url"],credentials["username"],credentials["password"])


    # connector._get_JWT_token()
    # r = connector.getUserDevicesUsingGet().json()["data"]
    # test_device = r[0]
    # test_device_name = test_device["name"]
    # test_device_entityType = test_device["id"]["entityType"]
    # test_device_deviceId = test_device["id"]["id"]
    #%%
    
    # k = connector.getTimeSeriesKeys(test_device_entityType,test_device_deviceId).json()

    # Convert Python DateTime (GMT time) to epoch

    #start_time=(calendar.timegm(datetime.datetime(year=2024,month=1,day=10,hour=5,minute=57,second=56).timetuple()))*1000
    
    #end_time=(calendar.timegm(datetime.datetime(year=2024,month=1,day=10,hour=18,minute=18,second=13).timetuple()))*1000
   
    
    # pointTs = datetime.datetime(2024,6,10,14,50,00)
    #auditlog=connector.implementAuditlog(actionTypes="Login",endTime=end_time,page=1,pagesize=30,sortOrder="ASC",sortProperty="entityType",startTime=start_time,textSearch="User").json()
    # connector.insertTimeSeriesData(credentials["testid"],{"ts":pointTs.timestamp()*1000,"values":{"test":1}})
    # time.sleep(4)
    # connector.insertTimeSeriesData(credentials["testid"],{"ts":pointTs.timestamp()*1000,"values":{"test":5}})
    # time.sleep(4)
    # startTs = datetime.datetime(2024,6,10,14,40,00)
    # endTs = datetime.datetime(2024,6,10,15,00,00)
    # connector.deleteTimeSeriesData(credentials["testid"],["test"],startTs,endTs)

    # -------------------- TEST reading ------------------------------

    filePath = os.path.join(base_path,"test","testfiles","standard_csv_us_latin1.csv")
    # format = connector.determineCsvFormat(filePath)
    # print(format)

    dataFrame = connector.readCsv(filePath,datetimeColumn="Timeline",encoding="latin-1")
    print(dataFrame)


