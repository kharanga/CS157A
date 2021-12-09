import mysql.connector
from helper import *
from datetime import date

class Database:
    def __init__(self, host, user, password, database):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
        )
        try:
            self.db = mysql.connector.connect(
                host=host,
                user=user,
                passwd=password,
                database=database
            )
        except:
            self.db = mysql.connector.connect(
                host=host,
                user=user,
                passwd=password,
            )
            self.cursor = self.db.cursor()
            for line in open('setup.sql', encoding="us-ascii"):
                self.cursor.execute(line)
            self.db.commit()
            self.db = mysql.connector.connect(
                host=host,
                user=user,
                passwd=password,
                database=database
            )
        self.cursor = self.db.cursor()

    def registerStudent(self):
        print("— — — Student Registration — — — \n")
        firstName = input("Enter student firstName : ")
        lastName = input("Enter student lastName : ")
        email = input("Enter student email : ")
        validEmail = checkEmail(email)
        if(validEmail == False):
        		print("Email entered is invalid")
        		return 
        sql = "INSERT INTO `Student` (`Student_First_Name`,`Student_Last_Name`,`Student_Email`) VALUES (%s,%s,%s)"
        val = (firstName,lastName,email)
        try: 
        		self.cursor.execute(sql,val)
        except:
            print("Student already registered in the system.\n")
            return
        self.db.commit()
        print("— — — SUCCESS — — — \n")

    def registerTutor(self):
        print("— — — Tutor Registration — — — \n")
        firstName = input("Enter tutor first name : ")
        lastName = input("Enter tutor last name : ")
        email = input("Enter tutor email : ")
        validEmail = checkEmail(email)
        if(validEmail == False):
        		print("Email entered is invalid")
        		return 
        sql = "INSERT INTO `Tutor` (`Tutor_First_Name`,`Tutor_Last_Name`,`Tutor_Email`) VALUES (%s,%s,%s)"
        val = (firstName,lastName,email)
        try: 
        		self.cursor.execute(sql,val)
        except:
            print("Tutor already registered in the system.\n")
            return
        lastId = self.cursor.lastrowid
        sql = "SELECT * FROM `Department`"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print("— — — — —DEPARTMENT — — — — — —\n")
        for row in result:
            print(row[0])
        department = input("Enter the department of this tutor: ")
        sql = "UPDATE `Tutor` SET `Department` = %s WHERE  tutor_id = %s"
        val = (department, lastId, )
        try: 
        		self.cursor.execute(sql,val)
        except:
            print("Department entered is invalid.\n")
            return

        sql = "SELECT * FROM `Course`"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print("— — — — —OFFERED COURSES — — — — — —\n")
        for row in result:
            print("Course ID = ", row[0])
            print("Course Name = ", row[1])
        courseSelected = input("Enter courses that this tutor is qualified for, press e to finish selection: ")
        while(courseSelected != "e"):
        		try:
        			sql = "INSERT INTO `Qualification` (`Tutor_ID`,`Course_ID`) VALUES (%s,%s)"
        			val = (lastId, courseSelected)
        			self.cursor.execute(sql, val)
        			courseSelected = input("Enter courses that this tutor is qualified for, press e to finish selection: ")
        		except: 
        			print("The course entered is invalid")
        			return
        self.db.commit()
        print("— — — SUCCESS — — — \n")

    def deleteAppointment(self):
        appointmentId = input("Enter Appointment ID to cancel or enter 'c' to cancel : ")
        if appointmentId == 'c':
            return
        sql = "DELETE FROM `Appointment` WHERE `Appointment_ID` = %s"
        val = (appointmentId,)
        error = self.cursor.execute(sql, val)
        if error is not None:
            print("Invalid Appointment ID. Please try again.")
            return
        self.db.commit()
        print("Appointment with ID = {} was successfully deleted from records.\n".format(appointmentId))

    def viewUpcomingAppointments(self):
        today = date.today().strftime("%Y-%m-%d")
        sql = "Select * from `Admin_VW` where `Date` >= (%s)"
        self.cursor.execute(sql, (today,))

        result = self.cursor.fetchall()
        print("— — — — — Upcoming Appointments— — — — — —\n")
        for row in result:
            print("Appointment Id = ", row[0])
            print("Course = ", row[1], row[2])
            print("Student = ", row[3], row[4])
            print("Tutor = ", row[6], row[7])
            print("Time = ", row[9], row[10])
            print("\n")
        print("— — — — — — — — — — — — — — — — — — —\n")

    def viewTodayAppointments(self):
        sql = "Select * from `today_appointment`"
        self.cursor.execute(sql)

        result = self.cursor.fetchall()
        print("— — — — — Appointments for Today — — — — — —\n")
        for row in result:
            print("Appointment Id = ", row[0])
            print("Course = ", row[1], row[2])
            print("Student = ", row[3], row[4])
            print("Tutor = ", row[6], row[7])
            print("Time = ", row[10])
            print("\n")
        print("— — — — — — — — — — — — — — — — — — —\n")
    
    def viewAppointmentsByDate(self):
        try:
            date = input("Enter date(YYYY-MM-DD) : ")
            sql="Select * from `Admin_VW` Where `Date` = (%s)"
            val = (date,)
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()
            if result is None:
                print("No appointments on that date.\n")
                return
            print("— — — — Appointments on {} — — — — — — —\n".format(date))
            for row in result:
                print("Appointment Id = ", row[0])
                print("Course = ", row[1], row[2])
                print("Student = ", row[3], row[4])
                print("Tutor = ", row[6], row[7])
                print("Time = ", row[9], row[10])
                print("\n")
                print("— — — — — — — — — — — — — — — — — —\n")
        except:
            print("Invalid date input. Please try again.\n")
        
    def viewPastAppointments(self):
        print("— — — — — Past Appointments — — — — — —\n")
        today = date.today().strftime("%Y-%m-%d")
        sql = "Select * from `Admin_VW` where `Date` <= (%s)"
        self.cursor.execute(sql, (today,))

        result = self.cursor.fetchall()
        if result is None:
            print("No appointments found.\n")
            return
        print("— — — — — — — — — — — — — — — — — — —\n")
        for row in result:
            print("Appointment Id = ", row[0])
            print("Course = ", row[1], row[2])
            print("Student = ", row[3], row[4])
            print("Tutor = ", row[6], row[7])
            print("Time = ", row[9], row[10])
            print("\n")
        print("— — — — — — — — — — — — — — — — — —\n")

    def bookAppointment(self):
        try:
            sql = "SELECT * FROM `Course`"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            print("— — — — —OFFERED COURSES — — — — — —\n")
            for row in result:
                print("Course ID = ", row[0])
                print("Course Name = ", row[1])
            course = input("Enter course ID : ")
            sql = "SELECT * FROM `course` WHERE `course_id` = (%s)"
            self.cursor.execute(sql, (course,))
            result = self.cursor.fetchone()
            if result is None:
                print("Invalid Course ID. Please try again.")
                return
            date = input("Enter date (YYYY-MM-DD) : ")
            validDate = checkDate(date)
            if(validDate == False):
            	print("Date entered has past")
            	return
            sql = "SELECT * FROM `Tutor_Full_Info` WHERE `Course_ID` = (%s)"
            self.cursor.execute(sql, (course,))
            result = self.cursor.fetchall()
            for row in result:
                sql="SELECT * FROM `Timeslot` WHERE NOT EXISTS (SELECT * FROM `Appointment` WHERE `Tutor_ID` = (%s) AND `Date` = (%s) AND `Appointment`.`Time` = `Timeslot`.`Timeslot`)"
                self.cursor.execute(sql, (row[0], date))
                timeslots = self.cursor.fetchall()
                if timeslots is None:
                    continue
                print("Tutor ID = ", row[0])
                print("Tutor Name = ", row[1], row[2])
                print("Available time slots: ")
                for timeslot in timeslots:
                    print(timeslot[0])
                print()
            tutor_id = int(input("Enter tutor ID : "))
            exists = False
            for row in result:
            	 print(row[0])
            	 if row[0] == tutor_id:
                    exists = True
                    break
            if not exists:
                print("Invalid Tutor ID. Please try again.")
                return
            sql = "SELECT * FROM `Tutor_Full_Info` WHERE `Course_ID` = (%s) AND `tutor_id` = (%s)"
            self.cursor.execute(sql, (course, tutor_id))
            result = self.cursor.fetchone()
            if result is None:
                print("Tutor is not qualified for requested course. Please try again.")
                return
            chosen_timeslot = input("Enter timeslot (HH:MM:SS) : ")
            student_email = input("Enter student email : ")
            sql = "SELECT * FROM `student` WHERE `student_email` = (%s)"
            self.cursor.execute(sql, (student_email,))
            result = self.cursor.fetchone()
            if result is None:
                print("Student needs to be registered first. \n")
                return

            sql = "SELECT * FROM `appointment` WHERE `tutor_id` = (%s) AND `date` = (%s) AND `time` = (%s)"
            self.cursor.execute(sql, (tutor_id, date, chosen_timeslot))
            results = self.cursor.fetchone()
            if results is not None:
                print("Chosen time is unavailable. Please try again.\n")
                return

            sql = "INSERT INTO `Appointment` (`Student_Email`,`Tutor_ID`, `Location`, `Course_ID`, `Date`, `Time`) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (student_email, tutor_id, "Online", course, date, chosen_timeslot)
            error = self.cursor.execute(sql, val)
            self.db.commit()
            if error is not None:
                print("One or more input is invalid. Please try again.\n")
            print("— — — SUCCESS — — — \n")
        except:
            print("One or more input is invalid. Please try again.\n")

    def viewStudentAppointments(self):
        try:
            student_email = input("Enter student email : ")
            sql = "SELECT * FROM `admin_vw` WHERE `student_email` = (%s)"
            self.cursor.execute(sql, (student_email,))

            result = self.cursor.fetchall()
            print("— — — — Appointments — — — — — — —\n")
            for row in result:
                print("Appointment Id = ", row[0])
                print("Course = ", row[1], row[2])
                print("Tutor = ", row[6], row[7])
                print("Time = ", row[9], row[10])
                print()
            print("— — — — — — — — — — — — — — — — — —")
        except:
            print("Student with such email not found.\n")

    def viewCoursesAndTutors(self):
        print("— — — Offered Courses by Tutors — — — \n")
        sql = "SELECT * FROM `Tutor`"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for row in results:
            print("Tutor Name: ", row[1], row[2])
            sql = "SELECT * FROM `Tutor_Full_Info` where `Tutor_ID` = (%s)"
            self.cursor.execute(sql, (row[0],))
            qualifications = self.cursor.fetchall()
            if qualifications is not None:
                print("Offered courses: ")
                for qualification in qualifications:
                    print(qualification[3], qualification[4])
                print()
        print("— — — — — — — — — — — — — — — — — —\n")

    def viewStudents(self):
        print("— — — Registered Students — — — \n")
        sql = "SELECT * FROM `student`"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for row in results:
            print("Name: ", row[0], row[1])
            print("Email: ", row[2])
            print()
        print("— — — — — — — — — — — — — — — — — —\n")
