import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

structureRF = open('structure.sql','r')
structure = structureRF.read()
structureRF.close()

flag = True
def print_menu():
    init()
    while flag:
        print(
        "There are optins:\n"
              "0) Stop and exit\n"
            "1) Show Active Databases\n"
            "2) Delete all in tables\n"
            "3) Add items to First Table\n"
            "4) Add Items to Second Table\n"
            "5) Delete from First Table\n"
            "6) Delete From Second Table\n"
            "7) Get Data from First Table\n"
            "8) Get Data from Second Table\n"
            "9) Update Data in First Table\n"
            "10) Update Data in Second Table\n"
            "11) Find Data in First Table\n"
            "12) Find Data in Second Table\n"
            "13) Delete data from first Table\n"
            "14) Delete Data from second Table\n"
            "15) Drop Database\n"            
            )
        answer = input()
        switch_option(answer)



def show_active_databases():
    cursor.callproc("show_active_databases")
    for value in cursor:
    	print(value)


def switch_option(answer):	
	try:
		if answer == '1':
			show_active_databases()
		elif answer == '2':
			delete_all_in_tables()
		elif answer == '3':
			add_items_to_first_database()
		elif answer == '4':
			add_items_to_second_database()
		elif answer == '5':
			delete_from_first_database()
		elif answer == '6':
			delete_from_second_database()
		elif answer == '7':
			get_data_from_first_database()
		elif answer == '8':
			get_data_from_second_database()
		elif answer == '9':
			update_data_in_first_table()
		elif answer == '10':
			update_data_in_second_table()
		elif answer == '11':
			find_in_first_table()
		elif answer =='12':
			find_in_second_table()
		elif answer == '13':
			delete_all_in_first_table()
		elif answer == '14':
			delete_all_in_second_table()	
		elif answer =='15':
			delete_database()
		elif answer == '0':
			set_flag_false()
        #else: error_message()
	except Exception as error:
		print (error)



def set_flag_false():
    print("Programm was stopped")
    flag = False
    exit(0)

connection_string = "host=localhost port=5432 dbname=postgres user=sobaka password=123"
connection = psycopg2.connect(connection_string)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()


def init():
     cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE  datname='HS'")
     exists = cursor.fetchone()
     if not exists:
         cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier('HS')))
     connect_database()
     create_tables()


def create_tables():
	cursor.execute(structure)


def delete_database():
    request = input('are you sure?\n(yes or no)')
    if request =='yes':
	    cursor.execute(sql.SQL("DROP DATABASE{}").format(sql.Identifier('HS')))

    	


def execute_database():
    cursor.execute(structure)###########################################################################


def connect_database():
    connection = psycopg2.connect(connection_string)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()


def delete_all_in_tables():
     cursor.callproc("delete_all_in_tables", )

def add_items_to_first_database():
    name=input('Input card name ')
    amount=int(input('Input number of card uve got '))
    total=int(input('Input price of a card '))
    cursor.callproc("add_items_to_first_table",(name, amount, total,))


def add_items_to_second_database():
    person=input('input persons name ')
    satisfaction=input('is he satisfied or not? ')
    cursor.callproc("add_items_to_second_table", (person, satisfaction, ))


def delete_from_first_database():
    get_data_from_first_database()
    target = input('input what you want to delete ')
    cursor.callproc("delete_from_first_table", (target, ))


def delete_from_second_database():
    get_data_from_second_database()
    target = input('input what you want to delete ')
    cursor.callproc("delete_from_second_table", (target, ))


def find_in_first_table():
    target = input('input what you want to find ')
    if (target.isdigit()==True):
    	cursor.callproc("find_in_first_table_integer",(target, ))
    	for elem in cursor.fetchall():
    		print(elem)
    else:	
    	cursor.callproc("find_in_first_table_character",(target, ))
    	for elem in cursor.fetchall():
    		print(elem)
    
def find_in_second_table():
	target = input('input what you want to find ')
	cursor.callproc("find_in_second_table_character",(target, ))
	for elem in cursor.fetchall():
		print(elem)


def error_message():
    print('Whooops...\n'
          'Something went wrong')



def get_data_from_first_database():
	cursor.callproc("get_data_from_first_table")
	for stri in cursor.fetchall():
		print(stri)
	
	
def delete_all_in_first_table():
	cursor.callproc("delete_all_in_first_table")
	
	
def delete_all_in_second_table():
	cursor.callproc("delete_all_in_second_table")
	

	
def get_data_from_second_database():
	cursor.callproc("get_data_from_second_table")
	print('id  person   isSatisf  creationTime   UpdateTime\n')
	for x in cursor.fetchall():
		print(x[0],x[1],x[2],x[3].strftime("%Y-%m-%d %H:%M:%S"),x[4] and x[4].strftime("%Y-%m-%d %H:%M:%S"))
			
	
	
def update_data_in_first_table():
	get_data_from_first_database()
	old_id = input('input strings id you want to update ')
	new_name = input('input new name ')
	new_amount = input('input new amount ')
	new_total = input('input new price ')
	cursor.callproc("update_name_in_first_table",(old_id, new_name,))
	cursor.callproc("update_amount_in_first_table",(old_id, new_amount,))
	cursor.callproc("update_total_in_first_table",(old_id, new_total,))
	
	

def update_data_in_second_table():
	get_data_from_second_database()
	old_id = input('input strings id you want to update ')
	new_person = input('input new name ')
	new_satisfaction = input('input new satisfaction ')
	cursor.callproc("update_person_in_second_table",(old_id, new_person,))
	cursor.callproc("update_satisfaction_in_second_table",(old_id, new_satisfaction,))
	

