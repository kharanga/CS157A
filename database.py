import mysql.connector
from datetime import date
from tabulate import tabulate

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
        sql = "INSERT INTO `Student` (`Student_First_Name`,`Student_Last_Name`,`Student_Email`) VALUES (%s,%s,%s)"
        val = (firstName,lastName,email)
        error = self.cursor.execute(sql,val)
        if error is not None:
            print("Student already registered in the system.\n")
            return
        self.db.commit()
        print("— — — SUCCESS — — — \n")

    def registerTutor(self):
        print("— — — Tutor Registration — — — \n")
        firstName = input("Enter tutor first name : ")
        lastName = input("Enter tutor last name : ")
        email = input("Enter tutor email : ")
        sql = "INSERT INTO `Tutor` (`Tutor_First_Name`,`Tutor_Last_Name`,`Tutor_Email`) VALUES (%s,%s,%s)"
        val = (firstName,lastName,email)
        error = self.cursor.execute(sql,val)
        if error is not None:
            print("Tutor already registered in the system.\n")
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
            print("Invalid Appointment ID. Please try again.\n")
            return
        self.db.commit()
        print("Appointment with ID = {} was successfully deleted from records.\n".format(appointmentId))

    def viewUpcomingAppointments(self):
        today = date.today().strftime("%Y-%m-%d")
        sql = "Select * from `Admin_VW` where `Date` >= (%s)"
        self.cursor.execute(sql, (today,))
        results = self.cursor.fetchall()
        if results is None:
            print("No upcoming appointments.\n")
            return
        print("— — — — — Upcoming Appointments— — — — — —\n")
        columns = [i[0] for i in self.cursor.description]
        print(tabulate(results, headers=columns))
        print("— — — — — — — — — — — — — — — — — — —\n")

    def viewTodayAppointments(self):
        sql = """Select appointment_id, course_id, course_name, student_first_name, student_last_name, 
                 tutor_first_name, tutor_last_name, time from `today_appointment`"""
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if results is None:
            print("No appointments today.\n")
            return
        print("— — — — — Appointments for Today — — — — — —\n")
        columns = [i[0] for i in self.cursor.description]
        print(tabulate(results, headers=columns))
        print("— — — — — — — — — — — — — — — — — — —\n")
    
    def viewAppointmentsByDate(self):
        try:
            date = input("Enter date(YYYY-MM-DD) : ")
            sql="Select * from `Admin_VW` Where `Date` = (%s)"
            val = (date,)
            self.cursor.execute(sql, val)
            results = self.cursor.fetchall()
            if results is None:
                print("No appointments on that date.\n")
                return
            print("— — — — Appointments on {} — — — — — — —\n".format(date))
            columns = [i[0] for i in self.cursor.description]
            print(tabulate(results, headers=columns))
            print("— — — — — — — — — — — — — — — — — —\n")
        except:
            print("Invalid date input. Please try again.\n")
        
    def viewPastAppointments(self):
        print("— — — — — Past Appointments — — — — — —\n")
        today = date.today().strftime("%Y-%m-%d")
        sql = "Select * from `Admin_VW` where `Date` <= (%s)"
        self.cursor.execute(sql, (today,))

        results = self.cursor.fetchall()
        if results is None:
            print("No appointments found.\n")
            return
        columns = [i[0] for i in self.cursor.description]
        print(tabulate(results, headers=columns))
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
            sql = "SELECT * FROM `Tutor_Full_Info` WHERE `Course_ID` = (%s)"
            self.cursor.execute(sql, (course,))
            result = self.cursor.fetchall()
            for row in result:
                sql="""SELECT * FROM `Timeslot` WHERE NOT EXISTS (SELECT * FROM `Appointment` WHERE 
                       `Tutor_ID` = (%s) AND `Date` = (%s) AND `Appointment`.`Time` = `Timeslot`.`Timeslot`)"""
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
            tutor_id = input("Enter tutor ID : ")
            exists = False
            for row in result:
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
            sql = """SELECT appointment_id, course_id, course_name, tutor_first_name,
                     tutor_last_name, date, time FROM `admin_vw` WHERE `student_email` = (%s)"""
            self.cursor.execute(sql, (student_email,))
            results = self.cursor.fetchall()
            if results is None:
                print("Student has no appointments yet.\n")
                return
            print("— — — — Appointments — — — — — — —\n")
            columns = [i[0] for i in self.cursor.description]
            print(tabulate(results, headers=columns))
            print("— — — — — — — — — — — — — — — — — —")
        except:
            raise Exception

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
        sql = "SELECT * FROM `student`"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if results is None:
            print("No registered students found.\n")
            return
        print("— — — Registered Students — — — \n")
        columns = [i[0] for i in self.cursor.description]
        print(tabulate(results, headers=columns))
        print("— — — — — — — — — — — — — — — — — —\n")

    def executeInput(self):
        try:
            print("— — — Direct Database Manipulation — — — \n")
            print("This option is recommended for ADVANCED users only")
            print("who have previous experience with RDBMS and SQL.")
            print("This option allows you to interact with the")
            print("database directly using SQL commands.\n")
            sql = input("Enter SQL command: ")
            self.cursor.execute(sql)
            columns = [i[0] for i in self.cursor.description]
            results = self.cursor.fetchall()
            print()
            print(tabulate(results, headers=columns))
            print("— — — — — — — — — — — — — — — — — —\n")
        except:
            print("Invalid SQL command or values. Please try again.\n")