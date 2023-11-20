import sqlite3
from datetime import datetime, timedelta
import random

# La cantidad de propietarios está acotada, y se
# identifican por su documento de identidad. De cada auto se conoce 

# nombre
# documento de identidad  (máximo 5 AUTOS)
# marca
# modelo
# matrícula
# mes de último pago de su seguro. 

# Accidentes en un mes: 

# número de matrícula del auto del denunciante 
# día del accidente. 
# Descripción de la causa del choque.

original_owners = {
    305678912: {
        'name': 'John Doe',
        'cars': [
            {
                'model': 'Toyota Camry',
                'plate': 'ABC123',
                'payment_date': '2022-09-15'
            },
            {
                'model': 'Honda Civic',
                'plate': 'XYZ789',
                'payment_date': '2022-08-20'
            },
        ]
    },
    208765432: {
        'name': 'Jane Smith',
        'cars': [
            {
                'model': 'Ford Explorer',
                'plate': 'DEF456',
                'payment_date': '2022-10-05'
            },
        ]
    },
    109876543: {
        'name': 'Bob Johnson',
        'cars': [
            {
                'model': 'Chevrolet Malibu',
                'plate': 'GHI789',
                'payment_date': '2022-07-12'
            },
            {
                'model': 'Nissan Altima',
                'plate': 'JKL012',
                'payment_date': '2022-09-28'
            },
            {
                'model': 'Tesla Model 3',
                'plate': 'MNO345',
                'payment_date': '2022-11-03'
            },
        ]
    },
    124567890: {
        'name': 'Alice Brown',
        'cars': [
            {
                'model': 'Volkswagen Jetta',
                'plate': 'PQR678',
                'payment_date': '2022-08-10'
            },
            {
                'model': 'Subaru Outback',
                'plate': 'STU901',
                'payment_date': '2022-12-22'
            },
        ]
    },
    345678901: {
        'name': 'Charlie Wilson',
        'cars': [
            {
                'model': 'Hyundai Sonata',
                'plate': 'VWX234',
                'payment_date': '2022-11-18'
            },
            {
                'model': 'Kia Sportage',
                'plate': 'YZA567',
                'payment_date': '2022-10-01'
            },
            {
                'model': 'Mazda CX-5',
                'plate': 'BCD890',
                'payment_date': '2022-09-07'
            },
        ]
    },
    987654321: {
        'name': 'Eva Davis',
        'cars': [
            {
                'model': 'Jeep Wrangler',
                'plate': 'EFG123',
                'payment_date': '2022-07-29'
            },
            {
                'model': 'Ram 1500',
                'plate': 'HIJ456',
                'payment_date': '2022-10-15'
            },
            {
                'model': 'Chevrolet Tahoe',
                'plate': 'KLM789',
                'payment_date': '2022-11-28'
            },
            {
                'model': 'Ford F-150',
                'plate': 'NOP012',
                'payment_date': '2022-12-10'
            },
        ]
    },
    123456789: {
        'name': 'Grace Taylor',
        'cars': [
            {
                'model': 'Audi A4',
                'plate': 'UVW456',
                'payment_date': '2022-11-05'
            },
            {
                'model': 'BMW X5',
                'plate': 'XYZ789',
                'payment_date': '2022-10-18'
            },
            {
                'model': 'Mercedes-Benz C-Class',
                'plate': 'MNO123',
                'payment_date': '2022-09-25'
            },
        ]
    },
    334455667: {
        'name': 'Samuel Rodriguez',
        'cars': [
            {
                'model': 'Ford Mustang',
                'plate': 'PQR456',
                'payment_date': '2022-12-02'
            },
            {
                'model': 'Chevrolet Corvette',
                'plate': 'STU789',
                'payment_date': '2022-10-12'
            },
        ]
    },
}

original_accidents = {
    'ABC123': [{'accident_date': '2023-11-01', 'description': 'Minor fender bender'}],
    'XYZ789': [{'accident_date': '2023-10-15', 'description': 'Side collision at an intersection'},
               {'accident_date': '2023-09-23', 'description': 'Parking lot incident'}],
    'GHI789': [{'accident_date': '2023-08-30', 'description': 'Rear-end collision on the highway'},
               {'accident_date': '2023-07-12', 'description': 'Minor accident while exiting a driveway'},
               {'accident_date': '2023-06-05', 'description': 'Side-swipe while merging onto the highway'}],
    'MNO345': [{'accident_date': '2023-05-20', 'description': 'Hit and run'}],
    'PQR678': [{'accident_date': '2023-04-09', 'description': 'Minor scratches from a parallel parking attempt'},
               {'accident_date': '2023-03-02', 'description': 'Side-swipe on a narrow street'},
               {'accident_date': '2023-02-14', 'description': 'Collision while reversing'}],
    'STU901': [{'accident_date': '2023-01-07', 'description': 'Intersection collision'}],
    'YZA567': [{'accident_date': '2022-12-10', 'description': 'Parking lot fender bender'},
               {'accident_date': '2022-11-18', 'description': 'Collision while changing lanes'}],
    'BCD890': [{'accident_date': '2022-10-25', 'description': 'Rear-end collision in traffic'}],
    'HIJ456': [{'accident_date': '2022-09-15', 'description': 'Minor accident during parallel parking'},
               {'accident_date': '2022-08-03', 'description': 'Side-swipe while merging onto the highway'}],
    'KLM789': [{'accident_date': '2022-07-22', 'description': 'Parking lot incident'}],
    'NOP012': [{'accident_date': '2022-06-11', 'description': 'Side collision during heavy rain'},
               {'accident_date': '2022-05-04', 'description': 'Parking lot fender bender'},
               {'accident_date': '2022-04-17', 'description': 'Collision while reversing'}],
    'MNO123': [{'accident_date': '2022-03-29', 'description': 'Rear-end collision at a stoplight'}],
    'PQR456': [{'accident_date': '2022-02-10', 'description': 'Minor accident during parallel parking'},
               {'accident_date': '2022-01-18', 'description': 'Side-swipe while merging onto the highway'}],
    'STU789': [{'accident_date': '2021-12-29', 'description': 'Parking lot incident'},
               {'accident_date': '2021-11-14', 'description': 'Rear-end collision in traffic'},
               {'accident_date': '2021-10-27', 'description': 'Minor accident while exiting a driveway'}],
}

# TABLE 01 OWNERS
def createOwnersDataBase(original_owners,conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS owners
                        (id INTEGER,
                        name TEXT,
                        model TEXT,
                        plate TEXT PRIMARY KEY,
                        payment_date DATE
                        )''')

    cursor.execute("SELECT COUNT(*) FROM owners")
    row_count = cursor.fetchone()[0]

    if row_count == 0:
        for id, owner_data in original_owners.items():
            name = owner_data['name']
            
            # Check if 'cars' key exists and has at least one car
            if 'cars' in owner_data and owner_data['cars']:
                # Loop through each car in the 'cars' list
                for car in owner_data['cars']:
                    model = car.get('model', 'Unknown Model')  # Use 'Unknown Model' if 'model' is missing
                    plate = car.get('plate', 'Unknown Plate')  # Use 'Unknown Plate' if 'plate' is missing
                    payment_date = car.get('payment_date', 'Unknown Date')  # Use 'Unknown Date' if 'payment_date' is missing
                    
                    cursor.execute("INSERT INTO owners (id, name, model, plate, payment_date) VALUES (?, ?, ?, ?, ?)",
                                (id, name, model, plate, payment_date))

    conn.commit()

# TABLE 02 ACCIDENTS

def createAccidentsDataBase(original_accidents,conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS accidents
                        (plate TEXT,
                        accident_date DATE,
                        description TEXT
                        )''')

    cursor.execute("SELECT COUNT(*) FROM accidents")
    row_count = cursor.fetchone()[0]

    if row_count == 0:
        for plate, accidents in original_accidents.items():
            for accident in accidents:
                accident_date = accident.get('accident_date', 'Unknown Date')  # Use 'Unknown Date' if 'accident_date' is missing
                description = accident.get('description', 'Unknown Description')  # Use 'Unknown Description' if 'description' is missing
                
                cursor.execute("INSERT INTO accidents (plate, accident_date, description) VALUES (?, ?, ?)",
                            (plate, accident_date, description))

    conn.commit()

def printColumns(data, cursor):
    columns = [column[0] for column in cursor.description]

    fixed_width = 10

    # Column headers
    header_str = "|".join(str(column).upper().ljust(fixed_width) for column in columns)
    print(header_str)
    print("-" * (fixed_width * len(columns)))  

    for row in data:
        formatted_row = [str(value).ljust(fixed_width) for value in row]
        row_str = "|".join(formatted_row)
        print(row_str)

def defineAction():
    print(
        '\nAcciones\n\n[A] Dar de alta un libro\n[B] Dar de baja un libro\n[M] Modificar un libro\n[L] Listar los libros\n')
    return input('Ingrese la acción que desea realizar: ').upper()

# FUNCTIONS -----------------------------------------------------------------------------------------------------------------------

def listEverything(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM accidents")

    data = cursor.fetchall()
    printColumns(data, cursor)

def listCars(conn):
    cursor = conn.cursor()

    id_list = int(input('Ingrese el id del usuario a quien listar: ')) 
    cursor.execute("SELECT * FROM accidents WHERE id LIKE ? ORDER BY model",
                   (id_list,))

    data = cursor.fetchall()
    printColumns(data, cursor)

# MAIN ----------------------------------------------------------------------------------------------------------------------------

def main(): 
    # Open connection
    conn = sqlite3.connect('cars.db')

    createOwnersDataBase(original_owners,conn)
    # createAccidentsDataBase(original_accidents,conn)

    action = defineAction()

    if action == 'L':
        listEverything()
    elif action == 'LC':
        listCars(conn)
    # elif action == ''
    
    # Close connection
    conn.close()
    print('Se ha cerrado la conexión')

main()

# 1. Dada el documento de un propietario, saber que autos posee un propietario. 
# 2. Dada la matrícula de un auto, conocer el nombre de su dueño. 
# 3. Dada la matrícula de un auto, devolver la lista de los accidentes que tuvo en el año,
# (opcional: ordenada por fecha). 
# 4. Dada la fecha actual, listar los propietarios que están atrasados en el pago (aquellos
# cuyo mes de útimo pago es menor que el mes actual) y en qué coche. (opcional: listado
# ordenado por nombre de propietario). 
# 5. Dado un mes devolver la lista de matrículas de autos accidentados en dicho mes
# ordenada por día. 
# 6. Dar de alta los datos de un accidente en la base de datos. Se puede asumir que los
# accidentes son ingresados en el mismo orden histórico en que suceden.
# 7. Dados el nombre y el documento de un propietario y los datos relativos a un auto,
# agregar dicho auto a la lista de autos que posee dicho propietario. En caso de que el
# propietario no figure en la estructura hay que darlo de alta.
# 8. Grabar los datos de la base de datos en un archivo binario.