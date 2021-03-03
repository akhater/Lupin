import calendar
import datetime

import utils
from config import getfirstDayOfWeek


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

    if(datetime.date.today().year == year and datetime.date.today().month == month):
        outofmonth = ""
    else:
        outofmonth = " outofmonth"
    
    dayClass = ""
    for week in cal.monthdays2calendar(year, month):
        HTMLOUT += "<tr>"
        for day in week:
            if(day[0]):
                calday = datetime.date(year, month, day[0])
                dateFormat =  utils.styleDateTime(datetime.date(year, month, day[0]), dateFormatter)
                if(datetime.date.today() == datetime.date(year, month, day[0])):
                    dayClass = "page-ref today" 
                elif utils.pageExists(utils.styleDateTime(calday, dateFormatter)):
                    dayClass += "page-ref page-exists" + outofmonth
                else:
                    dayClass = "page-ref" + outofmonth
                HTMLOUT += ("""<td><a data-ref="{}" href="#/page/{}" class="{}">{}</a></td>""").format(dateFormat, dateFormat, dayClass, day[0])
            else:
                HTMLOUT += "<td></td>"
        HTMLOUT += "</tr>"

    HTMLOUT += "</tbody></table></div><!--LupinCalendarEnds-->"

    return HTMLOUT

