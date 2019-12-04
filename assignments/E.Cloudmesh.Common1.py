from cloudmesh.common.util import banner, HEADING
from cloudmesh.common.debug import VERBOSE

banner("This is my first print command",debug=True,label="Label for Banner",color="GREEN")

banner("Trying out Heading")
HEADING("This is interesting!",c='#',color='HEADER')

banner("This is Verbose")
d = {"January": "1", "February": "2", "March":"3","April":"4","May":"5","June":"6","July":"7","August":"8","September":"9","October":"10","November":"11","December":'12'}
VERBOSE(d,label="Months",color='RED', verbose=-10)