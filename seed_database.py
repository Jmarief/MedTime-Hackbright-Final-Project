"""Seed Database, drop db, create db and populate db with data"""

import crud
import model
import server

# os.system('dropdb medtime')
# os.system('createdb medtime')

model.connect_to_db(server.app)
model.db.create_all()

"""Create a test user"""

# for n in range(1, 5):
# email = f'user{n}@test.com'
# password = 'test'
# f_name = 'test'
# l_name = 'testzzz'

crud.create_user('Testfname', 'Testlname', 'test@test.com', '1234678910', 'testpassword')
crud.create_medications('RX1', 'Take once at bedtime', 'blah blah')
crud.create_user_medications(1, 2, 100, 1)
crud.create_reminders(2, 2, '12-10-2021', "2021-12-10 22:00:00", '12-10-2021', 0)