import mysql.connector
import time

db = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="your-password",
	database="tutoringapp"
)

def initDB():
	 mycursor = db.cursor()


def displayMainMenu():
	 print("— — — — MENU — — — ")
	 print("1. Register Student")
	 print("2. Register Tutor")
	 print("3. Make Appointment")
	 print("4. Delete Appointment")
	 print("5. View All Appointment")
	 print("6. Exit")
	 print("— — — — — — — — — —")

def registerStudent():
	mycursor = db.cursor()
	print("— — — Student Registration — — — \n")
	firstName = input("Enter student firstName : ")
	lastName = input("Enter student lastName : ")
	email = input("Enter student email : ")
	sql = "INSERT INTO `student` (`Student_First_Name`,`Student_Last_Name`,`Student_Email`) VALUES (%s,%s,%s)"
	val = (firstName,lastName,email)
	mycursor.execute(sql,val)
	db.commit()
	print("— — — SUCCESS — — — \n")
	exit()

def registerStudent():
	mycursor = db.cursor()
	print("— — — Student Registration — — — \n")
	firstName = input("Enter student first name : ")
	lastName = input("Enter student last name : ")
	email = input("Enter student email : ")
	sql = "INSERT INTO `student` (`Student_First_Name`,`Student_Last_Name`,`Student_Email`) VALUES (%s,%s,%s)"
	val = (firstName,lastName,email)
	mycursor.execute(sql,val)
	db.commit()
	print("— — — SUCCESS — — — \n")
	exit()

def registerTutor():
	mycursor = db.cursor()
	print("— — — Tutor Registration — — — \n")
	firstName = input("Enter tutor first name : ")
	lastName = input("Enter tutor last name : ")
	email = input("Enter tutor email : ")
	sql = "INSERT INTO `tutor` (`Tutor_First_Name`,`Tutor_Last_Name`,`Tutor_Email`) VALUES (%s,%s,%s)"
	val = (firstName,lastName,email)
	mycursor.execute(sql,val)
	db.commit()
	print("— — — SUCCESS — — — \n")
	exit()

def addAppointment():
	mycursor = db.cursor()
	print("— — — Appointment Registration— — — \n")
	studentEmail = input("Enter student email : ")
	tutorEmail = input("Enter tutor email : ")
	courseCode = input("Enter course code : ")
	location = input("Enter location : ")
	date = input("Enter date(YYYY-MM-DD) : ")
	time = input("Enter time(HH:MM:SS) : ")

	sql = "Select `tutor_id` from `tutor` Where `tutor_email` = %s"
	val = (tutorEmail,)
	mycursor.execute(sql,val)

	resultTutor = mycursor.fetchone()
	tutorId = resultTutor[0]

	sql = "Select `student_id` from `student` Where `student_email` = %s"
	val = (studentEmail,)
	mycursor.execute(sql, val)

	resultStudent = mycursor.fetchone()
	studentId = resultStudent[0]

	sql = "Select `course_id` from `course` Where `course_name` = %s"
	val = (courseCode,)
	mycursor.execute(sql, val)

	resultCourse = mycursor.fetchone()
	courseId = resultCourse[0]



	sql = "INSERT INTO `appointment` (`Student_ID`,`Tutor_ID`, `Location`, `Course_ID`, `Date`, `Time`) VALUES (%s,%s,%s,%s,%s,%s)"
	val = (studentId,tutorId, location, courseId, date, time)
	mycursor.execute(sql, val)
	db.commit()
	print("— — — SUCCESS — — — \n")
	exit()

def deleteMenu():
	print("— — — Appointment Cancellation— — — \n")
	print("— — — — MENU — — — ")
	print("1. View All Appointments")
	print("2. Delete Appointment")
	n = int(input("Enter option : "))
	if n == 1:
		viewAppointment()
		deleteAppointment()
	elif n == 2:
		deleteAppointment()
	else:
		exit()
	exit()

def deleteAppointment():
	mycursor = db.cursor()
	appointmentId = input("Enter The Appointment Id To Be Delete : ")
	sql = "DELETE FROM `appointment` WHERE appointment_id = %s"
	val = (appointmentId,)
	mycursor.execute(sql, val)
	db.commit()
	exit()

def viewAppointment():
	mycursor = db.cursor()
	sql = "Select * from `Admin_VW`"
	mycursor.execute(sql)

	result = mycursor.fetchall()
	print("— — — — — — — — — — — — — — — — — — —")
	for row in result:
		print("Appointment Id = ", row[0])
		print("Course = ", row[1])
		print("Student = ", row[2], row[3])
		print("Tutor = ", row[4], row[5])
		print("Time = ", row[6], row[7])
		print("\n")
	print("— — — — — — — — — — — — — — — — — — —")

def run():
  	displayMainMenu()
  	n = int(input("Enter option : "))
  	if n == 1:
  		registerStudent()
  	elif n == 2:
  		registerTutor()
  	elif n == 3:
  		addAppointment()
  	elif n == 4:
  		deleteMenu()
  	elif n == 5:
  		viewAppointment()
  	elif n == 6:
  		print(" — — — Thank You — — -")
  	else:
  		run()


if __name__ == "__main__":
	initDB()
	run()