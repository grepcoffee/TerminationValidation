import bs4
import pyad
from datetime import  datetime as dt
from pyad import pyadutils, adquery

htmlfile = open('report.html')
textfile = open('lastlogin.txt',"r")
COMPANYBASEDN = "DC=company,DC=com"
tablelist = []

def parseHTML(input):
    soup = bs4.BeautifulSoup(input,features="lxml")
    tables = soup.findChildren('table')

    my_table = tables[1]

    rows = my_table.findChildren(['th', 'tr'])

    for row in rows:
        cells = row.findChildren('td')
        for cell in cells:
            value = str(cell.string).replace(u'\xa0', u'')
            tablelist.append(value)
    return tablelist

parseHTML(htmlfile)

del tablelist[:9]

def divide_chunks(l, n):
    for i in range(0, len(l), 9):
        yield l[i:i + n]

dividedlist = list(divide_chunks(tablelist, 9))

def adsearching(input):
    try:
        for i in input:
            q = pyad.adquery.ADQuery()
            usrid = i[1]
            nusrid = str("employeeID =" +usrid)
            q.execute_query(
                attributes=["mailNickname", "employeeID", "lastLogonTimeStamp"],
                where_clause= nusrid,
                base_dn=COMPANYBASEDN
            )

        for row in q.get_results():
            EmployeeID = (row['employeeID'])
            LastLogon = (pyadutils.convert_datetime(row['lastLogonTimeStamp']))
            Name = (row['mailNickname'])
            LastLogonDate = LastLogon.strftime('%m/%d/%Y')

        for i in dividedlist:
            if EmployeeID in i:
            timediff = dt.strptime(LastLogonDate, '%m/%d/%Y') - dt.strptime(i[7],'%m/%d/%Y')
            if timediff.days > 0:
            print("User " + Name + " Was Terminated on "+str(i[7])+" and last logged in on "+LastLogonDate+" which is "+str(timediff.days)+" days after his termination")

    except ValueError as e :
        print("Error "+str(e)+" in user "+Name+" Check HTML and AD Manually")

print("\n")
adsearching(dividedlist)
