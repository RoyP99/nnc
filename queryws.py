'''
Created on 27 sep 2024

@author: robje
'''
from simple_websocket import Client, ConnectionClosed
import threading
import json

class cQueryWs(object):
    '''
    classdocs
    '''


    def __init__(self, htmlSse, nmosInfo, nmosInfoLock):
        '''
        Constructor
        '''
        self.htmlSse = htmlSse
        self.nmosInfo = nmosInfo
        self.nmosInfoLock = nmosInfoLock
        self.endThread = False
        self.threadActive = False
        self.foundInfo = {'nodes': {},
                          'devices': {},
                          'sources': {},
                          'flows': {}, 
                          'senders': {},
                          'receivers': {}
                          }
        self.registryUrl = ''
        
    def myThread(self, url):
        self.threadActive = True
        print(f'connect to {url}')
        ws = Client.connect(url)
        print('connected')
        try:
            while self.endThread == False:
                data = ws.receive(0.1)
                if data != None:
                    try:
                        ddata = json.loads(data)
                        # print(f'Query {ddata}')
                    except:
                        ddata = {}
                    if 'grain_type' in ddata and 'grain' in ddata and ddata['grain_type'] == 'event':
                        grain = ddata['grain']
                        if 'data' in grain:
                            changedItems = []
                            for graindata in grain['data']:
                                spl = graindata['path'].split('/')
                                #print(spl)
                                myItem = spl[0]
                                if myItem in self.foundInfo:                                    
                                    if 'post' in graindata:
                                        itemInfo = graindata['post']
                                        if 'id' in itemInfo:
                                            itemId = itemInfo['id']
                                            self.foundInfo[myItem][itemId] = itemInfo  # replace or add
                                            if myItem not in changedItems:
                                                changedItems.append(myItem)
                                    elif 'pre' in graindata:
                                        itemInfo = graindata['pre']
                                        if 'id' in itemInfo:
                                            itemId = itemInfo['id']
                                            if itemId in self.foundInfo[myItem]:
                                                self.foundInfo[myItem].pop(itemId)
                                                if myItem not in changedItems:
                                                    changedItems.append(myItem)

                            self.nmosInfoLock.acquire()
                            for key in self.foundInfo.keys():
                                self.nmosInfo[key] = {}
                                for nkey, nvalue in self.foundInfo[key].items():
                                    self.nmosInfo[key][nkey] = nvalue.copy()
                            self.nmosInfoLock.release()
                            
                            if 'devices' in changedItems:
                                deviceList = []
                                for fDevice in self.foundInfo['devices']:
                                    dInfo = self.foundInfo['devices'][fDevice]
                                    deviceList.append({'label': dInfo['label'], 'uuid': dInfo['id'], 'description': dInfo['description'], 'type': dInfo['type'] })
                                sseStr = self.htmlSse.format_sse(json.dumps(deviceList), 'deviceList')
                                # sseStr = self.htmlSse.format_sse(json.dumps(self.foundInfo['devices']), 'deviceList')
                                self.htmlSse.announce(sseStr)
                                
        except (EOFError, ConnectionClosed):
            pass
        ws.close()
        self.threadActive = False
    
    def connect(self, url):
        if self.threadActive == True:
            self.close()
        self.endThread = False
        self.x = threading.Thread(target=self.myThread, args=(url,))
        self.x.start()
        
    def close(self):
        self.endThread = True
        self.x.join(1)
        
    def setRegistryUrl(self, newUrl):
        self.registryUrl = newUrl
        