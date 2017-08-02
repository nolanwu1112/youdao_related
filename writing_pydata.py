import sqlite3

def data_wrangle(input_der):
    if '[' in input_der:
        index_start = input_der.find('[')
        index_end = input_der.find(')')
        new_string = input_der[:index_start] + input_der[index_end+1:]
        return data_wrangle(new_string)
    else: 
        return input_der

derivative = {}
with sqlite3.connect("./database/vocab.db") as connection:
    c = connection.cursor()
    c.execute("SELECT vocab, derivatives FROM pho;")
    result = c.fetchall()

for item in result:
    value = data_wrangle(item[1])
    derivative[item[0]] = value
    
with open("derivatives_data.py", "w") as file:
    file.write(str(derivative))
