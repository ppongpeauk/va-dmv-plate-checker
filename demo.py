from PlateAPI import API

obj = API()

while True:
    plate_number = input("Plate Number: ")
    print(f"Query Plate: {plate_number}")
    query = obj.check_plate(plate=plate_number)
    print(f"Available: {query}")
