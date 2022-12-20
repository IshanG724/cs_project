import mysql.connector as m
import time
from datetime import date
conn=m.connect(host='localhost',user='root',passwd='7240')
xyz=0

if conn.is_connected():
    co=conn.cursor()

    def executer(s):    #To execute all mysql commands
        co.execute(s)
    
    def allfetcher():   #To fetch data from executed commands
        return co.fetchall()

    def diff_dates(date1, date2):   #Get difference of 2 dates in days, for billing
        d1=date(int(date1[:4] ),int(date1[5:7]),int(date1[8:]))
        d2=date(int(date2[:4]),int(date2[5:7]),int(date2[8:]))
        return abs(d2 - d1).days

    def enterroomtypes():   #For registering types of rooms available in the hotel
        global roomtypes
        global noofroomspertype
        #Table for storing structure of room types in hotel
        executer("create table if not exists rtypeinfo(typeroom int(2) not null , typename varchar(20),noofroomsperfloor int(2) not null ,price bigint(10) not null);")
        print('\nEnter the details for roomtypes available in your hotel\nType "none" when done\n')
        counter=1
        while True:
            ip=input("Room type #"+str(counter)+" : ")
            if ip=="none":
                break
            ip2=int(input("No. of rooms per floor for room type \""+ip+"\" : "))
            ip3 = int(input("Per day charges of Room type \""+ip+"\" (in Rs): "))
            s="insert into rtypeinfo(typeroom,typename,noofroomsperfloor,price) values({},'{}',{},{});".format(counter,ip,ip2,ip3)
            executer(s)
            counter+=1

    def ratelistroomtypes():    #To print current rate list
        executer("select * from rtypeinfo;")
        k=allfetcher()
        counter2=1          # just for beauty of o/p
        for i in k:
            j,k,l=i[0],i[1],i[3]
            if counter2%3==0:
                print(str(j)+") "+k+" --> "+str(l),end="\n")
            else:
                print(str(j)+") "+k+" --> "+str(l),end='\t')
            counter2+=1

    def reg_staff():    #Add new working staff
        s_name=input("Enter staff member's name : ")
        s_ph=int(input("Enter staff member's phone number : "))
        s_add=input("Enter staff member's permanent residential address : ")
        s_email=input("Enter email id : ")
        s_pos=input("Enter his/her job : ")
        s_salary=int(input("Salary : "))
        s_floor_allotted=int(input("Enter floor allotted to staff member : "))
        id_operator()
        executer('select * from counter1;')
        check=allfetcher()
        sid="S"+str(len(check))
        executer("insert into staff (st_id,st_name,st_address,st_phno,st_emailid,st_job,st_salary,st_floor) values ('{}','{}','{}',{},'{}','{}',{},{});".format(sid,s_name,s_add,s_ph,s_email,s_pos,s_salary,s_floor_allotted))
        conn.commit()
        print("\nStaff member added successfully")
        time.sleep(1)
        
    def id_operator():  #Used to create staff id
        s="create table if not exists counter1(cd varchar(5) not null);"
        executer(s)
        j="insert into counter1(cd) values('{}');".format('ok')
        executer(j)
        conn.commit()

    def cust_details(cin,roomno):   #Input details of customer for checkin
        c_name=input("Enter name : ")
        c_add=input("Enter address : ")
        c_ph=int(input("Enter phone number : "))
        c_email=input("Enter email address : ")
        c_out=input("Enter Expected date of checkout (yyyy-mm-dd) : ")
        a=str(roomno)
        m="insert into {}(cust_name, cust_address, ph_no, c_email, Check_in_date, Expected_Checkout) values ('{}','{}',{},'{}','{}','{}');".format(a,c_name,c_add,c_ph,c_email,cin,c_out)
        executer(m)
        conn.commit()
        print()
        print("Your Room No. : "+roomno)
        print()
        print("ROOM BOOKED SUCCESSFULLY !!!")
        time.sleep(1)

    def cust_details_output():  # Get output of data of customers currently in hotel
        print("~"*90)
        print("How you want to access data?")
        print("1. Whole at once")
        print("2. Floor wise")
        print("3. Particular room")
        print()
        os=int(input("Your choice : "))
        if os==1:
            print()
            print()
            executer("select room_no from floors;")
            rooms=allfetcher()
            data_found=0
            for i in rooms:
                executer("select * from {} ;".format(i[0]))
                roomdata=allfetcher()
                if len(roomdata) == 0:
                    pass
                for r in roomdata:
                    if r[-1]=='no':
                        if data_found==0:
                            print("•Customer Name|Customer Address|Phone No.|Email ID|Room Type|FLoor|Check in date|Expected checkout date|Checkout status|\n")
                            data_found=1
                        st1=''
                        for j in r:
                            st1 = st1 + str(j) + ' | '
                        print(str(i[0])+' →', st1)
            if data_found==0:
                time.sleep(0.35)
                print("NO DATA FOUND")
        elif os==2:
            b=int(input("\nFor what floor you want to access data? "))
            print()
            executer("select room_no from floors where floor={};".format(b))
            rooms = allfetcher()
            data_found = 0
            for i in rooms:
                executer("select * from {} ;".format(i[0]))
                roomdata = allfetcher()
                if len(roomdata) == 0:
                    pass
                for r in roomdata:
                    if r[-1] == 'no':
                        if data_found == 0:
                            print("•Customer Name|Customer Address|Phone No.|Email ID|Room Type|FLoor|Check in date|Expected checkout date|Checkout status|\n")
                            data_found = 1
                        st1 = ''
                        for j in r:
                            st1 = st1 + str(j) + ' | '
                        print(str(i[0]) + ' →', st1)
            if data_found == 0:
                time.sleep(0.35)
                print("There's no room booked at this floor right now.")
        elif os==3:
            b=input("For what room you want to access data? ")
            print()
            executer("select * from {} ;".format(b))
            roomdata = allfetcher()
            if len(roomdata) == 0:
                print("Room hasn't been booked yet!")
            else:
                data_found=0
                for r in roomdata:
                    if r[-1] == 'no':
                        if data_found == 0:
                            print("•Customer Name|Customer Address|Phone No.|Email ID|Room Type|FLoor|Check in date|Expected checkout date|Checkout status|\n")
                            data_found = 1
                        st1 = ''
                        for j in r:
                            st1 = st1 + str(j) + ' | '
                        print(b + ' →', st1)
                if data_found == 0:
                    time.sleep(0.35)
                    print("There's no room booked at this floor right now.")
        else:
            print("Wrong input!\nGoing back to Main Menu........")
        time.sleep(1.1)
        input("Press Enter to Continue.......")

    def staffdetailer():    #Get data of current working staff
        print("~"*90)
        print("How you want to access data?")
        print("1. Whole at once")
        print("2. Floor wise")
        print("3. Particular Staff Member")
        print()
        os=int(input("How you want to access data? "))
        print()
        if os==1:
            l=0
            executer("select * from staff;")
            pr=allfetcher()
            for i in range(2):
                if len(pr)==0:
                    time.sleep(0.35)
                    print("No data found")
                    break
                elif len(pr)!=0 and l==0:
                    l=1
                    print("•ID|Name|Address|Phone No.|Email ID|Job|Salary|Floor allotted|")
                else:
                    print("\n•These are details of your staff")
                    for i in pr:
                        st1=''
                        for j in i:
                            st1=st1+str(j)+' | '
                        print('→',st1)
                
        elif os==2:
            llll=str(int(input("For which floor you would like to fetch data? : ")))
            executer("select st_id, st_name, st_address, st_phno, st_emailid, st_job, st_salary from staff where st_floor={};".format(llll))
            pr=allfetcher()
            if len(pr)==0:
                print("No data found")
            else:
                count=0
                print("\nThese are details of your staff which works on floor number "+llll+"\n")
                print("•ID|Name|Address|Phone No.|Email ID|Job|Salary|\n")
                while count<len(pr):
                    st2=''
                    for i in pr[count]:
                        st2=st2+str(i)+' | '
                    print('→',st2)
                    count+=1
        elif os==3:
            llll = str(input("Enter Staff ID : "))
            executer("select st_name, st_address, st_phno, st_emailid, st_job, st_salary,st_floor from staff where st_id={};".format(llll))
            pr = allfetcher()
            print("\nThese are details of staff member " + llll + "\n")
            print("•ID|Name|Address|Phone No.|Email ID|Job|Salary|\n")
            st2 = ''
            for i in pr[0]:
                st2 = st2 + str(i) + ' | '
            print('→', st2)
        else:
            print("Wrong input!\nGoing back to Main Menu........")
        time.sleep(1)
        input("\n\nPress Enter to Continue.......")
        return()

    def checkout():
        co_room=input("Enter customer's room no. : ")
        ph=int(input("Enter customer's mobile number"))
        executer("select * from {} where ph_no={};".format(co_room,ph))
        f1=allfetcher()
        if len(f1)==0:
            time.sleep(0.5)
            print("Entered details of checkout are unmatched to current records")
            time.sleep(1)
            print("Returning to Main Menu")
            input("Press enter to continue........")
            return ()
        f=f1[0]
        executer("select curdate();")
        cdate=str(allfetcher()[0][0])
        if f[-1] == "no":
            cindate = str(f[-3])
            diff=diff_dates(cindate,cdate)
            diff+=1
            executer("select price from rtypeinfo where typeroom={};".format(int(co_room[-2])))
            billamt = diff * allfetcher()[0][0]
            executer("update {} set checkoutdone='yes' where ph_no={};".format(co_room, ph))
            executer("insert into past_visitors(ph_no, Check_in_date, Amount_paid, Expected_Checkout, checkoutdate) values({},'{}',{},'{}','{}');".format(ph,f[-3],billamt,f[-2],cdate))
            conn.commit()
            print("\nTotal Amount to be paid by the customer : ",billamt,"\n")
        else:
            time.sleep(0.5)
            print("Checkout of the Customer with the above entered details has already been done")
            time.sleep(1)
            print("Returning to Main Menu")
            input("Press enter to continue........")
            return ()
        time.sleep(0.5)
        print("\n\nCheckout Successful")
        time.sleep(1)
        input("Press Enter to Continue.......")
        return()

    def go_to_cust_details(x,y):   #To avoid unnecessary repetition of code block in checkin
        cust_details(x,y)
        print()
        input('Press Enter to continue.........\n')
        receptionist()

    def checkin():
        time.sleep(1)
        print('~'*90)
        print("\t\t\t\tRATE LIST")
        ratelistroomtypes()
        print("\n\n")
        i_ques3=input("Enter the type of room customer is looking for : ")
        i_ques4=input("Enter the floor customer want a room at. : ")
        c_date=input("Enter Check in Date in format yyyy-mm-dd : ")
        y=int(c_date[0:4])
        m=int(c_date[5:7])
        d=int(c_date[8:10])
        executer("select * from floors where floor='{}';".format(i_ques4))
        c=allfetcher()
        for i in c:
            if i[1][-2]==i_ques4:
                executer("select Expected_Checkout, checkoutdone from {};".format(i[-1]))
                f1 = allfetcher()
                if len(f1)==0:
                    go_to_cust_details(c_date, i[-1])
                else:
                    for f in f1:
                        date = str(f[0])
                        yy = int(date[0:4])
                        mm = int(date[5:7])
                        dd = int(date[8:10])
                        cd = f[1]
                    if y > yy:
                        go_to_cust_details(c_date, i[-1])
                    elif m > mm:
                        go_to_cust_details(c_date, i[-1])
                    elif d > dd:
                        go_to_cust_details(c_date, i[-1])
                    elif cd == 'yes':
                        go_to_cust_details(c_date, i[-1])
        else:
            time.sleep(1.2)
            print("Rooms of such requirements are not available")
            time.sleep(0.3)
            print("please search for another room type or floor or for another checkin date")
            time.sleep(1)
            input("press enter to continue.............")
            checkin()

    def key_change():   #To Update master key
        new_key=input("Enter new Master Key : ")
        executer("update pass set passw='{}' where userid='{}' ;".format(new_key,'Master_key'))
        conn.commit()
        print("\n\nMaster Key updated Successfully!\n")
        print("Redirecting to login screen.........")
        time.sleep(1)

    def passcreater(key12): # To create initial logins for hotel
        if key12=="147258369":
            s="create table if not exists pass(login_type varchar(20) not null , userid varchar(20) not null unique primary key , passw varchar(25) not null);"
            executer(s)    
            try:
                t=i_1
                u='Master_key'
                p='147258369'
                executer("insert into pass(login_type , userid , passw) values('{}','{}','{}');".format(t,u,p))
                conn.commit()
                t='Manager'
                u='Manag1010'
                p='1010m'
                executer("insert into pass(login_type , userid , passw) values('{}','{}','{}');".format(t,u,p))
                conn.commit()
                t='Receptionist'
                u='Recep1010'
                p='1010r'
                executer("insert into pass(login_type , userid , passw) values('{}','{}','{}');".format(t,u,p))
                conn.commit()
                print("~"*90)
                print("Initial Credentials created, if you wish to cahange the credentials choose update credentials in the login screen")
                print("Redirecting to login screen.........")
                time.sleep(1)
            except :
                print("Credentials already created. You may proceed to login to your system or update credentials.")
                print("Redirecting to login screen.........")
                time.sleep(1)
            login()
        else:
            print("\t\t\tMaster key invalid")
            print("Redirecting to login screen........")
            time.sleep(1)
            login()
            
    def passupdater(key):   #To change/update logins
        global xyz
        print("\n"+"~"*90)
        executer("select passw from pass where userid='Master_key';")
        if key==allfetcher()[0][-1]:
            print("\nFor which login_type you want to update credentials? : ")
            print("1. Manager")
            print("2. Receptionist\n")
            i=int(input("Your choice : "))
            print()
            if i==1:
                a=input("Enter old user name : ")
                b=input("Enter old Password : ")
                passcheckerm(a,b)
                if xyz == 1:
                    j1=input("Enter new user name for Manager : ")
                    executer("update pass set userid = '{}' where login_type = '{}';".format(j1,'Manager'))
                    conn.commit()
                    j2=input("Enter new password for Manager : ")
                    executer("update pass set passw = '{}' where login_type = '{}';".format(j2,'Manager'))
                    conn.commit()
                    xyz=0
                print("\nUser ID and Password successfully changed!")
                print("Redirecting to login screen........")
                time.sleep(1)
                    
            elif i==2:
                a=input("Enter old user name : ")
                b=input("Enter old Password : ")
                passcheckerr(a,b)
                if xyz==6:
                    j1=input("Enter new user name for Receptionist : ")
                    executer("update pass set userid = '{}' where login_type = '{}';".format(j1,'Receptionist'))
                    conn.commit()
                    j2=input("Enter new password for Receptionist : ")
                    executer("update pass set passw = '{}' where login_type = '{}';".format(j2,'Receptionist'))
                    conn.commit()
                    xyz=0
                print("\nUser ID and Password successfully changed!")
                print("Redirecting to login screen........")
                time.sleep(1)
            else:
                print("Wrong input!\nRedirecting to login screen........")
                time.sleep(1)
            login()
        else:
            print("\t\t\tMaster key invalid")
            print("Redirecting to login screen........")
            time.sleep(1)
            print()
            login()

    def passcheckerm(a,b):
        executer("select userid from pass where login_type='Manager';")
        k=allfetcher()
        executer("select passw from pass where login_type='Manager' ;")
        r=allfetcher()
        if a==k[0][0] and b==r[0][0]:
            global xyz
            xyz=1
        else:
            print("\nPassword and User ID combination are inappropriate")
            print("Redirecting to Login Screen\n")
            time.sleep(1)
            login()

    def passcheckermcall(a,b):
        executer("select userid from pass where login_type='Manager';")
        k=allfetcher()
        executer("select passw from pass where login_type='Manager' ;")
        r=allfetcher()
        if a==k[0][0] and b==r[0][0]:
            manager()
        else:
            print("\nPassword and User ID combination are inappropriate")
            print("Redirecting to Login Screen\n")
            time.sleep(1)
            login()
            
    def passcheckerr(a,b):
        executer("select userid from pass where login_type='Receptionist';")
        k=allfetcher()
        executer("select passw from pass where login_type='Receptionist';")
        r=allfetcher()
        print(k[0][0])
        if a==k[0][0] and b==r[0][0]:
            global xyz
            xyz=6
        else:
            print("\nPassword and User ID combination are inappropriate")
            print("Redirecting to Login Screen\n")
            time.sleep(1)
            login()

    def passcheckerrcall(a,b):
        executer("select userid from pass where login_type='Receptionist';")
        k=allfetcher()
        executer("select passw from pass where login_type='Receptionist';")
        r=allfetcher()
        if a==k[0][0] and b==r[0][0]:
            receptionist()
        else:
            print("\nPassword and User ID combination are inappropriate")
            print("Redirecting to Login Screen\n")
            time.sleep(1)
            login()       

    def removestaff():
        x = input("Enter staff id to be removed : ")
        executer("delete from staff where st_id='{}';".format(x))
        print("\nStaff member successfully removed from records.\n")

    def updatestaffdetails():
        x=input("Enter staff id for which you want to change existing details : ")
        print("\nFor What field you want to update details for "+x)
        print("1) Name, 2) Address, 3) Phone number, 4) Email id, 5) Job, 6) Salary, 7) Floor 8)Main Menu\n")
        y=int(input("Select from the above given options for which field you want to change details : "))
        o=""
        if y==1:
            o,m="st_name","Name"
        elif y==2:
            o,m="st_address","Address"
        elif y==3:
            o,m="st_phno","Ph No."
        elif y==4:
            o,m="st_emailid","Email ID"
        elif y==5:
            o,m="st_job","Job"
        elif y==6:
            o,m="st_salary","Salary"
        elif y==7:
            o,m="st_floor","Floor Allotted"
        elif y==8:
            manager()
        else:
            print("\nSelect appropriate option!!")
            updatestaffdetails()
        a=input("\nEnter updated value for "+m+" : ")
        fc="update staff set "+o+"='{}' where st_id='{}';".format(a,x)
        executer(fc)
        conn.commit()
        print("\n\nStaff Details Updated Sucessfully")
        time.sleep(0.5)
        input("Press Enter to continue.........")
        
    def setprice():
        executer("select * from rtypeinfo;")
        d1=allfetcher()
        print("Current Rate List")
        ratelistroomtypes()
        print("\n\n")
        for i in d1:
            m=int(input("Enter updated price for room type "+i[1]+" : "))
            executer("update rtypeinfo set price={} where typeroom={};".format(m,i[0]))
            conn.commit()
        print("\nRate List updated successfully.\n")
        time.sleep(1)
        input("Press Enter to Continue.......")
        return ()

    def prevv():
        executer("select room_no from floors;")
        k=allfetcher()
        df=0
        for i in k:
            executer("select * from "+str(i[0])+" natural join past_visitors where past_visitors.ph_no="+str(i[0])+".ph_no ;")
            k1=allfetcher()
            if len(k1)==0:
                pass
            df=1
            for r in k1:
                st1 = ''
                for j in r:
                    st1 = st1 + str(j) + ' | '
                print('→', st1)
        if df==0:
            print("NO DATA FOUND")
        time.sleep(0.4)
        input("\nPress enter to continue......")
        time.sleep(1)
        return

    def master_key():
        time.sleep(0.7)
        executer("select passw from pass where userid='Master_key';")
        print("\nMaster key is → " + allfetcher()[0][-1] + "\n")
        print("Do you wish to change  Master Key? \n\t1)Yes\n\t2)No")
        i_key = input("\nYour choice : ")
        if i_key == '2':
            time.sleep(1)
        elif i_key != '1' and i_key != '2':
            print("Wrong input!\nGoing back to Main Menu........")
            time.sleep(1)
        else:
            key_change()

    def manager():
        print('~'*90)
        print('\t\t\t\t\tMAIN MENU')
        print("\t\t\t\tWelcome Manager")
        print()
        counter2 = 1
        # spaces below are just for beauty of o/p
        k={1:"Register Staff Member.    ",2:"Update Staff Data.",3:"Update Rate List of rooms.",4:"Remove Staff Member.",5:"Current Staff Data.       ",6:"Current Customers' Data.",7:"Past Visitors' Records.   ",8:"Master key.",9:"Logout."}
        for i in k:
            if counter2 % 2 == 0:
                print(str(i) + ") " + k[i] , end="\n")
            else:
                print(str(i) + ") " + k[i] , end='\t\t')
            counter2 += 1
        print("\n")
        ch1 = int(input("Select your choice  :  "))
        try:
            if(ch1 == 1):
                reg_staff()
                manager()
            elif (ch1==2):
                updatestaffdetails()
                manager()
            elif ch1==3:
                setprice()
                manager()
            elif ch1==4:
                removestaff()
                manager()
            elif ch1==5:
                staffdetailer()
                manager()
            elif(ch1 ==6):
                cust_details_output()
                manager()
            elif ch1==7:
                prevv()
                manager()
            elif ch1==8:
                master_key()
                manager()
            elif ch1==9:
                print()
                print()
                print('~' * 90)
                print('You have been logged out')
                login()
            else:
                print("INVALID INPUT !! TRY AGAIN !!\n")
                manager()
        except Exception as e:
            print(e)
            print("~"*90)
            print("ERROR! GOING BACK TO MAIN MENU")
            time.sleep(1)
            manager()

    def receptionist():
        print('~'*90)
        print('\t\t\t\t\t\t\t\tMAIN MENU')
        print("\t\t\t\t\t\tWelcome Receptionist")
        print()
        print("\t1) CheckIn.\t\t2) Customers' Data.\t\t3) CheckOut.\t\t4) Logout.")
        print()
        ch1 = int(input("Select your choice  :  "))
        try:
            if(ch1 == 1):
                checkin()
                receptionist()
            elif (ch1 == 2):
                cust_details_output()
                receptionist()
            elif(ch1 == 3):
                checkout()
                receptionist()
            elif(ch1 ==4):
                print()
                print()
                print('~'*90)
                print('You have been logged out')
                login()
            else:
                print("INVALID INPUT !! TRY AGAIN !!\n")
                receptionist()
        except Exception as e:
            print(e)
            print("~"*90)
            print("ERROR! GOING BACK TO MAIN MENU")
            time.sleep(1)
            receptionist()

    def login():
        print('~'*90)
        print("\t\t\t\t\t","Hotel",i_1.upper())
        print("\t\t\t\tWelcome to Login Screen")
        print('~'*90)
        print("\t\tChoose any from the folloing options using their number assigned")
        print("\t\t\t1. Manager")
        print("\t\t\t2. Receptionist")
        print("\t\t\t3. Create logins")
        print("\t\t\t4. Update logins")
        print("\t\t\t5. Exit System")
        log=int(input("Enter your choice : "))
        if log==1:
            a=input("Enter user name : ")
            b=input("Enter Password : ")
            passcheckermcall(a,b)
        elif log==2:
            a=input("Enter user name : ")
            b=input("Enter Password : ")
            passcheckerrcall(a,b)
        elif log==3:
            j=input("Enter the Product Key for this system : ")  #Product key coz master key isn't defined yet.
            passcreater(j)
        elif log==4:
            j=input("Enter Master key for this system : ")
            passupdater(j)        
        elif log==5:
            print()
            print('~'*90)
            print("\t\t\tThanks for service")
            print("You can restart system anytime by same interface, just type initiation() on command line")
        else:
            print("Select Valid option")
            login()
    
    def hoteldata():
        i_2='create database '+i_1+';'        
        executer(i_2)
        executer("use "+i_1+";")
        time.sleep(1)
        print("\nIt seems you are entering details for a new hotel, so you've been redirected here .......")
        time.sleep(1.1)
        print("\nEnter the following details so that we can create database for your hotel : "+i_1)
        global i_ques2, rno
        i_ques2=int(input("\nEnter number of floors in your hotel : "))
        enterroomtypes()
        i_3="create table if not exists floors(floor int(3) not null , room_no varchar(5) not null);"
        executer(i_3)
        executer("select * from rtypeinfo;")
        y=allfetcher()
        for i in range (1,i_ques2+1):
            for e in y:
                tmp=e[2]
                a=1
                while tmp!=0:
                    rno="R"+str(i)+str(e[0])+str(a)
                    s="create table "+rno+"(cust_name varchar(20), cust_address longtext, ph_no bigint(20) unique, c_email varchar(100) unique, Check_in_date date, Expected_Checkout date, checkoutdone varchar(5) default 'no');"
                    executer(s)  # room name = floor+type+number --> Ex --> R321 = 3rd floor, type 2 , 1st room out of noofroomsperfloor available
                    a+=1
                    tmp-=1
                    d="insert into floors(floor,room_no) values('{}','{}');".format(str(i),rno)
                    executer(d)
        i_5="create table if not exists staff"
        i_6=" (st_id varchar(3) not null primary key, st_name varchar(20) not null,st_address longtext not null, st_phno bigint(20) not null unique, st_emailid varchar(100) not null unique, st_job varchar(20) not null,st_salary int(9) not null,st_floor int(4) not null);"
        s=i_5+i_6
        executer(s)
        executer("create table past_visitors (ph_no bigint(15) not null unique, Check_in_date date,Amount_paid bigint(10), Expected_checkout date, checkoutdate date);")

    def initiation():
        key=147258369
        print('~'*90)
        print("\t\t\tWelcome to Hotel Management System")
        print('~'*90)
        start=input("Would you like to begin the system (y/n): ")
        print('~'*90)
        if start[0].lower()=='y':
            print("Initiating System")
            print('~'*90)
            time.sleep(0.3)
        else:
            print('~'*90)
            print("You can restart system anytime by same interface, just type initiation() on command line")
            print('~'*90)
            print("Thanks for Service")
            return("")
        global i_1
        i_1=input("Enter your Hotel's name : ")
        try:
            co.execute("use "+i_1+";")
        except:
            hoteldata()
        login()
    initiation()
