from sam_utilities import validate_list_input
from typing import Tuple, Dict

class Person():
    def __init__(self, name: str, age: int, job: str, salery: float, work_hours: Tuple[int, int], company: str):
        self._name = name
        self._age = age
        self._job = job
        self._salery = float(salery)
        self._work_hours = work_hours
        self._company = company
    
    def getName(self):
        return self._name
    
    def printMe(self):
        print(f"Name: {self._name}\nAge: {self._age}\nJob: {self._job}\nSalery: {self._salery}\nWork Hours: {self._work_hours}\nCompany: {self._company}")
    
    @staticmethod
    def loadFromString(string: str):
        data = string.strip().split(",")
        work_hours = data[4].split(":")
        work_hours[0] = int(work_hours[0])
        work_hours[1] = int(work_hours[1])
        return Person(
            data[0],
            int(data[1]),
            data[2],
            float(data[3]),
            tuple(work_hours),
            data[5]
        )

    def __str__(self):
        return f"{self._name},{self._age},{self._job},{self._salery},{self._work_hours[0]}:{self._work_hours[1]},{self._company}"

people: Dict[str, Person] = {}

with open("people.csv") as file:
    lines = file.readlines()
    for line in lines:
        person = Person.loadFromString(line)
        people[person.getName()] = person

names = []
for name in people.keys():
    names.append(name)
names.append("0")

running = True
while running:
    for name in people.keys():
        print(f": {name}")
    name = validate_list_input(names, "Please choose a person. (Or enter 0 to stop.) ")
    if name == "0":
        running = False
        break
    people.get(name).printMe()