import mysql.connector as m
import time
conn=m.connect(host='localhost',user='root',passwd='7240')
xyz=0

if conn.is_connected():
    co=conn.cursor()

    def executer(s):
        co.execute(s)
    
    def allfetcher():
        return co.fetchall()

    def enterroomtypes():
        global roomtypes
        global noofroomspertype
        executer("create table if not exists rtypeinfo(typeroom int(2) not null , typename varchar(20),noofroomsperfloor int(2) not null ,price bigint(10) not null)")
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

    def ratelistroomtypes():
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

    def reg_staff():    
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
        m="insert into staff"+ "(st_id,st_name,st_address,st_phno,st_emailid,st_job,st_salary,st_floor) values ('{}','{}','{}',{},'{}','{}',{},{})".format(sid,s_name,s_add,s_ph,s_email,s_pos,s_salary,s_floor_allotted)
        executer(m)
        conn.commit()
        print("\nStaff member added successfully")
        time.sleep(1)
        
    def id_operator():
        s="create table if not exists counter1(cd varchar(5) not null);"   ###
        executer(s)
        j="insert into counter1(cd) values('{}')".format('ok')
        executer(j)
        conn.commit()

    def cust_details(cin,roomno):
        c_name=input("Enter name : ")
        c_add=input("Enter address : ")
        c_ph=int(input("Enter phone number : "))
        c_email=input("Enter email address : ")
        c_out=input("Enter Expected date of checkout (yyyy-mm-dd) : ")
        a=str(roomno)
        m="insert into {}(cust_name, cust_address, ph_no, c_email, Check_in_date, Expected_Checkout) values ('{}','{}',{},'{}','{}','{}')".format(a,c_name,c_add,c_ph,c_email,cin,c_out)
        executer(m)
        conn.commit()
        print()
        print("Your Room No. : "+roomno)
        print()
        print("ROOM BOOKED SUCCESSFULLY !!!")
        time.sleep(1)

    def cust_details_output():
        print("~"*90)
        print("How you want to access data?")
        print("1. Whole at once")
        print("2. Floor wise")
        print()
        os=int(input("Your choice : "))
        print()
        print()
        executer("use hotels;")
        s="select n_floors,roomperfloorpertype,roomtypes from hotel;"
        j=allfetcher()
        nr=j[0][0]*j[0][1]*j[0][2] #no. of rooms
        nf=j[0][0]
        executer("use {}".format(i_1))
        if os==1:
            data_found=0
            for i in range(1,nr+1):
                executer(str("select * from room{}".format(i)))
                k=allfetcher()
                if len(k)==0:
                    pass
                elif len(k)!=0:
                    new_var=1
                    data_found=1
                    if k[-1][-1]=='no':
                        print("\t\tThis is the data for room",i)
                        print("Customer Name|Customer Address|Phone No.|Email ID|Room Type|FLoor|Check in date|Expected checkout date|Checkout status|\n")
                        print(k[-1])
                        print()
                        print()
            if data_found==0:
                time.sleep(0.35)
                print("NO DATA FOUND")
        elif os==2:
            b=int(input("For what floor you want to access data? "))
            print()
            for i in range(1,nr+1):
                nk="select * from room{} as r Natural join floors as f where floor.f=floor.r and floor.floors={} order by room_no.floor".format(i,b)
                executer(nk)
                e=allfetcher()
                if len(e)==0:
                    print("There's no room booked at this floor right now.")
                else:
                    if e[-1][-1]=='no':
                        print("Customer Name|Customer Address|Phone No.|Email ID|Room Type|FLoor|Check in date|Expected checkout date|Checkout status|\n")
                        print(e[-1])
                        print()
                        print()            
        else:
            print("Wrong input!\nGoing back to Main Menu........")
        time.sleep(1.1)
        input("Press Enter to Continue.......")

    def staffdetailer():
        print("~"*90)
        print("How you want to access data?")
        print("1. Whole at once")
        print("2. floor wise")
        print()
        os=int(input("How you want to access data? "))
        print()
        if os==1:
            l=0
            executer("select * from staff")
            pr=allfetcher()
            for i in range(2):
                if len(pr)==0:
                    time.sleep(0.35)
                    print("No data found")
                elif len(pr)!=0 and l==0:
                    l=1
                    print("•ID|Name|Address|Phone No.|Email ID|Job|Salary|Floor alloted|")
                else:
                    print("\n•These are details of your staff")
                    for i in pr:
                        st1=''
                        for j in i:
                            st1=st1+str(j)+' | '
                        print('→',st1)
                
        elif os==2:
            llll=str(int(input("For which floor you would like to fetch data? : ")))
            executer("select st_id, st_name, st_address, st_phno, st_emailid, st_job, st_salary from staff where st_floor="+llll+';')
            pr=allfetcher()
            if len(pr)==0:
                print("No data found")
            else:
                count=0
                print("\nThese are details of your staff which works on floor number "+llll)
                print("•ID|Name|Address|Phone No.|Email ID|Job|Salary|\n")
                while count<len(pr):
                    st2=''
                    for i in pr[count]:
                        st2=st2+str(i)+' | '
                    print('→',st2)
                    count+=1
                
        time.sleep(1.15)
        input("\n\nPress Enter to Continue.......")

    def checkout():
        co_room=int(input("Enter customer's room no. : "))
        ph=int(input("Enter customer's mobile number"))
        executer("select * from room{}".format(co_room))
        f=allfetcher()
        executer("select curdate()")
        kl=allfetcher()
        cdate=kl[0][0]
        n=0
        for i in f:
            if i[-1]=="no":
                id=i[-3]
                rt=i[4]
                executer("select datediff({},{})".format(kl,cdate))
                diff=allfetcher()
                ap=diff*roomd[rt]
                u="update room{} set checkoutdone='yes' where ph_no={}".format(co_room,ph)
                executer("insert into past_visitors(ph_no, Check_in_date, Expected_Checkout, Amount_payed, checkoutdate) values({},'{}','{}',{},'{}')".format(ph,i[-3],i[-2],ap,cdate))
                conn.commit
                break
            else:
                n=n+1
        executer(u)
        if n!=0:
            time.sleep(0.5)
            print("Entered deails of checkout are unmatched to current records")
            time.sleep(1)
            print("Returning to main menu.....")
            input("press enter to continue")
            return()
        time.sleep(0.5)
        print("\n\nCheckout Successful")
        time.sleep(1)
        input("Press Enter to Continue.......")

    def go_to_cust_details(x,y):   #To avoid unnecessary repetition of code block
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
                        date = f[0]
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

    def key_change():
        new_key=input("Enter new Master Key : ")
        executer("update pass set passw='{}' where userid='{}' ".format(new_key,'Master_key'))
        conn.commit()
        print("Master Key updated Successfully!\n")
        print("Redirecting to login screen.........")
        time.sleep(1)

    def passcreater(key12): 
        if key12=="147258369":
            s="create table if not exists pass(login_type varchar(20) not null , userid varchar(20) not null unique primary key , passw varchar(25) not null);"   ###
            executer(s)    
            try:
                t=i_1
                u='Master_key'
                p='147258369'
                executer("insert into pass(login_type , userid , passw) values('{}','{}','{}')".format(t,u,p))
                conn.commit()
                t='Manager'
                u='Manag1010'
                p='1010m'
                executer("insert into pass(login_type , userid , passw) values('{}','{}','{}')".format(t,u,p))
                conn.commit()
                t='Receptionist'
                u='Recep1010'
                p='1010r'
                executer("insert into pass(login_type , userid , passw) values('{}','{}','{}')".format(t,u,p))
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
            
    def passupdater(key):
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
                    print("\n\nChanging Userid first")
                    j1=input("Enter new user name for Manager : ")
                    executer("update pass set userid = '{}' where login_type = '{}'".format(j1,'Manager'))
                    conn.commit()
                    print("\nNow updating password")
                    j2=input("Enter new password for Manager : ")
                    executer("update pass set passw = '{}' where login_type = '{}'".format(j2,'Manager'))
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
                    print("\n\nChanging Userid first\n")
                    j1=input("Enter new user name for Receptionist : ")
                    executer("update pass set userid = '{}' where login_type = '{}'".format(j1,'Receptionist'))
                    conn.commit()
                    print("\nNow updating password")
                    j2=input("Enter new password for Receptionist : ")
                    executer("update pass set passw = '{}' where login_type = '{}'".format(j2,'Receptionist'))
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
        executer("select userid from pass where login_type='Manager';")    ####
        k=allfetcher()
        executer("select passw from pass where login_type='Manager' ;")    ####
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
        executer("select userid from pass where login_type='Manager';")    ####
        k=allfetcher()
        executer("select passw from pass where login_type='Manager' ;")    ####
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
            print("You can restart system anytime by same interface, just type initiation() on command line")  #### initiation() use karne wali line add kar apne according, iss statement ke bracket ke andar hi.
        else:
            print("Select Valid option")
            login()

    def updatestaffdetails():
        x=input("Enter staff id for which you want to change existing details : ")
        print("\nFor What field you want to update details for "+x)
        print("1) Name, 2) Address, 3) Phone number, 4) Email id, 5) Job, 6) Sallary, 7) Floor\n")
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
        else:
            print("\nSelect appropriate option!!")
            updatestaffdetails()
        a=input("\nEnter updated value for "+m+" : ")
        fc="update staff set "+o+"='{}' where st_id='{}'".format(a,x)
        executer(fc)
        conn.commit()
        print("\n\nStaff Details Updated Sucessfully")
        time.sleep(0.5)
        input("Press Enter to continue.........")
        
    def setprice():
        executer("use hotels;")
        executer("select * from hotel;")
        k=allfetcher()
        c=k[0][2]
        global roomd
        roomd={}
        print("These are the room types")
        print("1) Dulex Room\t\t \t2) Dulex Room (AC)\n3) Regular Room\t\t \t4) Regular Room (AC)\n5) Luxary 5 Star Room (AC)")
        for i in c:
           mk=input("Enter price for room "+i+": ")
           roomd[i]=mk
        global roomn
        roomn={}
        for i in c:
            if i==1:
                roomn[1]='Dulex Room'
            elif i==2:
                roomn[2]='Dulex Room (AC)'
            elif i==3:
                roomn[3]='Regular Room'
            elif i==4:
                roomn[4]='Regular Room (AC)'
            elif i==5:
                roomn[5]='Luxary 5 Star Room (AC)'
        executer("use {}".format(i_1))

    def prevv():
        executer("use hotels;")
        executer("select * from hotel;")
        k=allfetcher()
        n=0
        for i in range(1,k[0][0]+1):
            for j in range(1,1+k[0][1]):
                for l in k[0][2]:
                    n=n+1
        executer("use "+i_1+";")
        for i in range(1,1+n):
            executer("select * from past_visitor natural join room"+str(i)+"where ph_no.past visitor=ph_no.room"+str(i)+";")
            dick=allfetcher()
            for i in dick:
                print(i)

    def manager():
        print('~'*90)
        print('\t\t\tMAIN MENU')
        print()
        print("Welcome Manager")
        print()
        print("\t1)Customer Details.\t\t2)Register Staff Member. \n\t3)Staff members' details \t\t4) Update Staff Details \n\t5)Set/Update Price List for rooms   \t6) Logout \n\t7) Master key \t\t8) old customer data fetcher")
        print()
        ch1 = int(input("Select your choice  :  "))
        try:
            if(ch1 == 1):
                cust_details_output()
                manager()
            elif (ch1==2):
                reg_staff()
                manager()
            elif ch1==3:
                staffdetailer()
                manager()
            elif ch1==4:
                updatestaffdetails()
                manager()
            elif ch1==5:
                setprice()
                manager()
            elif(ch1 ==6):
                print()
                print()
                print('~'*90)
                print('You have been logged out')
                login()
            elif ch1==7:
                time.sleep(0.7)
                executer("select passw from pass where userid='Master_key';")
                print("\nMaster key is → "+allfetcher()[0][-1]+"\n")
                print("Do you wish to change  Master Key? \n\t1)Yes\n\t2)No, proceed further.")
                i_key=input("\nYour choice : ")
                if i_key=='2':
                    time.sleep(1)
                    pass
                elif i_key!='1' and i_key!='2':
                    print("Wrong input!\nGoing back to Main Menu........")
                    time.sleep(1)
                    pass
                else:
                    key_change()
                manager()
            elif ch1==8:
                prevv()
                manager()
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
        print('\t\t\tMAIN MENU')
        print()
        print("Welcome receptionist")
        print()
        print("\t1) CheckIn.\t\t2) Customer Details\n\t3) CheckOut\t\t4) Logout")
        print()
        ch1 = int(input("  select your choice  :  "))
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
    
    def hoteldata():
        i_2='create database '+i_1+';'        
        executer(i_2)
        executer("use "+i_1+";")
        time.sleep(1)
        print("\n It seems you are entering details for a new hotel, so you've been redirected here .......")
        time.sleep(1.1)
        print("\n\tEnter the following details so that we can create database for your hotel"+i_1)
        global i_ques2, rno
        i_ques2=int(input("Enter number of floors in your hotel : "))
        enterroomtypes()
        i_3="create table if not exists floors(floor int(3) not null , room_no varchar(5) not null);"
        executer(i_3)
        executer("select * from rtypeinfo")
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
                    d="insert into floors(floor,room_no) values('{}','{}')".format(str(i),rno)
                    executer(d)
        i_5="create table if not exists staff"
        i_6=" (st_id varchar(3) not null primary key, st_name varchar(20) not null,st_address longtext not null, st_phno bigint(20) not null unique, st_emailid varchar(100) not null unique, st_job varchar(20) not null,st_salary int(9) not null,st_floor int(4) not null);"
        s=i_5+i_6
        executer(s)
        executer("create table past_visitors (ph_no bigint(15) not null unique, Check_in_date date,Amount_paid bigint(10), Expected_checkout date, checkoutdate date);")

    def initiation():
        executer("create database if not exists hotels;")
        executer("Use hotels;")
        #executer("create table if not exists hotel (hotel_name varchar(15) NOT NULL)")
        key=147258369
        print('~'*90)
        print("\t\t\tWelcome to Hotel Management System")
        print('~'*90)
        start=input("Would you like to begin the system (y/n): ")
        print('~'*90)
        if start[0].lower()=='y':
            print("Initiating System")
            time.sleep(1)
        else:
            print('~'*90)
            print("You can restart system anytime by same interface, just type initiation() on command line")
            print('~'*90)
            print("Thanks for Service")
            return("")
        global i_1
        i_1=input("Enter your Hotel's name : ")                      # Hotel name take any!!!
        try:
            co.execute("use "+i_1+";")
        except:
            hoteldata()
        login()
    initiation()