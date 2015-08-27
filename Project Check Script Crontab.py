# -*- coding: UTF-8 -*-
import MySQLdb
import serial
import time
import datetime
from gtts import gTTS
import subprocess
import webbrowser
import urllib
import ThaiBulkSMSAPI
import datetime

#ตั้งเวลานัดโทร กี่วัน
time_auto_call = 4
time_auto_sms = 5

def change_phone_number_format(Phone,check_vt):
    num = []
    number = {'0','1','2','3','4','5','6','7','8','9'}
    if (Phone == None):
        return 0
    for i in range(len(Phone)):
        if(Phone[i] in number):
            num.append(Phone[i])
    realnum =''.join(num)
    print len(realnum)
    if(len(realnum)==9 or len(realnum)==10):
        if(len(realnum)==9 and check_vt == 1):
           return 0
        else:
            return realnum
    else:
        return 0

def find_max_id(check_vt):
    db = MySQLdb.connect(####Database Pi####, use_unicode=True, charset="UTF8")
    num= check_vt-1
    text=["tmessage","vmessage"]
    text2=["TM_ID","VM_ID"]
    sql = "SELECT max(%s) FROM %s"%(text2[num],text[num])
    print sql
    cursor = db.cursor()
    cursor.execute(sql)
    max_id = cursor.fetchall()
    print max_id[0][0]
    if(max_id[0][0]==None):
        return -1
    return max_id[0][0]
    
def chkmax_dayofmonth (year):
        max_dayofmonth = [31,28,31,30,31,30,31,31,30,31,30,31]
        if ((year%4) == 0 and (year%100!=0)):
            max_dayofmonth[1]=29
        elif(year%100==0 and year%400==0):
            max_dayofmonth[1] = 29
        return max_dayofmonth
    
def new_plus_time(plus_day):
    start_date = (time.strftime("%Y/%m/%d"))
    print start_date

    date_1 = datetime.datetime.strptime(start_date, "%Y/%m/%d")

    end_date = date_1 + datetime.timedelta(days=plus_day)
    output = str(end_date)
    return output[0:10]

def plus_time(plus_day):
    currentTime =(time.strftime("%d "+"%m "+"%Y "+"\n%H:"+"%M:"+"%S"))

    day = (time.strftime("%d"))
    month = (time.strftime("%m"))
    year = (time.strftime("%Y"))

    day = int(day)
    month= int(month)
    year = int(year)

    #year = 2004

    max_dayofmonth = chkmax_dayofmonth(year)

    day +=plus_day

    if(day >max_dayofmonth[month-1]):
        day = day-max_dayofmonth[month-1]-1
        month +=1
        if(month>12):
            month = 1
            year +=1

    #print "Current Time:\n"+currentTime
    #print "Plus Time:"

    chd=0
    chm=0
    if (day)<10 :
        chd=1    
    if (month)<10:
        chm=2
        
    chMD=chd+chm
    if chMD==0:
        text = str(day),str(month),str(year)
    elif chMD==1:
        text = '0'+str(day),str(month),str(year)
    elif chMD==2:
        text = str(day),'0'+str(month),str(year)
    else:
        text = '0'+str(day),'0'+str(month),str(year)
    text2 = text[2],text[1],text[0]
    return '-'.join(text2)

def function_time():
    current_time = time.time()
    myset = time.localtime(current_time)
    dateformat = '%d/%m/%Y'
    dayformat = '%d'
    monthformat = '%m'
    yearformat = '%Y'

    day = time.strftime(dayformat, myset)
    month = time.strftime(monthformat, myset)
    year = int(time.strftime(yearformat, myset))
    year+=543
    year = str(year)
    date = time.strftime(dateformat, myset)
    #print(date,day,month,year )
    mylist = [day,month,year] 
    return "/".join(mylist)

def insert_db(Name,Surname,Tel,Time,hn,check_vt,status):
    #insert_db("สวัสดีค่ะ",patient[0][1],patient[0][2],patient[0][3],oapp_date,"11.30",oapp_contact_point,"รายละเอียดเพิ่มเติมจร๊ะ")


    # Open database connection
    db = MySQLdb.connect(####Database Pi####, use_unicode=True, charset="UTF8")
    cursor = db.cursor()
    cursor2 = db.cursor()
    num = check_vt-1
    text2=["TM","VM"]
    text=["tmessage","vmessage"]

    #sql2="SELECT max(%s_ID) FROM %s"%(text2[num],text[num])
    #sql = ("INSERT INTO %s (%s_Name,%s_Surname,%s_Tel,%s_Time,hn) VALUES ('%s','%s','%s','%s','%s')")%(text[num],text2[num],text2[num],text2[num],text2[num],Name,Surname,Tel,Time,hn)
    if(check_vt == 1):
            if(status == 1 or status ==3):
    # Prepare SQL query to INSERT a record into the database.
                sql2 = "SELECT max(TM_ID) FROM tmessage"
                cursor2.execute(sql2)
                max_id = cursor2.fetchall()
                    
            
                sql = ("INSERT INTO tmessage (TM_Name,TM_Surname,TM_Tel,TM_Time,hn) VALUES ('%s','%s','%s','%s','%s')")%(Name,Surname,Tel,Time,hn)
    
                cursor.execute(sql)
		db.commit()
		db.close()
		print "INSERT DONE"

    elif(check_vt == 2):
            if(status ==1 or status ==2):
    # Prepare SQL query to INSERT a record into the database.
                sql2 = "SELECT max(VM_ID) FROM vmessage"
                cursor2.execute(sql2)
                max_id = cursor2.fetchall()
    
                sql = ("INSERT INTO vmessage (VM_Name,VM_Surname,VM_Tel,VM_Time,hn) VALUES ('%s','%s','%s','%s','%s')")%(Name,Surname,Tel,Time,hn)
    
                cursor.execute(sql)
		db.commit()
		db.close()
		print "INSERT DONE"


def select_db(date,max_id,check_vt):
    db = MySQLdb.connect(####Database Pi####, use_unicode=True, charset="UTF8")
    
    num = check_vt-1
    text2=["TM","VM"]
    text=["tmessage","vmessage"]
    
    cursor = db.cursor()
    sql = ("SELECT * from %s where %s_Time = '%s' and %s_ID > %d")%(text[num],text2[num],date,text2[num],max_id)
    cursor.execute(sql)
    rows = cursor.fetchall()
   
    cursor.close()
    db.close()
    return rows

def select_customer(date,check_vt):


    conn =MySQLdb.connect(####Database Hospital####, use_unicode=True, charset="UTF8")
    conn3 = MySQLdb.connect(####Database Pi####, use_unicode=True, charset="UTF8")

    cur = conn.cursor()
    cur3 = conn3.cursor()

    cur3.execute("select hn,status from project_attend")
    hn_rows = cur3.fetchall()
    hn_array=[]
    hn_status=[]
    for i in range (len(hn_rows)):
        one = hn_rows[i][0]
        two = hn_rows[i][1]

        hn_array.append(str(one)),hn_status.append(str(two))
    in_p=', '.join(hn_array)
    cur.execute("select hn,nextdate,contact_point from oapp where nextdate='%s' and hn in (%s)"%(date,in_p))
    oapp = cur.fetchall()
    if (len(oapp)==0):
        return -2

    count = 1
    for i in oapp :
        oapp_date = i[1]
        oapp_contact_point = i[2]
        print "###########################"
        print "Number ",count
        count+=1
        cur2 = conn.cursor()
        cur2.execute("select hn,fname,lname,hometel from patient where hn=%s "%i[0])
        cur3.execute("select status from project_attend where hn=%s"%i[0])
        status_rows = cur3.fetchall()
        status = status_rows[0][0]
        patient = cur2.fetchall()
        #print "HR : ",patient[0][0]
        #print "Name : ",patient[0][1]
        #print "Surname: ",patient[0][2]
        #print "Phone : ",patient[0][3]
        #print "Date : ",oapp_date
        #print "Place : ",oapp_contact_point
        hn=i[0].encode('utf-8')
        fname=patient[0][1].encode('utf-8')
        lname=patient[0][2].encode('utf-8')
        if(patient[0][3]==None):
        	hometel=change_phone_number_format(patient[0][3],check_vt)#.encode('utf-8')
        else:
            hometel=change_phone_number_format(patient[0][3].encode('utf-8'),check_vt)
        nextdate=oapp_date
        
        print "\n\nDATA : " 
        print fname,lname,hometel,nextdate
        if(hometel!=0 and hometel!='0'):
       		insert_db(fname,lname,hometel,nextdate,hn,check_vt,status)
		
    cur3.close()
    cur2.close()
    cur.close()
    conn.close()

def call(rows):
    for i in range (len(rows)):
        date = re_date(rows[i][4])
        #text = ('สวัสดีค่ะคุณ').decode('utf-8')+rows[i][1]+('').decode('utf-8')+rows[i][2]+(' คุณมีนัดกับทางโรงพยาบาลแม่ทา').decode('utf-8')
        #text2 = ('วันที่ ').decode('utf-8')+date+('ค่ะ').decode('utf-8')
        #text3 = ('').decode('utf-8')+rows[i][7]+('ค่ะ').decode('utf-8')

        phone_number= rows[i][3]
        #gtts_sound_mp3(text,text2)
        print "########## R O U N D "+str(i+1)+" ##########"
        vaja_sound_mp3(rows[i][1],rows[i][2],rows[i][4])
        gsm_call(phone_number)
        
def re_date(date):
        x = date.split("-")
        year = int(x[0])
        year += 543
        
        text = x[2],x[1],str(year)
        return "/".join(text)

def send_sms(rows):
        user='thaibulksms'
        
        password='thisispassword'
        

        for i in range (len(rows)):
		#print 'in for'
                #phone= rows[i][3]
		#print rows[i][3]
		#exit()
                phone = '0850376152'
                name = rows[i][1]
                surname = rows[i][2]
                date = rows[i][4]
                print name,date,phone
                date = re_date(date)
                message = ('คุณ ').decode('utf-8')+ name +(' ').decode('utf-8')+ surname + (' ######').decode('utf-8')+ date +(' #####').decode('utf-8')
                #print message
                sender='THAIBULKSMS'

                SMS = ThaiBulkSMSAPI.ThaiBulkSMSAPI()
                a=SMS.sendMessage(user,password,phone,message,sender,'')
                print 'Phone : ',phone
                print 'Message : ',message
                print a
                print 'Status : ',a[0]
                i=0
                count=0
                for i in range(200):
                    if a[1][i] == '>' :
                        #print a[1][i]
                        #print i
                        count+=1
                        #print count
                        if count == 9 :
                            print 'UsedCredit : ',a[1][i+1]
                #exit()

def gsm_call(phone_number):
    ser = serial.Serial(port='/dev/ttyAMA0', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1)
    ch=1
    phone_number = '########'
    cmd="ATD"+phone_number+";\r\n"
    print cmd
    ser.write(cmd.encode())
    while (ch):
        time.sleep(1)
        cmd="AT+CLCC\r\n"
        ser.write(cmd.encode())
        msg = ser.read(64)
        print msg
        #print msg[21]
        if (msg.find('BUSY') != -1 or msg.find('NO CARRIER') != -1 or msg.find('NO ANSWER') != -1):
            cmd="ATH\r\n"
            ser.write(cmd.encode())
            msg = ser.read(64)
            print msg
            ch=0
            #time.sleep(5)
        elif msg[21] == '0':
            subprocess.call("sudo aplay /home/pi/Desktop/main2/Sound.wav", shell=True)
            cmd="ATH\r\n"
            ser.write(cmd.encode())
            msg = ser.read(64)
            print msg
            ch=0
    time.sleep(5)
    ser.close()
        
def gtts_sound_mp3(text,text2):
    tts = gTTS(text = text, lang='th') 
    tts.save('sound1.mp3')

    tts = gTTS(text = text2, lang='th') 
    tts.save('sound2.mp3')

    #tts = gTTS(text = text3, lang='th')
    #tts.save('sound3.mp3')
    print "gTTS Done"
def mod_day(day):
    print '###### Mod_Day ####'
    num=int(day)
    if (num<10):
        day=str(num)
    return day

def day_to_thai(day,month,year_th):
    print '###### day_to_thai ####'
    year_en=year_th-543
    date = datetime.date(year_en,month,day)
    print date
    thaiday = ["อาทิตย์","จันทร์","อังคาร","พุธ","พฤหัสบดี","ศุกร์","เสาร์"]
    pos = date.strftime("%w")
    print pos
    return thaiday[int(pos)]    
def vaja_sound_mp3(name,surname,date):
        import pycurl
	#from StringIO import StringIO
        date=re_date(date)
        realname = (name+'%20'+surname)
        text = date.split('/')
        month=('มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม')
        num=int(text[1])
        mon = month[num-1].decode('utf-8')
        #แปลงวัน 01-09 เป็น 1-9
        text[0]=mod_day(text[0])
        #แปลงวัน เป็น จันทร์ อังคาร ....
        thaiday = day_to_thai(int(text[0]),num,int(text[2]))
        thaiday_week = thaiday.decode('utf-8')
        
        before = text[0],mon,text[2]
        date = ' '.join(before)
        
        
        url = 'ติดต่อ API เพื่อส่ง SMS'
        name = {'name':realname.encode('utf-8')}
        ttime = {'date':date.encode('utf-8')}
        day_of_week = {'dayofweek':thaiday_week.encode('utf-8')}#เพิ่ม day of week
        c = pycurl.Curl()
        c.setopt(c.URL,url+'?'+urllib.urlencode(name)+'&'+urllib.urlencode(ttime)+'&'+urllib.urlencode(day_of_week))
        c.perform()
        c.close()
	#print url
        #webbrowser.open(url)
        
        time.sleep(5)
        subprocess.call("sudo cp -f /var/www/vaja/Sound.wav  /home/pi/Desktop/main2/", shell=True)
        print "Vaja Done"


#----- Main ------#
datecall = new_plus_time(time_auto_call)
datesms = new_plus_time(time_auto_sms)
print datecall,datesms
#exit()

max_sms_id = find_max_id(1)
max_call_id = find_max_id(2)
#date = function_time()
               #check_vt 1 = sms
               #check_vt 2 = call

################# Select Hospital DB ###################
select_customer(datesms,1)
select_customer(datecall,2)
########################################################

print max_call_id,max_sms_id
#exit()

if(max_call_id > -2):
    call_rows = select_db(datecall,max_call_id,2)
if(max_sms_id > -2):
    sms_rows = select_db(datesms,max_sms_id,1)
if(max_sms_id==-2):
    sms_rows = []
if(max_call_id==-2):
    call_rows = []
print (len(call_rows)),(len(sms_rows))    
#print call_rows,sms_rows
##exit()        
#for i in range (len(sms_rows)):
#    print sms_rows[i][0],sms_rows[i][1],sms_rows[i][3]

#print len(call_rows),len(sms_rows)
#exit()
if(len(call_rows) > 0):
        print '########## Calling ##########'
        call(call_rows)
if(len(sms_rows) > 0 ):
        print '########## Sending SMS ##########'
        send_sms(sms_rows)
if(len(sms_rows)==0 and len(call_rows)==0):
        print "No work to do this day"
subprocess.call("sudo python /var/www/sms/check_blance.py", shell=True)
#___ END MAIN_____#
