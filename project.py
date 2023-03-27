import mysql.connector
import PySimpleGUI as sg

db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="yadidiah",
    database="restrauntmenu"
)

myCursor = db.cursor()
sg.theme('DarkAmber')
def insert_meal(id,meal_name,meal_price,meal_type,meal_ingredients):
    
    query ="INSERT INTO meals(meal_id, name, price, type, ingredients) VALUES({}, '{}', {}, '{}', '{}')".format(id,meal_name,meal_price,meal_type,meal_ingredients)
    myCursor.execute(query)
    db.commit()
    print(myCursor.rowcount, "Record inserted successfully into meals table")
    
def delete_meal(id: int):
    
    query = "DELETE FROM meals WHERE meal_id={}".format(id)
    myCursor.execute(query)
    print(myCursor.rowcount, "record(s) deleted from meals table")
    db.commit()
    
def update_meal(id,change,ans):
    query = "UPDATE meals SET {} = {} WHERE meal_id={}".format(change,ans,id)
    myCursor.execute(query)
    print(f"{change} has been changed for meal with id {id}")
    db.commit()

def filter_search(filters):
    query = "SELECT * FROM meals WHERE "
    filter_queries = []
    
    for key, value in filters.items():
        if value is not None and value != "":
            if isinstance(value, str):
                if value[0] =="<":
                    val = int(value[1:])
                    filter_queries.append(f"{key}<{val}")
                elif value[0] ==">":
                    val = int(value[1:])
                    filter_queries.append(f"{key}>{val}")
                elif value[0] =="=":
                    val = int(value[1:])
                    filter_queries.append(f"{key}={val}")
                else:
                    filter_queries.append(f"{key} LIKE '%{value}%'")
            else:
                filter_queries.append(f"{key}={value}")
    query += " AND ".join(filter_queries)
    myCursor.execute(query)
    data = myCursor.fetchall()
    return data


myCursor.execute('SELECT * FROM meals')
data = myCursor.fetchall()


meal_options = [row[0] for row in myCursor.fetchall()]

options = ['id', 'name', 'price','type','ingredients']
layout = [
        [[sg.Table(key="table",values=data, headings=[i[0] for i in myCursor.description],num_rows=20,max_col_width=75, auto_size_columns=True, justification='center')]],
        [sg.Text("Enter:")],
        [sg.Button("Insert Meal")],
        
        [sg.Text("Enter Meal ID (Number):",key='text1', visible=False), sg.Input(key='input1', visible=False), 
        sg.Text('Enter Meal Name:',key='text2', visible=False), sg.InputText(key='input2', visible=False)],
        [sg.Text('Enter Meal Price (Number):',key='text3', visible=False), sg.InputText(key='input3', visible=False),
        sg.Text('Enter Meal Type',key='text4', visible=False), sg.InputText(key='input4', visible=False)], 
        [sg.Text('Enter All Ingredients(add spaces before next value):',key='text5', visible=False), sg.InputText(key='input5', visible=False),
        sg.Button("Submit", key="submit",visible=False),

        sg.Button("Delete Meal")],
        [sg.Text("Enter the id to delete:", key ="delete_id", visible=False),
        sg.Input(key='delete_input', visible=False)],


        [sg.Button("Update Meal",key="update")], 
        [sg.Text("Enter the id to Update:", key ="update_id", visible=False),sg.Input(key='update_input', visible=False)],
        [sg.Text("Enter what to change (add space if multiple):", key ="change", visible=False),sg.Input(key='change_input', visible=False)],
        [sg.Text("Enter the changed values (add space if multiple):", key ="value", visible=False),sg.Input(key='value_input', visible=False)],
        
        [sg.Button("Filter")],
        [sg.Listbox(values=options,key="filter_box" ,size=(20, len(options)), select_mode='multiple',visible=False)],
        [sg.Text("Enter filter:", key ="filter", visible=False),sg.Input(key='filter_input', visible=False)],
        [sg.Button('Enter',key="enter")],
        [sg.Button("QUIT")]

        ]


window = sg.Window('Select your meals', layout)

# read the window for events
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Insert Meal':
        # set the visibility of the four text and input fields to True
        window['text1'].update(visible=True)
        window['input1'].update(visible=True)
        window['text2'].update(visible=True)
        window['input2'].update(visible=True)
        window['text3'].update(visible=True)
        window['input3'].update(visible=True)
        window['text4'].update(visible=True)
        window['input4'].update(visible=True)
        window['text5'].update(visible=True)
        window['input5'].update(visible=True)
        window["submit"].update(visible=True)

    if event== 'submit':
            insert_meal(values["input1"],values["input2"],values["input3"],values["input4"],values["input5"])

    elif event=='Delete Meal':
        window['delete_id'].update(visible=True)
        window['delete_input'].update(visible=True)
       
        if values["delete_input"]:
            var = int(values["delete_input"])
            delete_meal(var)
        else:
            print("Please enter a valid meal ID.")
        

    elif event=="update":
        window['update_id'].update(visible=True)
        window['update_input'].update(visible=True)
        window['change'].update(visible=True)
        window['change_input'].update(visible=True)
        window['value'].update(visible=True)
        window['value_input'].update(visible=True)

        change = values["change_input"].split()
        value = values["value_input"].split()

        for i in range(len(change)):
            update_meal(values["update_input"],change[i],value[i])


    elif event=="Filter":
        window["filter_box"].update(visible=True)
        window["filter"].update(visible=True)
        window["filter_input"].update(visible=True)

        window["enter"].update(visible=True)
    if event== 'enter':
        list1 = values["filter_input"].split()
        dict_values={}
        for i in range(len(values["filter_box"])):
            dict_values[values["filter_box"][i]]=list1[i]
        

        data = filter_search(dict_values)
        if data:
            window["table"].update(values=data,)
        else:
            print("No data found.")
                    

        
        


    elif event == 'QUIT':

        sg.popup('GOODBYE! 😁 ')
        break


window.close()
db.close()



