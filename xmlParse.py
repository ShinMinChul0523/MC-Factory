# -*- coding: utf-8 -*-


import urllib.request
from urllib.parse  import quote
import xml.etree.ElementTree as etree




class Data:
    NONESELECTED = 0
    DATEINFO = 1

    def __init__(self):
        self.key = '4f417a44526a756e38394c766c5946'
        self.Year = '9999'
        self.Month = '9999'
        self.Date = '9999'
        self.select_menu = self.NONESELECTED
        self.filename = None
        self.url = None
        self.tree = None
        self.root = None

    def parse(self, menu,num1,num2,num3):
        self.select_menu = menu
        if self.select_menu == self.DATEINFO:
            self.url = 'http://openapi.seoul.go.kr:8088/%s/xml/SearchFirstAndLastTrainInfobyLineService/1/5/%s/%s/%s/' % (self.key,num1,num2,num3)
            data = urllib.request.urlopen(self.url).read()
            self.filename = "Data" + ".xml"
        f = open(self.filename, "wb")
        f.write(data)
        f.close()
        self.tree = etree.parse(self.filename)
        self.root = self.tree.getroot()
            
    def printInfo(self, menu):
        self.select_menu = menu
        if self.select_menu == self.DATEINFO:
            for boxOfficeResult in self.root.iter("SearchFirstAndLastTrainInfobyLineService"):
                for dailyBoxOffice in boxOfficeResult.iter("row"):
                    print('--------------------------------------------------------------')
                    print('호선 \t\t:' + dailyBoxOffice.findtext('LINE_NUM'))
                    print('1)평일 2)토요일 3)휴일/일요일\t\t:' + dailyBoxOffice.findtext('WEEK_TAG'))
                    print('상행선(1),하행선(2)\t\t:' + dailyBoxOffice.findtext('INOUT_TAG'))
                    print('지하철 역 번호\t:' + dailyBoxOffice.findtext('FR_CODE'))
                    print('전철역 코드\t\t:' + dailyBoxOffice.findtext('STATION_CD'))
                    print('전철 역 명 \t\t:' + dailyBoxOffice.findtext('STATION_NM'))
                    print('첫차 시간 \t\t:' + dailyBoxOffice.findtext('FIRST_TIME'))
                    print('첫차 출발역 이름 \t\t:' + dailyBoxOffice.findtext('F_SUBWAYSNAME'))
                    print('첫차 도착역 이름 \t\t:' + dailyBoxOffice.findtext('F_SUBWAYENAME'))
                    print('막차 시간 \t\t:' + dailyBoxOffice.findtext('LAST_TIME'))
                    print('막차 출발역 이 \t\t:' + dailyBoxOffice.findtext('L_SUBWAYSNAME'))
                    print('막차 도착역 이름 \t\t:' + dailyBoxOffice.findtext('L_SUBWAYENAME'))
                    print('--------------------------------------------------------------')
       
def main():
    print("------------지하철 첫차와 막차 시간표-------------")
    print("----------------------------------------------")
    print("----------------------------------------------")
    print("----------------------------------------------")
    print("----------------------------------------------")
    num = input("원하는 호선을 입력하세요")
    day = input("평일정보는 1 토요일정보는 2 일요일 및 공휴일 정보는 3")
    Root = input("상행선정보 1, 하행선정보 2")
    
    a = Data()
    a.parse(1,num,day,Root)
    a.printInfo(1)

    
if __name__ == "__main__":
    main()

