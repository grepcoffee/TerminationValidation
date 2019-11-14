import bs4
import pyad
from pyad import pyadutils, adquery

# Declare Variables
COMPANYBASEDN = "DC=company,DC=com"
htmlfile = open('report.html')
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
 for i in input:
#    print(i[1])
    q = pyad.adquery.ADQuery()
    usrid = i[1]
    nusrid = str("employeeID =" +usrid)
    q.execute_query(
        attributes=["mailNickname", "employeeID", "lastLogonTimeStamp"],
        where_clause= nusrid,
        base_dn= COMPANYBASEDN
    )
    for row in q.get_results():
        EmployeeID = (row['employeeID'])
        LastLogon = (pyadutils.convert_datetime(row['lastLogonTimeStamp']))
        Name = (row['mailNickname'])
        LastLogonDate = LastLogon.strftime('%m/%d/%Y')
        print(Name, EmployeeID, LastLogonDate)

#Script Terminal Output

adsearching(dividedlist)
