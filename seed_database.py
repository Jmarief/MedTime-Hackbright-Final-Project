"""Seed Database, drop db, create db and populate db with data"""

import os
import crud
import model
import server
from datetime import datetime
from datetime import timedelta

os.system('dropdb medtime')
os.system('createdb medtime')

model.connect_to_db(server.app)
model.dp.create_all()

"""Create a test user"""

#for n in range(1, 5):
    #email = f'user{n}@test.com'
    #password = 'test'
    #f_name = 'test'
    #l_name = 'testzzz'

crud.create_user('Testfname', 'Testlname', 'test@test.com', 'testpassword', '1234678910')
crud.create_user_medications('user1', 'rx1', '2', '2x')
crud.create_reminders('medication3', 'rx1', '2', scheduled_date.strptime(10-30-2021, "%-m-%-d-%-y"), scheduled_time.strptime(9-00-AM, 6-00-PM) )
