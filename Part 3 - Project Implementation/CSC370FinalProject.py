#daniel dubichev - v00877776 - CSC370 A3
#note to markers this only works in python 2 versions. see that for taking command line input i use raw_input (p2) instead of the p3 variant (input)


'''
if keystroke is d drop tables and build them again and do basic populations -- INNEFICIENT
if keystoke is t truncate tables and do basic populations -- EFFICIENT
if keystroke is c continue with the script -- QUICK
if keystoke is anything else keep asking for input

'''


#imports
import psycopg2
import sys,os
import datetime

#psql
psql_usr = 'danieldubichev'
psql_db = 'danieldubichev'
psql_password = 'danny123'
psql_server = 'studentdb1.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,
    user= psql_usr,
    password=psql_password,
    host=psql_server,
    port= psql_port)

#client side cursors and server side cursors
cursor = conn.cursor()

print("CSC370 Assignment 3")
print("Testing if user table exists. If user table exists, then all other tables exist by my database design")
print("If user table doesn't exist, then tables will be created and populated")
print("if user table does exist, you will have the chance to either truncate the table and repopulate, drop all tables and repopulate, or continue with the script")
print("Now querying whether any tables exist at all")
cursor.execute("SELECT * FROM users;")
firsttime = cursor.fetchone()
if firsttime == None:
    print("No rows detected in main user table, now creating database")
    print("")
    cursor.execute("CREATE TABLE users(userID SERIAL, userName varchar(21) NOT NULL, userEmail varchar(75) NOT NULL, userPassword varchar(21) NOT NULL, userRegisterDate Date NOT NULL,userType varchar(7) NOT NULL, PRIMARY KEY (userID));")
    print("The query was " + cursor.query)


    #learner
    print("")
    cursor.execute("CREATE TABLE learner (learnerID int, learnerFavoriteTopic varchar(20), learnerBio varchar(80), learnerSkillLevel varchar(15), learnerLastLog Date, FOREIGN KEY (learnerID) references users(userID));")
    print("The query was " + cursor.query)

    #staff
    print("")
    cursor.execute("CREATE TABLE staff (staffID int, staffPhone varchar(15), staffEmail varchar(75) NOT NULL, FOREIGN KEY (staffID) references users(userID));")
    print("The query was " + cursor.query)

    #material
    print("")
    cursor.execute("CREATE TABLE material (materialID SERIAL, materialSource varchar(30) NOT NULL, materialLink varchar(100) NOT NULL, materialType varchar(20) NOT NULL, materialSubject varchar(30) NOT NULL, materialGrade varchar(15) NOT NULL, materialDifficulty smallint NOT NULL, materialDateProduced date NOT NULL, PRIMARY KEY (materialID));")
    print("The query was " + cursor.query)

    #textbook
    print("")
    cursor.execute("CREATE TABLE textbook (relmaterialID int, textbookLink varchar(100) NOT NULL, textbookName varchar(75) NOT NULL, FOREIGN KEY (relmaterialID) REFERENCES material(materialID));")
    print("The query was " + cursor.query)

    #sequence
    print("")
    cursor.execute("CREATE TABLE sequence (sequenceID SERIAL, sequenceDescription varchar(100), sequenceSize smallint NOT NULL, sequenceName varchar(40) NOT NULL, sequenceDifficulty smallint NOT NULL, PRIMARY KEY(sequenceID));")
    print("The query was " + cursor.query)

    #entry
    print("")
    cursor.execute("CREATE TABLE entry (entryID SERIAL, relsequenceID int NOT NULL, relmaterialID int NOT NULL, entryRelevance varchar(50), entryPosition smallint NOT NULL, PRIMARY KEY (entryID), FOREIGN KEY (relmaterialID) references material(materialID), FOREIGN KEY (relsequenceID) references sequence(sequenceID));")
    print("The query was " + cursor.query)

    #REPOPULATION TIME
    print("repopulating with starter data")


    cursor.execute("INSERT INTO users (userName, userEmail, userPassword, userRegisterDate, userType) VALUES ('danieldubichev', 'dannydubichev@gmail.com', 'test1', '2019-04-20', 'learner' ),('joemama', 'joemam@yahoo.ca', 'test2', '2019-07-06', 'learner'),('eidanchilla', 'eidanchilla@msn.com', 'test3', '2019-03-20', 'learner'),('jonassmith', 'jonassmith@aol.ca', 'test4', '2019-02-11', 'staff'),('alannabanana', 'banananna@bananas.com', 'test5', '2019-01-01', 'staff');")

    #matching foreign keys to learner & staff tables
    #staff
    cursor.execute("INSERT INTO staff(staffid, staffphone, staffemail) SELECT userid, null, useremail FROM users u WHERE NOT EXISTS (SELECT 1 FROM staff s WHERE s.staffID = u.userID) AND  u.usertype = 'staff';")
    #learners
    cursor.execute("INSERT INTO learner(learnerid) SELECT userid FROM users u WHERE NOT EXISTS (SELECT 1 FROM learner l  WHERE l.learnerID = u.userID) AND  u.usertype = 'learner';")

    #now populate learner and staff tables
    #learner
    cursor.execute("UPDATE learner SET learnerFavoriteTopic = 'Chinese', learnerBio = 'I love to learn!', learnerskilllevel =  'Advanced', learnerlastlog = '2019-10-10' Where learner.learnerid = '1';")
    cursor.execute("UPDATE learner SET learnerFavoriteTopic = 'Math', learnerBio = 'Math is l1f3', learnerskilllevel =  'Advanced', learnerlastlog = '2019-11-10' Where learner.learnerid = '2';")
    cursor.execute("UPDATE learner SET learnerFavoriteTopic = 'Chemistry', learnerBio = 'The next walter white', learnerskilllevel =  'Professional', learnerlastlog = '2019-10-11' Where learner.learnerid = '3';")

    #staff
    cursor.execute("UPDATE Staff SET staffphone = '2505087873'WHERE Staffid = '4';")
    cursor.execute("UPDATE Staff SET staffphone = '6045087873'WHERE Staffid = '5';")

    #material
    cursor.execute("INSERT INTO material (materialsource, materiallink, materialtype, materialsubject, materialgrade, materialdifficulty, materialdateproduced) VALUES ( 'Uni Of Victoria', 'www.uvic.ca/math101/midterm01', 'practice midterm', 'introcalculus', 'first year uni','6', '2012-01-01'), ( 'Uni Of Victoria', 'www.uvic.ca/csc101/assignment01', 'assignment 1', 'intro to computers', 'first year uni', '1', '2018-06-30'), ( 'Uni Of Alabama', 'www.rolltide.edu/math400/quiz-9', '9th quiz in course', 'differential equations', '4th year uni', '8', '2019-01-11');")

    #textbook
    cursor.execute("INSERT INTO textbook (relmaterialid, textbooklink, textbookname) VALUES ('1', 'www.pearson.com/129304u3280', 'Pearson Calculus Intro'), ('3', 'www.ama.edu/math-advanced', 'Advanced Mathematical Approaches'), ('3', 'www.ama.edu/diffeq-advanced', 'Advanced Differential Equations');")

    #sequence
    cursor.execute("INSERT INTO sequence (sequencedescription, sequencesize, sequencename, sequencedifficulty) VALUES (' A sequence with a very easy then hard math course', '2', 'Easy & Hard Maths', '8');")

    #entry
    cursor.execute("INSERT INTO entry(relsequenceid, relmaterialid, entryrelevance, entryposition) VALUES ('1', '1', 'the easy part - intro calc', '1'), ('1', '3', 'the hard part - advanced diff eq', '2');")

    #test all tables have been properly populated after data repopulation
    print("now displaying the populate tables")
    print("")
    cursor.execute("SELECT * FROM users;")
    print("The query used was: " + cursor.query)
    print("")
    rows = cursor.fetchall()
    for r in rows:
        print(r)
    cursor.execute("SELECT * FROM learner;")
    print("The query used was: " + cursor.query)
    print("")
    rows = cursor.fetchall()
    for r in rows:
        print(r)
    cursor.execute("SELECT * FROM staff;")
    print("The query used was: " + cursor.query)
    print("")
    rows = cursor.fetchall()
    for r in rows:
        print(r)
    cursor.execute("SELECT * FROM material;")
    print("The query used was: " + cursor.query)
    print("")
    rows = cursor.fetchall()
    for r in rows:
        print(r)
    cursor.execute("SELECT * FROM textbook;")
    print("The query used was: " + cursor.query)
    print("")

    rows = cursor.fetchall()
    for r in rows:
        print(r)
    cursor.execute("SELECT * FROM sequence;")
    print("The query used was: " + cursor.query)
    print("")

    rows = cursor.fetchall()
    for r in rows:
        print(r)
    cursor.execute("SELECT * FROM entry;")
    print("The query used was: " + cursor.query)
    print("")

    rows = cursor.fetchall()
    for r in rows:
        print(r)



if firsttime != None:

    print("There is data that currently exists in the db,")
    print("Press 't' then enter on your keyboard to truncate each table then repopulize each table with data")
    print("Press 'd' then enter on your keyboard to drop and recreate each table, the repopulate each table with data")
    print("Press any other key then enter on your keyboard to continue with using the current data in assignment 3 tables and script")

    selectedoption = raw_input("Press desired key then 'enter': ")

    if selectedoption == 't':
        print("Truncating tables")
        #table truncation
        #restart identity is to restart auto-increment at one
        print("")
        cursor.execute("TRUNCATE TABLE users, learner, staff, material, textbook, sequence, entry RESTART IDENTITY;")
        print("The query used was: " + cursor.query)
        print("")
        #repopulate tables
        print("Repopulating tables")

        #repopulating user table
        cursor.execute("INSERT INTO users (userName, userEmail, userPassword, userRegisterDate, userType) VALUES ('danieldubichev', 'dannydubichev@gmail.com', 'test1', '2019-04-20', 'learner' ),('joemama', 'joemam@yahoo.ca', 'test2', '2019-07-06', 'learner'),('eidanchilla', 'eidanchilla@msn.com', 'test3', '2019-03-20', 'learner'),('jonassmith', 'jonassmith@aol.ca', 'test4', '2019-02-11', 'staff'),('alannabanana', 'banananna@bananas.com', 'test5', '2019-01-01', 'staff');")

        #matching foreign keys to learner & staff tables
        #staff
        cursor.execute("INSERT INTO staff(staffid, staffphone, staffemail) SELECT userid, null, useremail FROM users u WHERE NOT EXISTS (SELECT 1 FROM staff s WHERE s.staffID = u.userID) AND  u.usertype = 'staff';")
        #learners
        cursor.execute("INSERT INTO learner(learnerid) SELECT userid FROM users u WHERE NOT EXISTS (SELECT 1 FROM learner l  WHERE l.learnerID = u.userID) AND  u.usertype = 'learner';")

        #now populate learner and staff tables
        #learner
        cursor.execute("UPDATE learner SET learnerFavoriteTopic = 'Chinese', learnerBio = 'I love to learn!', learnerskilllevel =  'Advanced', learnerlastlog = '2019-10-10' Where learner.learnerid = '1';")
        cursor.execute("UPDATE learner SET learnerFavoriteTopic = 'Math', learnerBio = 'Math is l1f3', learnerskilllevel =  'Advanced', learnerlastlog = '2019-11-10' Where learner.learnerid = '2';")
        cursor.execute("UPDATE learner SET learnerFavoriteTopic = 'Chemistry', learnerBio = 'The next walter white', learnerskilllevel =  'Professional', learnerlastlog = '2019-10-11' Where learner.learnerid = '3';")

        #staff
        cursor.execute("UPDATE Staff SET staffphone = '2505087873'WHERE Staffid = '4';")
        cursor.execute("UPDATE Staff SET staffphone = '6045087873'WHERE Staffid = '5';")

        #material
        cursor.execute("INSERT INTO material (materialsource, materiallink, materialtype, materialsubject, materialgrade, materialdifficulty, materialdateproduced) VALUES ( 'Uni Of Victoria', 'www.uvic.ca/math101/midterm01', 'practice midterm', 'introcalculus', 'first year uni','6', '2012-01-01'), ( 'Uni Of Victoria', 'www.uvic.ca/csc101/assignment01', 'assignment 1', 'intro to computers', 'first year uni', '1', '2018-06-30'), ( 'Uni Of Alabama', 'www.rolltide.edu/math400/quiz-9', '9th quiz in course', 'differential equations', '4th year uni', '8', '2019-01-11');")

        #textbook
        cursor.execute("INSERT INTO textbook (relmaterialid, textbooklink, textbookname) VALUES ('1', 'www.pearson.com/129304u3280', 'Pearson Calculus Intro'), ('3', 'www.ama.edu/math-advanced', 'Advanced Mathematical Approaches'), ('3', 'www.ama.edu/diffeq-advanced', 'Advanced Differential Equations');")

        #sequence
        cursor.execute("INSERT INTO sequence (sequencedescription, sequencesize, sequencename, sequencedifficulty) VALUES (' A sequence with a very easy then hard math course', '2', 'Easy & Hard Maths', '8');")

        #entry
        cursor.execute("INSERT INTO entry(relsequenceid, relmaterialid, entryrelevance, entryposition) VALUES ('1', '1', 'the easy part - intro calc', '1'), ('1', '3', 'the hard part - advanced diff eq', '2');")

        #test all tables have been properly populated after data repopulation
        print("now displaying the populate tables")
        print("")
        cursor.execute("SELECT * FROM users;")
        print("The query used was: " + cursor.query)
        print("")
        rows = cursor.fetchall()
        for r in rows:
            print(r)
        cursor.execute("SELECT * FROM learner;")
        print("The query used was: " + cursor.query)
        print("")
        rows = cursor.fetchall()
        for r in rows:
            print(r)
        cursor.execute("SELECT * FROM staff;")
        print("The query used was: " + cursor.query)
        print("")
        rows = cursor.fetchall()
        for r in rows:
           print(r)
        cursor.execute("SELECT * FROM material;")
        print("The query used was: " + cursor.query)
        print("")
        rows = cursor.fetchall()
        for r in rows:
            print(r)
        cursor.execute("SELECT * FROM textbook;")
        print("The query used was: " + cursor.query)
        print("")

        rows = cursor.fetchall()
        for r in rows:
            print(r)
        cursor.execute("SELECT * FROM sequence;")
        print("The query used was: " + cursor.query)
        print("")

        rows = cursor.fetchall()
        for r in rows:
            print(r)
        cursor.execute("SELECT * FROM entry;")
        print("The query used was: " + cursor.query)
        print("")

        rows = cursor.fetchall()
        for r in rows:
            print(r)


    #drop tables
    if selectedoption == 'd':
        print("dropping tables")
        cursor.execute("DROP TABLE users, learner, staff, material, textbook, sequence, entry;")

        #table recreation after tables are dropped
        #users
        print("")
        cursor.execute("CREATE TABLE users(userID SERIAL, userName varchar(21) NOT NULL, userEmail varchar(75) NOT NULL, userPassword varchar(21) NOT NULL, userRegisterDate Date NOT NULL,userType varchar(7) NOT NULL, PRIMARY KEY (userID));")
        print("The query was " + cursor.query)


        #learner
        print("")
        cursor.execute("CREATE TABLE learner (learnerID int, learnerFavoriteTopic varchar(20), learnerBio varchar(80), learnerSkillLevel varchar(15), learnerLastLog Date , FOREIGN KEY (learnerID) references users(userID));")
        print("The query was " + cursor.query)

        #staff
        print("")
        cursor.execute("CREATE TABLE staff (staffID int, staffPhone varchar(15), staffEmail varchar(75) NOT NULL, FOREIGN KEY (staffID) references users(userID));")
        print("The query was " + cursor.query)

        #material
        print("")
        cursor.execute("CREATE TABLE material (materialID SERIAL, materialSource varchar(30) NOT NULL, materialLink varchar(100) NOT NULL, materialType varchar(20) NOT NULL, materialSubject varchar(30) NOT NULL, materialGrade varchar(15) NOT NULL, materialDifficulty smallint NOT NULL, materialDateProduced date NOT NULL, PRIMARY KEY (materialID));")
        print("The query was " + cursor.query)

        #textbook
        print("")
        cursor.execute("CREATE TABLE textbook (relmaterialID int, textbookLink varchar(100) NOT NULL, textbookName varchar(75) NOT NULL, FOREIGN KEY (relmaterialID) REFERENCES material(materialID));")
        print("The query was " + cursor.query)

        #sequence
        print("")
        cursor.execute("CREATE TABLE sequence (sequenceID SERIAL, sequenceDescription varchar(100), sequenceSize smallint NOT NULL, sequenceName varchar(40) NOT NULL, sequenceDifficulty smallint NOT NULL, PRIMARY KEY(sequenceID));")
        print("The query was " + cursor.query)

        #entry
        print("")
        cursor.execute("CREATE TABLE entry (entryID SERIAL, relsequenceID int NOT NULL, relmaterialID int NOT NULL, entryRelevance varchar(50), entryPosition smallint NOT NULL, PRIMARY KEY (entryID), FOREIGN KEY (relmaterialID) references material(materialID), FOREIGN KEY (relsequenceID) references sequence(sequenceID));")
        print("The query was " + cursor.query)

        #REPOPULATION TIME
        print("repopulating with starter data")


        cursor.execute("INSERT INTO users (userName, userEmail, userPassword, userRegisterDate, userType) VALUES ('danieldubichev', 'dannydubichev@gmail.com', 'test1', '2019-04-20', 'learner' ),('joemama', 'joemam@yahoo.ca', 'test2', '2019-07-06', 'learner'),('eidanchilla', 'eidanchilla@msn.com', 'test3', '2019-03-20', 'learner'),('jonassmith', 'jonassmith@aol.ca', 'test4', '2019-02-11', 'staff'),('alannabanana', 'banananna@bananas.com', 'test5', '2019-01-01', 'staff');")

        #matching foreign keys to learner & staff tables
        #staff
        cursor.execute("INSERT INTO staff(staffid, staffphone, staffemail) SELECT userid, null, useremail FROM users u WHERE NOT EXISTS (SELECT 1 FROM staff s WHERE s.staffID = u.userID) AND  u.usertype = 'staff';")
        #learners
        cursor.execute("INSERT INTO learner(learnerid) SELECT userid FROM users u WHERE NOT EXISTS (SELECT 1 FROM learner l  WHERE l.learnerID = u.userID) AND  u.usertype = 'learner';")

        #now populate learner and staff tables
        #learner
        cursor.execute("UPDATE learner SET learnerFavoriteTopic = 'Chinese', learnerBio = 'I love to learn!', learnerskilllevel =  'Advanced', learnerlastlog = '2019-10-10' Where learner.learnerid = '1';")
        cursor.execute("UPDATE learner SET learnerFavoriteTopic = 'Math', learnerBio = 'Math is l1f3', learnerskilllevel =  'Advanced', learnerlastlog = '2019-11-10' Where learner.learnerid = '2';")
        cursor.execute("UPDATE learner SET learnerFavoriteTopic = 'Chemistry', learnerBio = 'The next walter white', learnerskilllevel =  'Professional', learnerlastlog = '2019-10-11' Where learner.learnerid = '3';")

        #staff
        cursor.execute("UPDATE Staff SET staffphone = '2505087873'WHERE Staffid = '4';")
        cursor.execute("UPDATE Staff SET staffphone = '6045087873'WHERE Staffid = '5';")

        #material
        cursor.execute("INSERT INTO material (materialsource, materiallink, materialtype, materialsubject, materialgrade, materialdifficulty, materialdateproduced) VALUES ( 'Uni Of Victoria', 'www.uvic.ca/math101/midterm01', 'practice midterm', 'introcalculus', 'first year uni','6', '2012-01-01'), ( 'Uni Of Victoria', 'www.uvic.ca/csc101/assignment01', 'assignment 1', 'intro to computers', 'first year uni', '1', '2018-06-30'), ( 'Uni Of Alabama', 'www.rolltide.edu/math400/quiz-9', '9th quiz in course', 'differential equations', '4th year uni', '8', '2019-01-11');")

        #textbook
        cursor.execute("INSERT INTO textbook (relmaterialid, textbooklink, textbookname) VALUES ('1', 'www.pearson.com/129304u3280', 'Pearson Calculus Intro'), ('3', 'www.ama.edu/math-advanced', 'Advanced Mathematical Approaches'), ('3', 'www.ama.edu/diffeq-advanced', 'Advanced Differential Equations');")

        #sequence
        cursor.execute("INSERT INTO sequence (sequencedescription, sequencesize, sequencename, sequencedifficulty) VALUES (' A sequence with a very easy then hard math course', '2', 'Easy & Hard Maths', '8');")

        #entry
        cursor.execute("INSERT INTO entry(relsequenceid, relmaterialid, entryrelevance, entryposition) VALUES ('1', '1', 'the easy part - intro calc', '1'), ('1', '3', 'the hard part - advanced diff eq', '2');")

        #test all tables have been properly populated after data repopulation
        print("now displaying the populate tables")
        print("")
        cursor.execute("SELECT * FROM users;")
        print("The query used was: " + cursor.query)
        print("")
        rows = cursor.fetchall()
        for r in rows:
            print(r)
        cursor.execute("SELECT * FROM learner;")
        print("The query used was: " + cursor.query)
        print("")
        rows = cursor.fetchall()
        for r in rows:
            print(r)
        cursor.execute("SELECT * FROM staff;")
        print("The query used was: " + cursor.query)
        print("")
        rows = cursor.fetchall()
        for r in rows:
           print(r)
        cursor.execute("SELECT * FROM material;")
        print("The query used was: " + cursor.query)
        print("")
        rows = cursor.fetchall()
        for r in rows:
            print(r)
        cursor.execute("SELECT * FROM textbook;")
        print("The query used was: " + cursor.query)
        print("")

        rows = cursor.fetchall()
        for r in rows:
            print(r)
        cursor.execute("SELECT * FROM sequence;")
        print("The query used was: " + cursor.query)
        print("")

        rows = cursor.fetchall()
        for r in rows:
            print(r)
        cursor.execute("SELECT * FROM entry;")
        print("The query used was: " + cursor.query)
        print("")

        rows = cursor.fetchall()
        for r in rows:
            print(r)




    if selectedoption != 't' and selectedoption != 'd':
        print("")
        print("you have not selected to truncate or drop. you will now be ran through the assignment 3 script")
        print("")

    #repopulation of the tables with basic data.
print("")
print("")
print("DEMONSTRATING BASIC SELECT QUERIES")
#execute query - selecting all the users
print("the following are basic select queries")
print("selecting all the users and their id's, names and emails.")
cursor.execute("select userid, username, useremail from users;")

rows = cursor.fetchall()

for r in rows:
    print(r)
print("")
print("Query completed.")
print("Query was: select userid, username, useremail from users;")


#execute query, selecting all the learners
print("selecting all the learners")
cursor.execute("select learnerid, learnerfavoritetopic, learnerbio, learnerskilllevel, learnerlastlog from learner;")
rows = cursor.fetchall()

for r in rows:
    print(r)
print("")
print("Query completed.")
print("select learnerid, learnerfavoritetopic, learnerbio, learnerskilllevel, learnerlastlog from learner;")


#execute query, selecting all the staff
print("selecting all the staff")
cursor.execute("select staffid, staffphone, staffemail from staff;")
rows = cursor.fetchall()

for r in rows:
    print(r)
print("")
print("Query completed.")
print("Query was: select staffid, staffphone, staffemail from staff;")

#inserting a user then deciding whether it is a staff or user

print("inserting a user")
print("as soon as you answer whether you are a learner or staff, you will be updated to the main user database as well as the corresponding subclass table")
print("")
username = raw_input("Type in your username : ")
print("")
useremail = raw_input("What is your email : ")
print("")
userpassword = raw_input("What is your password : ")
print("")
now = datetime.datetime.now()
year = '{:02d}'.format(now.year)
month = '{:02d}'.format(now.month)
day = '{:02d}'.format(now.day)
daymonthyear = '{}-{}-{}'.format(year,month,day)
userregisterdate = daymonthyear
print("")
#if it is the case that the input is neither a learner or staff
#terminate the process because the only acceptable inputs are 'learner' or 'staff'
usertype = raw_input("Are you a learner or a staff? Please only type 'learner' or 'staff', the process will terminate otherwise: ")
print("")



while usertype != 'staff' or usertype != 'learner':
    usertype = raw_input("please type in whether the user is a 'staff' or 'learner': ")
    if usertype == 'staff' or usertype == 'learner':
        break

print("")
print("Your information is now being inserted into the database")


#if the username does not already exist in the DB, then insert cmd line data into db

cursor.execute("SELECT username FROM users WHERE username = '" + username + "';")
userrowattempt1 = cursor.fetchone()
if userrowattempt1 != None:
    print("The username you selected already exists in the Database. Please re run the program and try again")
    sys.exit()


cursor.execute("INSERT INTO users(username, useremail, userpassword, userregisterdate, usertype) VALUES ('" + username + "', '" + useremail + "', '" + userpassword + "', '" + userregisterdate + "', '" + usertype + "')")

print("The query typed in was: " + cursor.query + " and you have been succesfully added to the database")
print("")
print("The user table is now:")

cursor.execute("SELECT * FROM users;")
rows = cursor.fetchall()

for r in rows:
    print(r)
print("")




    #now we are adding the user to the corresponding subclass table, depending on their type; either learner or staff.
if (usertype == "staff"):

    cursor.execute("INSERT INTO staff(staffid, staffphone, staffemail) SELECT userid, null, useremail FROM users u WHERE NOT EXISTS (SELECT 1 FROM staff s WHERE s.staffID = u.userID) AND  u.usertype = 'staff';")

    print("You chose the staff user type subclass. Please enter the following information to be added to the staff data table")
    print("")

    staffphonenumber = raw_input("What is your phone number?: ")
    print("")



    cursor.execute("update staff SET staffphone = '" + staffphonenumber + "' WHERE staffphone IS NULL; ")
    print("The query that was executed is: ")
    print(cursor.query)

    print("")
    print("The staff table is now:")
    cursor.execute("SELECT * FROM staff;")
    rows = cursor.fetchall()

    for r in rows:
        print(r)
    print("")


if (usertype == "learner"):

    cursor.execute("INSERT INTO learner(learnerid) SELECT userid FROM users u WHERE NOT EXISTS (SELECT 1 FROM learner l  WHERE l.learnerID = u.userID) AND  u.usertype = 'learner';")

    print("You chose the learner user type subclass. Please enter the following information to be added to the learner data table")
    print("")

    learnerfavoritetopic = raw_input("What is your favorite academic topic?: ")
    print("")
    learnerbio = raw_input("Tell us a bit about yourself: ")
    print("")
    learnerskilllevel = raw_input ("What is your skill level (Beginner to Professional)?: ")
    print("")
    learnerlastlog = daymonthyear

    print("Now inserting the data you've inputted into the staff data table")
    cursor.execute("update learner set learnerfavoritetopic = '" + learnerfavoritetopic + "', learnerbio = '" + learnerbio + "', learnerskilllevel = '"+ learnerskilllevel + "', learnerlastlog = '" + learnerlastlog + "' WHERE learnerfavoritetopic is NULL;")
    print("The query that was executed is: ")
    print(cursor.query)

    print("")
    print("The learner table is now:")
    cursor.execute("SELECT * FROM learner;")
    rows = cursor.fetchall()

    for r in rows:
        print(r)
    print("")




print("")
print("here are the sample MATERIALS to create sequences")
cursor.execute("SELECT * FROM material;")
rows = cursor.fetchall()

for r in rows:
    print(r)
print("")



print("here are the SEQUENCES")
cursor.execute("SELECT * FROM sequence;")
rows = cursor.fetchall()

for r in rows:
    print(r)
print("")

print("here are the ENTRIES")
cursor.execute("SELECT * FROM entry;")
rows = cursor.fetchall()

for r in rows:
    print(r)
print("")

print("Would you like to add a material the the testbook")
addmaterialanswer = raw_input("Type in 'yes' or 'no' (or you will be queried again) : ")

#enter while loop, keep looping until 'yes' or 'no' answer is provided
while addmaterialanswer != 'yes' or addmaterialanswer != 'no':
    addmaterialanswer = raw_input("please answer if you would like to add a material (yes) or continue onto the sequences (no): ")
    if addmaterialanswer == 'yes' or addmaterialanswer == 'no':
        break

#add a material, you answered yes
hasqbeentapped = 1
if addmaterialanswer == 'yes':
    while hasqbeentapped:
        print("")
        print("We will now be inserting a material into the material table")
        #material table has the following columns
        #id (autoinc)
        #materialsource = uvic? harvard?
    #materiallink = url
    #materialtype = video? pdf?
    #materialSubject = Math?
    #materialGrade = 1st year uni? Grade 8? etc...
    #materialdateProduced = simple date
    #
    #WE WILL DISSALOW MATERIAL THAT HAS AN IDENTICAL URL TO THAT OF A MATERIAL ALREADY IN THE TABLE
        newmaterialsource =  raw_input("What is the source of the material? For example Harvard or Uvic: ")
        newmateriallink = raw_input("What is the url of your material: ")
        newmaterialtype = raw_input("What is the type/format of your material? For example Video or PDF: ")
        newmaterialsubject = raw_input("What is the subject of material? For example Math or Chemistry: ")
        newmaterialgrade = raw_input("What is the intended grade of the material?: For example first year University or Elementary School:")
        newmaterialdifficulty = raw_input("On a scale of 1 to 10 how hard is this material? 10 being hardest: ")
        newmaterialdateproduced = raw_input("What is the date of the material produced?: Please type it in the form 'YYYY-MM-DD' (Example: 1998-10-01) or else the program will crash: ")

        cursor.execute("SELECT materiallink FROM material WHERE materiallink = '" + newmateriallink + "';")
        doesmaterialexist = cursor.fetchone()
        if doesmaterialexist != None:
            print("The URL you provided in the database already exists")
            qinput = raw_input("Please press the 'q' button if you would like to quit the process of inserting new material into the database: ")
            if qinput == 'q':
                print("'q' has been tapped and the process of new material is now moving on")
                hasqbeentapped = 0
            else:
                print("'q' was not tapped, so we will be attempting to insert new material again")

        else:
            #insert
            print("The url you provided is unique, indicating a material not yet known to the database")
            print("")
            print("Now inserting the inputted data into the DB")
            cursor.execute("INSERT INTO material (materialsource, materiallink, materialtype, materialsubject, materialgrade, materialdifficulty, materialdateproduced) VALUES ('" +newmaterialsource+ "', '" +newmateriallink+ "', '" +newmaterialtype+ "', '" +newmaterialsubject+ "', '" +newmaterialgrade+ "', " +newmaterialdifficulty+ ", '" +newmaterialdateproduced+ "');")
            print("The executed query was" + cursor.query)
            #select
            cursor.execute("SELECT * FROM material;")
            print("Now displaying material table with new material inserted")
            print("The query used was: " + cursor.query)
            print("")

            rows = cursor.fetchall()
            for r in rows:
                print(r)

            qinput = raw_input("Please press the 'q' button if you would like to quit the process of inserting new material into the database: ")
            if qinput == 'q':
                print("'q' has been tapped and the process of new material is now moving on")
                hasqbeentapped = 0
            else:
                print("'q' was not tapped, so we will be attempting to insert new material again")
                break



if addmaterialanswer == 'no':
    print("")
    print("you selected no, continuing with the script")



'''
#sequence testing
print("Sequence testing is now underway")
print("Here are the current sequences")
print("")
cursor.execute("SELECT * FROM sequence;")
rows = cursor.fetchall()
for r in rows:
    print(r)
print("Would you like to create a new sequence?")
print("Press the 'y' key to create a new sequence, or press 'n' to not input a new sequence or create new entries")
#this 'hasqbeentapped' variable is for the while loop
#the while loop below here adds consistent sequences, and the nested while loop within the one below adds entries to new sequences
#once enough entries have been added to the desired sequence, then the nested while loop true condition will break, indicating that no more entries are added to the sequence
#once the nested loop is finished, update some sequence data and break the hasqbeentapped condition if a user wishes to exit the sequence creating process
hasqbeentapped = 1
while qhasbeentapped = True:
    # sequence columns are listed below
    # we will first be creating a sequence, followed by entries corresponding/belonging to the sequence
    # sequencedescription
    # sequencesize,
    # sequencename,
    # sequencedifficulty
    print("A sequence consists of entries, however first we need to define some characteristics of your sequence")
    print("Sequence description, sequence name and sequence difficulty will be now inputted, however the sequence size will be default 0 until entries are entered")
    newsequencesize = 0
    newsequencename = raw_input("Please define your sequence name : ")
    newsequencedescription = raw_input("Please give a short bio/description of what your sequence entails : ")
    newsequencedifficulty = raw_input("Please input the level of difficulty that your sequence is : ")

    cursor.execute("INSERT INTO sequence(sequencedescription, sequencesize, sequencename, sequencedifficulty) VALUES ('" +newsequencedescription+ "', '" +newsequencesize+ "', '" +newsequencename+ "', '" +newsequencedifficulty+ "');")
    print("")
    print("The query used was: " + cursor.query)
    print("The resulting row set for sequences is: ")
    print("")
    cursor.execute("SELECT * from sequence;")
    rows = cursor.fetchall()
    for r in rows:
        print(r)
    print("")
    print("Now populating sequence with entries ")
    print("")
    print("Displaying the entries that are available to select from")
    #newentryloop is a variable that maintains the looping of the while loop while adding entries
    #if newentryloop flips to 0, then quit the looping of adding entries
    newentryloop = 1
    newentryposition = 0
    while newentryloop:
        print("This is the process of adding a material/entry to your sequence")
        newsequencesize = newsequencesize + 1
        print("Remember the ID of the material that you want to select, as it will be used to reference and create entries")
        cursor.execute("SELECT * from material;")
        rows = cursor.fetchall()
        for r in rows:
            print(r)
        print("")
        print("Please now select the new entry you would like to add to your entry list. Also note this will be the first entry in the list!")
        newentryposition = newentryposition + 1
        newentrymatID = raw_input("Please select the ID of material that you want to add to your sequence from the available table displayed above: ")
        newentrydescription = raw_input("Please input a small sentence as to why you want this entry included in the DB: ")
        #fetch the id of the sequence added in the while loop depending on 'hasqbeentapped'
        #newsentryseqID - select the ID of the sequence for which the name matches newsequencename
        cursor.execute("SELECT sequenceID from sequence where sequencename = " + newsequencename + ";")
        newentryseqID = cursor.fetchone()
        #now begin to insert the entry data into the entry table
        cursor.execute("INSERT INTO entry (relsequenceID, relmaterialID, entryRelevance, entryPosition) VALUES ('"+newentryseqID+"', '"+newentrymatID+"',  '"+ newentrydescription +"',  '" + newentrydescription +"' );")
        print("")
        print("press 'y' to continue adding entries to the sequence, press 'n' to stop adding entries to the sequence")
        print("")
        queryentries = raw_input("Would you like to continue the process of inserting entries into your newly created sequence?")
        if queryentries != 'y':
            print("You did not end up tapping/pressing 'y'")
            print("Now terminating the entry creation process")

        else:


        # ENTRY table details
        # EntryID SERIAL -this entryID is a unique identifier to every entry
        # relsequenceID int NOT NULL -this references the sequence the entry belongs to.
        # DUE TO SIMPLICITY, sequences will only be allowed modification upon new creation of a sequence
        # relmaterialID int NOT NULL, relmaterialid is the id of the material that the entry referenes
        # entryRelevance varchar(50), entry relevance is a short description as to why this entry is relevant to the sequence
        # entryPosition smallint NOT NULL,
        #
        #
        # KEYS
        # PRIMARY KEY (entryID), FOREIGN KEY (relmaterialID) references material(materialID), FOREIGN KEY (relsequenceID) references sequence(sequenceID));








'''
#commit the updates
conn.commit()


#close the cursor
cursor.close()

#close the connection
conn.close()
