# -*- coding: utf-8 -*-

import os
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.encoders import encode_base64

import time
import urllib.request
from urllib.parse  import quote
import xml.etree.ElementTree as etree
import webbrowser
import sys


# Open API
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

    # 화면프린트        
    def printInfo(self, menu):
        self.select_menu = menu
        if self.select_menu == self.DATEINFO:
            for MetroInfoResult in self.root.iter("SearchFirstAndLastTrainInfobyLineService"):
                for dailyMetroInfo in MetroInfoResult.iter("row"):
                    print('--------------------------------------------------------------')
                    print('호선 \t\t\t\t:' + dailyMetroInfo.findtext('LINE_NUM'))
                    print('1)평일 2)토요일 3)휴일/일요일\t:' + dailyMetroInfo.findtext('WEEK_TAG'))
                    print('상행선(1),하행선(2)\t\t:' + dailyMetroInfo.findtext('INOUT_TAG'))
                    print('지하철 역 번호\t\t\t:' + dailyMetroInfo.findtext('FR_CODE'))
                    print('전철역 코드\t\t\t:' + dailyMetroInfo.findtext('STATION_CD'))
                    print('전철 역 명 \t\t\t:' + dailyMetroInfo.findtext('STATION_NM'))

                    print('첫차 시간 \t\t\t:' + dailyMetroInfo.findtext('FIRST_TIME'))
                    print('첫차 출발역 이름 \t\t:' + dailyMetroInfo.findtext('F_SUBWAYSNAME'))
                    print('첫차 도착역 이름 \t\t:' + dailyMetroInfo.findtext('F_SUBWAYENAME'))
                    print('막차 시간 \t\t\t:' + dailyMetroInfo.findtext('LAST_TIME'))
                    print('막차 출발역 이름 \t\t:' + dailyMetroInfo.findtext('L_SUBWAYSNAME'))
                    print('막차 도착역 이름 \t\t:' + dailyMetroInfo.findtext('L_SUBWAYENAME'))
                    print('--------------------------------------------------------------')

    # 파일입출력
    def saveInfo(self, menu, f):
        self.select_menu = menu
        if self.select_menu == self.DATEINFO:
            for MetroInfoResult in self.root.iter("SearchFirstAndLastTrainInfobyLineService"):
                for dailyMetroInfo in MetroInfoResult.iter("row"):
                    f.write(dailyMetroInfo.findtext('LINE_NUM') + "호선 ")
                        
                    if dailyMetroInfo.findtext('WEEK_TAG') == '1':
                        f.write("평일 ")

                    elif dailyMetroInfo.findtext('WEEK_TAG') == '2':
                        f.write("토요일 ")

                    else:
                        f.write("일요일 및 공휴일 ")

                    if dailyMetroInfo.findtext('INOUT_TAG') == '1':
                        f.write("상행선 시간표\n")

                    else:
                        f.write("하행선 시간표\n")
                            
                    f.write('--------------------------------------------------------------\n')
                    f.write('호선 \t\t\t\t:' + dailyMetroInfo.findtext('LINE_NUM') + '\n')
                    f.write('1)평일 2)토요일 3)휴일/일요일\t:' + dailyMetroInfo.findtext('WEEK_TAG') + '\n')
                    f.write('상행선(1),하행선(2)\t\t:' + dailyMetroInfo.findtext('INOUT_TAG') + '\n')
                    f.write('지하철 역 번호\t\t\t:' + dailyMetroInfo.findtext('FR_CODE') + '\n')
                    f.write('전철역 코드\t\t\t:' + dailyMetroInfo.findtext('STATION_CD') + '\n')
                    f.write('전철 역 명 \t\t\t:' + dailyMetroInfo.findtext('STATION_NM') + '\n')
                    f.write('첫차 시간 \t\t\t:' + dailyMetroInfo.findtext('FIRST_TIME') + '\n')
                    f.write('첫차 출발역 이름 \t\t:' + dailyMetroInfo.findtext('F_SUBWAYSNAME') + '\n')
                    f.write('첫차 도착역 이름 \t\t:' + dailyMetroInfo.findtext('F_SUBWAYENAME') + '\n')
                    f.write('막차 시간 \t\t\t:' + dailyMetroInfo.findtext('LAST_TIME') + '\n')
                    f.write('막차 출발역 이름 \t\t:' + dailyMetroInfo.findtext('L_SUBWAYSNAME') + '\n')
                    f.write('막차 도착역 이름 \t\t:' + dailyMetroInfo.findtext('L_SUBWAYENAME') + '\n')
                    f.write('--------------------------------------------------------------\n\n')

# 메인 타이틀 출력
def printTitle():
    os.system('cls')
    print("--------------------------------------------------")
    print("----------- 지하철 첫차와 막차 시간표 ------------")
    print("--------------------------------------------------\n")

# 메인 현재 시간 출력
def printTime():
    t = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

    now = time.localtime()

    print("[", now.tm_year,"년", now.tm_mon,"월", now.tm_mday, "일", t[now.tm_wday], "]")
    print("[", now.tm_hour,"시", now.tm_min,"분 ]\n")

# 시간표 화면 출력
def printTimetable(num, day, Root):
    print("데이터를 불러오는 중...\n")
                
    a = Data()
    a.parse(1,num,day,Root)
    a.printInfo(1)

    print("\n데이터를 불러왔습니다! \n")

# 시간표 텍스트파일 저장
def saveData(num, day, Root, menuNum):
    inputNum = input("데이터를 저장할까요? (예: 1, 아니오: 2) : ")

    if inputNum == '1':
        print(" ")
        fileName = input("파일 이름: ")
        f = open(fileName + ".txt", 'w')

        print("\n데이터를 저장하는 중...")

        # 오늘 날짜 시간표 저장
        if menuNum == 1:
            for Root2 in [1, 2]:
                a = Data()
                a.parse(1,num,day,Root2)
                a.saveInfo(1, f)

        # 원하는 시간표 저장
        elif menuNum == 2:
            a = Data()
            a.parse(1,num,day,Root)
            a.saveInfo(1, f)

        # 모든 노선 시간표 저장
        elif menuNum == 3:
            for num2 in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                for day2 in [1, 2, 3]:
                    for Root2 in [1, 2]:
                        a = Data()
                        a.parse(1,num2,day2,Root2)
                        a.saveInfo(1, f)
            

        f.close()

# 시간표 파일 리스트
def getFileList() :
    # 텍스트 리스트를 다른 텍스트 파일로 만든다.
    os.system('dir /b *.txt > list.txt')

    # 만든 파일을 오픈한다.
    f = open('list.txt')
            
    line = f.readline()     # 한줄 읽기
    line = line[:-1]        # 공백문자 제거

    # 모든 파일을 리스트에 담는다.
    fileList = []
            
    while line:
        if line != "list.txt":
            fileList.append(line)
                    
        line = f.readline()
        line = line[:-1]

    # 파일 리스트를 출력한다.
    index = 1
    for d in fileList:
        print("[", index, "] ", d)
        index += 1

    f.close()
    
    return fileList

    
#------
# 메인
#------
def main():
    while 1:
        printTitle()
        printTime()

        # 메뉴
        print("1. 오늘 날짜 시간표")
        print("2. 원하는 시간표")
        print("3. 모든 노선 시간표")
        print("4. 저장한 시간표")
        print("5. 이메일 전송")
        print("6. 인터넷 검색")
        print("7. 종료\n")

        inputNum = input("입력 : ")

        # 1. 오늘 날짜 시간표
        if inputNum == '1':
            printTitle()
            printTime()

            num = input("원하는 호선을 입력하세요 : ")

            now = time.localtime()

            day = 1

            if now.tm_wday < 6:         # 평일
                day = 1

            elif now.tm_wday == 6:      # 토요일
                day = 2

            elif now.tm_wday == 7:      # 일요일
                day == 3
                
            for Root in [1, 2]:         # 상, 하행선 모두 출력
                if Root == 1:
                    print("\n상행선 시간표")

                else:
                     print("\n하행선 시간표")
                            
                printTimetable(num, day, Root)
                
            saveData(num, day, Root, 1)

        # 2. 원하는 시간표
        elif inputNum == '2':
            printTitle()
            printTime()

            num = input("원하는 호선을 입력하세요 : ")
            day = input("평일 1 토요일 2 일요일 및 공휴일 3 : ")
            Root = input("상행선 1, 하행선 2 : ")

            print("\n")
            printTimetable(num, day, Root)
            
            saveData(num, day, Root, 2)

        # 3. 모든 노선 시간표
        elif inputNum == '3':
            printTitle()
            printTime()

            for num in [1, 2, 3, 4, 5, 6, 7, 8, 9]:     # 호선
                for day in [1, 2, 3]:                   # 날짜
                    for Root in [1, 2]:                 # 상,하행선
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
                
            saveData(num, day, Root, 3)

        # 4. 저장한 시간표
        elif inputNum == '4':
            printTitle()
            printTime()

            # 파일 이름 리스트를 얻어온다.
            fileList = getFileList()

            if len(fileList) == 0:
                print("\n데이터가 없습니다.")
                input()
                continue
            
            fileNum = int(input("\n불러올 파일 번호를 입력해주세요 : "))

            printTitle()
            printTime()

            # 입력된 번호의 파일을 읽어서 출력한다.
            if len(fileList) < fileNum:
                print("번호를 잘못 입력하셨습니다.")
                
            else:
                print("데이터를 불러오는 중...\n")
                f = open(fileList[fileNum - 1])
                print(f.read())
                f.close()
                print("\n데이터를 불러왔습니다! \n")

            input()

        # 5. 이메일 전송
        elif inputNum == '5':
            printTitle()
            printTime()

            # 메일 정보 입력
            senderID = input("daum 아이디 입력 : ")
            senderPW = input("daum 패스워드 입력 : ")
            sender = senderID + '@daum.net'

            print("\n")

            recipient = input("받는 사람 메일 주소 : ")

            print("\n")

            mailTitle = input("메일 제목 : ")
            mailString = input("내용 : ")

            # 첨부파일 정보 입력
            attach = "";
            
            printTitle()
            printTime()
            
            fileList = getFileList()

            if len(fileList) == 0:
                print("\n첨부 할 수 있는 데이터가 없습니다.")
                print("메일 보내기에 실패했습니다.")
                input()
                continue
            
            fileNum = int(input("\n불러올 파일 번호를 입력해주세요 : "))


            # 입력된 번호의 파일을 읽어서 출력한다.
            if len(fileList) < fileNum:
                print("\n번호를 잘못 입력하셨습니다.")
                print("메일 보내기에 실패했습니다.")
                input()
                continue
                
            else:
                attach = fileList[fileNum - 1]

            print("\n메일을 전송하고 있습니다!!")

            # 메일 정보 설정
            msg = MIMEMultipart()
            msg['Subject'] = Header(mailTitle,'utf8')
            msg['From'] = sender
            msg['To'] = recipient

            # 서버 접속
            s = smtplib.SMTP_SSL('smtp.daum.net',465)

            try:
                s.login( senderID , senderPW )

            except:
                print("\n아이디 또는 비밀번호가 잘못되었습니다.")
                print("메일 보내기에 실패했습니다.")
                input()
                continue
                

            # 첨부파일
            if (attach != None):
                part = MIMEBase("application", "octet-stream" , _charset="utf8")
                part.set_payload(open(attach, "rb").read())
                encode_base64(part)
                part.add_header("Content-Disposition", "attachment", filename = ("utf8", "",os.path.basename(attach)))
            
            msg.attach(part)
            msg.attach(MIMEText(mailString, "html", _charset="utf8"))

            # 메일 전송
            s.sendmail(sender, recipient, msg.as_string())
            s.quit()

            print("\n메일 전송을 완료하였습니다.")
                
            input()
            
        # 6. 인터넷 검색    
        elif inputNum == '6':
            printTitle()
            printTime()
            search=input("검색어를 입력하세요:")
            search_split=search.split()
            webbrowser.open("https://www.google.co.kr/search?q="+search)

        # 7. 종료    
        elif inputNum == '7':
            break

    
if __name__ == "__main__":
    main()

