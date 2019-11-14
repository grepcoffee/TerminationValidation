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
##

###
print("\n")
adsearching(dividedlist)
