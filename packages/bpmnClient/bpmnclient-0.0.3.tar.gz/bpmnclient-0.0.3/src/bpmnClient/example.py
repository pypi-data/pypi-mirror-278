
from client import *

cl = Client('http://localhost:3000','12345')

#cl.model.list();


#print(cl.status())

#cl.data.findInstnaces({"name":'Buy Used Car'})

cl.engine.start('Buy Used Car',{}).listItems().dump()
#Report.dump(res)
#cl.listItems(res)
