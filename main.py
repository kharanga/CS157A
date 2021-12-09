from Database import Database
import os

host = os.getenv("MYSQL_HOST", "localhost")
user = os.getenv("MYSQL_USER", "root")
password = os.getenv("MYSQL_PASSWORD", "secret")
database = os.getenv("MYSQL_DB", "tutoringapp")

db = Database(host, user, password, database)

def displayMainMenu():
	print("— — — — MENU — — — ")
	print("1. Register Student")
	print("2. Register Tutor")
	print("3. Book Appointment")
	print("4. Cancel Appointment")
	print("5. Records")
	print("6. Direct database manipulation (advanced)")
	print("7. Exit")
	print("— — — — — — — — — —")

def recordsMenu():
	print("— — — Records — — — ")
	print("1. Appointments for today")
	print("2. Upcoming Appointments")
	print("3. Past Appointments")
	print("4. Appointments by Date")
	print("5. Offered Courses by Tutors")
	print("6. Registered Students")
	print("7. Go Back")
	print("— — — — — — — — — —")
	n = int(input("Enter option: "))
	if n == 1:
		db.viewTodayAppointments()
	elif n == 2:
		db.viewUpcomingAppointments()
	elif n == 3:
		db.viewPastAppointments()
	elif n == 4:
		db.viewAppointmentsByDate()
	elif n == 5:
		db.viewCoursesAndTutors()
	elif n == 6:
		db.viewStudents()
	elif n == 7:
		return
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
			db.executeInput()
		elif n == 7:
			print("- - - Thank You - - -")
			exit()
		else:
			run()

if __name__ == "__main__":
	run()
