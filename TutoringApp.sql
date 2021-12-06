CREATE DATABASE TutoringApp;
 USE TutoringApp;
 
 
 CREATE TABLE Department (
	Department_ID INT NOT NULL UNIQUE,
    Department_Name VARCHAR(60) UNIQUE,

    PRIMARY KEY(Department_ID)
 );
 
 CREATE TABLE Course (
	Course_ID INT NOT NULL UNIQUE,
    Course_Name VARCHAR(60) UNIQUE,
    Department_ID INT,
    
    PRIMARY KEY(Course_ID),
    FOREIGN KEY(Department_ID) REFERENCES Department(Department_ID)
 );
 
 CREATE TABLE Student (
	Student_ID INT NOT NULL AUTO_INCREMENT UNIQUE,
    Student_First_Name VARCHAR(60),
    Student_Last_Name VARCHAR(60),
    Student_Email VARCHAR(60),
    
    PRIMARY KEY(Student_ID)
 );
 
  CREATE TABLE Tutor (
	Tutor_ID INT NOT NULL AUTO_INCREMENT UNIQUE,
    Tutor_First_Name VARCHAR(60),
    Tutor_Last_Name VARCHAR(60),
    Tutor_Email VARCHAR(60),
    
    PRIMARY KEY(Tutor_ID)
 );
 
 CREATE TABLE Appointment (
	Appointment_ID INT NOT NULL AUTO_INCREMENT UNIQUE,
    Date DATE,
	Time TIME,
    Location VARCHAR(100),
    Course_ID INT,
    Tutor_ID INT,
    Student_ID INT,
    
    PRIMARY KEY(Appointment_ID),
    FOREIGN KEY(Course_ID) REFERENCES Course(Course_ID),
    FOREIGN KEY(Tutor_ID) REFERENCES Tutor(Tutor_ID),
    FOREIGN KEY(Student_ID) REFERENCES Student(Student_ID) 
 );
 
CREATE VIEW Admin_VW AS
SELECT a.Appointment_ID, c.Course_Name, s.Student_First_Name, s.Student_Last_Name, t.Tutor_First_Name, t.Tutor_Last_Name, a.Date, a.Time
From Course c, Student s, Appointment a, Tutor t
WHERE s.Student_ID = a.Student_ID AND a.Course_ID = c.Course_ID AND a.Tutor_ID = t.Tutor_ID;
 
INSERT INTO Department (Department_ID, Department_Name)
VALUES  ('100', 'Math'),
		('200', 'Science'),
        ('300', 'Engineer');
        
INSERT INTO Course (Course_ID, Course_Name, Department_ID)
VALUES ('101', 'Math42', '100'),
		('102', 'Math39', '100'),
		('201', 'Biol1A', '200'),
		('202', 'Phys50', '200'),
		('301', 'Eng101', '300'),
		('302', 'Eng100W', '300');

INSERT INTO Student(Student_First_Name, Student_Last_Name, Student_Email)
VALUES ('Khang', 'Nguyen', 'khang.d.nguyen@sjsu.edu'),
		('John', 'Doe', 'test@gmail'),
        ('Karen', 'Smith', 'karen.smith@sjsu.edu'),
        ('Pocahontas', 'Nguyen', 'pocahontas.nguyen@sjsu.edu'),
        ('Tyler', 'Tang', 'tyler.tang@sjsu.edu');

INSERT INTO Tutor(Tutor_First_Name, Tutor_Last_Name, Tutor_Email)
VALUES ('Edgar', 'Truong', 'edgar.truong@sjsu.edu'),
		('Devin', 'Truong', 'devin.truong@gmail'),
        ('Mary', 'Truong', 'mary.truong@sjsu.edu'),
        ('Katherine', 'Truong', 'katherine.truong@sjsu.edu'),
        ('Paul', 'Truong', 'paul.truong@sjsu.edu');
        
INSERT INTO Appointment(Location, Date, Time, Course_ID, Tutor_ID, Student_ID)
VALUES ('MH380', '2021-12-10', '11:00:00', '101', '1', '2'),
	('DH120', '2021-12-11', '13:00:00', '201', '2', '1'),
	('MW230', '2021-12-30', '15:00:00', '301', '1', '3'),
	('FN230', '2021-12-21', '09:00:00', '102', '3', '5'),
	('BS110', '2021-12-19', '10:00:00', '102', '3', '2');
    



