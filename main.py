from Database import Database
import os

host = os.getenv("MYSQL_HOST", "localhost")
user = os.getenv("MYSQL_USER", "root")
password = os.getenv("MYSQL_PASSWORD", "your-password")
database = os.getenv("MYSQL_DB", "tutoringapp")

db = Database(host, user, password, database)

def displayMainMenu():
	print("— — — — MENU — — — ")
	print("1. Register Student")
	print("2. Register Tutor")
	print("3. Book Appointment")
	print("4. Cancel Appointment")
	print("5. Records")
	print("6. Exit")
	print("— — — — — — — — — —")

def recordsMenu():
	print("— — — Records — — — ")
	print("1. Upcoming Appointments")
	print("2. Past Appointments")
	print("3. Appointments by Date")
	print("4. Offered Courses by Tutors")
	print("5. Registered Students")
	print("6. Go Back")
	print("— — — — — — — — — —")
	n = int(input("Enter option: "))
	if n == 1:
		db.viewAppointment()
		run()
	elif n == 2:
		db.viewPastAppointments()
		run()
	elif n == 3:
		db.viewAppointmentsByDate()
		run()
	elif n == 4:
		db.viewCoursesAndTutors()
		run()
	elif n ==5:
		db.viewStudents()
	elif n == 6:
		run()
	else:
		recordsMenu()

def delete():
	print("— — — Appointment Cancellation — — —")
	db.viewStudentAppointments()
	db.deleteAppointment()

def run():
	while(True):
		displayMainMenu()
		n = int(input("Enter option: "))
		if n == 1:
			db.registerStudent()
		elif n == 2:
			db.registerTutor()
		elif n == 3:
			db.bookAppointment()
		elif n == 4:
			delete()
		elif n == 5:
			recordsMenu()
		elif n == 6:
			print("- - - Thank You - - -")
			exit()
		else:
			run()

if __name__ == "__main__":
	run()
