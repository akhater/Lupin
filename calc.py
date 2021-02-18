import calendar
import datetime

import utils
from config import getfirstDayOfWeek


def ord(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

def dtStylish(dt,f):
    return dt.strftime(f).replace("{th}", ord(dt.day))

def buildCalendar(year, month):
    firstDayOfWeek = getfirstDayOfWeek()

    cal = calendar.Calendar(firstDayOfWeek)
    dt = datetime.date(year, month, 1)
    dateFormatter = utils.getdateFormatter()

    calendar.setfirstweekday(firstDayOfWeek) 
    daysOfWeek = (calendar.weekheader(2)).split(' ') 
    HTMLOUT = ("""<!--LupinCalendarBegins--><div class="logseq-tools-calendar"><h2>{}</h2><table><thead><tr>""").format(dt.strftime("%B %Y"))
    for dayOfWeek in daysOfWeek:
        HTMLOUT += ("<th>{}</th>").format(dayOfWeek)
    HTMLOUT += "</tr></thead><tbody>"
    #<th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th><th>Sun</th></tr></thead><tbody>

    if(datetime.date.today().year == year and datetime.date.today().month == month):
        outofmonth = ""
    else:
        outofmonth = " outofmonth"
    
    for week in cal.monthdays2calendar(year, month):
        HTMLOUT += "<tr>"
        for day in week:
            if(day[0]):
                calday = datetime.date(year, month, day[0])
                dateFormat =  dtStylish(datetime.date(year, month, day[0]), dateFormatter)
                if(datetime.date.today() == datetime.date(year, month, day[0])):
                    # print(datetime.date(year, month, day[0]))
                    dayClass = "page-ref today" 
                    # HTMLOUT += ("""<td><a data-ref="{}" href="#/page/{}" class="page-ref today">{}</a></td>""").format(dateFormat, dateFormat, day[0])
                # elif utils.pageExists(calday.strftime("%Y_%m_%d")):
                elif utils.pageExists(dtStylish(calday, dateFormatter)):
                    dayClass += "page-ref page-exists" + outofmonth
                    # HTMLOUT += ("""<td><a data-ref="{}" href="#/page/{}" class="page-ref page-exists">{}</a></td>""").format(dateFormat, dateFormat, day[0])
                else:
                    dayClass = "page-ref" + outofmonth
                    # HTMLOUT += ("""<td><a data-ref="{}" href="#/page/{}" class="page-ref">{}</a></td>""").format(dateFormat, dateFormat, day[0])
                HTMLOUT += ("""<td><a data-ref="{}" href="#/page/{}" class="{}">{}</a></td>""").format(dateFormat, dateFormat, dayClass, day[0])
            else:
                HTMLOUT += "<td></td>"
        HTMLOUT += "</tr>"

    HTMLOUT += "</tbody></table></div><!--LupinCalendarEnds-->"

    return HTMLOUT

