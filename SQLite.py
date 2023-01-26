import sqlite3
import os

def sanityCheck(line):
    noQuotes = []
    out = ""
    for idx in range(0,len(line.strip().split(","))):
        tmp = line.split(",")[idx].strip()
        if(idx not in noQuotes):
            tmp = "'" + tmp + "'"
        tmp += ","
        out += tmp
    return out[:-1]

conn = 0
cursor = 0
dbPath = "census-income.db"

if(not os.path.exists(dbPath)):
    #Creating a new database
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    #Create a new table
    createTableQuery = "CREATE TABLE Income(SS_ID INTEGER PRIMARY KEY AUTOINCREMENT, AAGE int, ACLSWKR varchar(100), ADTIND varchar(100) , ADTOCC varchar(100) , AHGA varchar(100) , AHRSPAY int , AHSCOL varchar(100) , AMARITL varchar(100) , AMJIND varchar(100) , AMJOCC varchar(100) , ARACE varchar(100) , AREORGN varchar(100) , ASEX varchar(100) , AUNMEM varchar(100) , AUNTYPE varchar(100) , AWKSTAT varchar(100) , CAPGAIN int , CAPLOSS int , DIVVAL int , FILESTAT varchar(100) , GRINREG varchar(100) , GRINST varchar(100) , HDFMX varchar(100) , HHDREL varchar(100) , MARSUPWT number , MIGMTR1 varchar(100) , MIGMTR3 varchar(100) , MIGMTR4 varchar(100) , MIGSAME varchar(100) , MIGSUN varchar(100) , NOEMP number , PARENT varchar(100) , PEFNTVTY varchar(100) , PEMNTVTY varchar(100) , PENATVTY varchar(100) , PRCITSHP varchar(100) , SEOTR varchar(100) , VETQVA varchar(100) , VETYN varchar(100) , WKSWORK number , YEAR varchar(100) , TRGT varchar(100))"
    # print(createTableQuery)
    cursor.execute(createTableQuery)
    conn.commit()

    data = []
    with open("census-income.data","r") as f:
            data = f.readlines()

    #Insert Data
    insertQuery = "INSERT INTO Income(AAGE, ACLSWKR, ADTIND, ADTOCC, AHGA, AHRSPAY, AHSCOL, AMARITL, AMJIND, AMJOCC, ARACE, AREORGN, ASEX, AUNMEM, AUNTYPE, AWKSTAT, CAPGAIN, CAPLOSS, DIVVAL, FILESTAT, GRINREG, GRINST, HDFMX, HHDREL, MARSUPWT , MIGMTR1, MIGMTR3, MIGMTR4, MIGSAME, MIGSUN, NOEMP , PARENT, PEFNTVTY, PEMNTVTY, PENATVTY, PRCITSHP, SEOTR, VETQVA, VETYN, WKSWORK , YEAR, TRGT) VALUES ("

    for line in data:
        # cursor.execute(insertQuery + ")")
        cursor.execute(insertQuery + sanityCheck(line) + ")")

else:
    conn = sqlite3.connect("census-income.db")
    cursor = conn.cursor()

# Question 3 - Male/Female Count in each race group
fromTable2 = cursor.execute("SELECT ARACE,ASEX,COUNT(SS_ID) FROM Income GROUP BY ARACE,ASEX")
print("------- Question 3 - Male/Female Count -------")
for result in fromTable2:
    print(str(result))

# Question 4
fromTable3 = cursor.execute("SELECT ARACE,ROUND(AVG(WKSWORK*AHRSPAY*40),2) FROM Income WHERE AHRSPAY IS NOT NULL GROUP BY ARACE")
print("------- Question 4 - average annual income per race group -------")
for result in fromTable3:
    print(str(result))

# Question 5-1
fromTable4 = cursor.execute("CREATE TABLE IF NOT EXISTS Person AS SELECT SS_ID, AAGE, AHGA, ASEX, PRCITSHP, PARENT, GRINST, GRINREG, AREORGN, AWKSTAT FROM Income")
print("------- Question 5 - Table Person -------")

# Question 5-2
fromTable5 = cursor.execute("CREATE TABLE IF NOT EXISTS Job AS SELECT SS_ID, ADTIND, ADTOCC, AMJOCC, AMJIND FROM Income")
print("------- Question 5 - Table Job -------")

# Question 5-3
fromTable6 = cursor.execute("CREATE TABLE IF NOT EXISTS Pay AS SELECT SS_ID, AHRSPAY, WKSWORK FROM Income")
print("------- Question 5 - Table Pay -------")

# Question 6-1
fromTable7 = cursor.execute("SELECT MAX(P.AHRSPAY), COUNT(Pr.GRINST), Pr.GRINST, MAX(J.ADTIND), MAX(J.ADTOCC) FROM Person Pr INNER JOIN Pay P ON Pr.SS_ID = P.SS_ID INNER JOIN Job J ON Pr.SS_ID = J.SS_ID GROUP BY Pr.GRINST;")
print("------- Question 6 - Query 1 -------")
for result in fromTable7:
    print(str(result))

# Question 6-2
print("------- Question 6 - Query 2 -------")
fromTable8 = cursor.execute("SELECT COUNT(Pr.AREORGN),  J.AMJIND,Pr.AHGA, ROUND(AVG(P.AHRSPAY),2), ROUND(AVG(P.WKSWORK),2) FROM Person Pr INNER JOIN Pay P ON Pr.SS_ID = P.SS_ID INNER JOIN Job J ON Pr.SS_ID = J.SS_ID WHERE (Pr.AREORGN != 'All other' AND Pr.AREORGN != 'NA' AND Pr.AREORGN != 'Do not know') AND (Pr.AHGA='Bachelors degree(BA AB BS)' OR Pr.AHGA='Masters degree(MA MS MEng MEd MSW MBA)' OR Pr.AHGA='Doctorate degree(PhD EdD)') GROUP BY J.AMJIND,Pr.AHGA ORDER BY Pr.AHGA;")
for result in fromTable8:
    print(str(result))


conn.commit()
conn.close()