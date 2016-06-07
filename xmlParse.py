# -*- coding: utf-8 -*-

import os
import time
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

def printTitle():
    os.system('cls')
    print("--------------------------------------------------")
    print("----------- 지하철 첫차와 막차 시간표 ------------")
    print("--------------------------------------------------\n")

def printTimetable(num, day, Root):
    print("데이터를 불러오는 중...\n")
                
    a = Data()
    a.parse(1,num,day,Root)
    a.printInfo(1)

    print("\n데이터를 불러왔습니다! \n")
       
def main():
    while 1:
        printTitle()
        
        print("1. 오늘 날짜 시간표")
        print("2. 원하는 시간표")
        print("3. 모든 노선 시간표\n")

        inputNum = input("입력 : ")

        if inputNum == '1':
            printTitle()

            num = input("원하는 호선을 입력하세요 : ")

            now = time.localtime()

            day = 1

            if now.tm_wday < 6:
                day = 1

            elif now.tm_wday == 6:
                day = 2

            elif now.tm_wday == 7:
                day == 3
                
            for Root in [1, 2]:
                if Root == 1:
                    print("\n상행선 시간표")

                else:
                     print("\n하행선 시간표")
                            
                printTimetable(num, day, Root)
                
            input()

        elif inputNum == '2':
            printTitle()

            num = input("원하는 호선을 입력하세요 : ")
            day = input("평일 1 토요일 2 일요일 및 공휴일 3 : ")
            Root = input("상행선 1, 하행선 2 : ")

            print("\n")
            printTimetable(num, day, Root)
            input()

        elif inputNum == '3':
            printTitle()

            for num in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                for day in [1, 2, 3]:
                    for Root in [1, 2]:
                        print(num, "호선 ")
                        
                        if day == 1:
                            print("평일 ")

                        elif day == 2:
                            print("토요일 ")

                        else:
                            print("일요일 및 공휴일 ")

                        if Root == 1:
                            print("상행선 시간표")

                        else:
                            print("하행선 시간표")
                            
                        printTimetable(num, day, Root)

                        print("\n")
                
            input()

    
if __name__ == "__main__":
    main()

