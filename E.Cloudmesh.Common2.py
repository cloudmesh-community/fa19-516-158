from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.util import banner

data = dotdict ({"Red":"0","Blue":"1","Green":2})
banner(data["Red"],color='RED')
banner(data["Blue"],color='BLUE')
# banner(data["Green"],debug=True,color='GREEN')
# banner("Is there an issue with Green?",data["Green"],color='GREEN')
if data["Red"] is "0":
    print("This is Red")