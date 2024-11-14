from sam_utilities import validate_list_input
from typing import Tuple, Dict, List
import json

def process_list(thing):
    if isinstance(thing, list):  # Check if the thing is a list
        if len(thing) >= 2:  # Ensure the list has at least two elements
            return tuple(thing[:2])  # Extract the first two elements and create a tuple
        else:
            return "List has fewer than two elements"
    else:
        return "The thing is not a list"


class Person():
    def __init__(self, obj: str, name: str, age: int, job: str, salery: float, work_hours: Tuple[int, int] | List[int], company: str):
        self.obj = obj
        self.name = name
        self.age = age
        self.job = job
        self.salery = float(salery)
        if not isinstance(work_hours, tuple):
            work_hours = process_list(work_hours)
            if isinstance(work_hours, str):
                work_hours = (0, 0)
        self.work_hours = work_hours
        self.company = company
    
    def getName(self):
        return self.name
    
    def printMe(self):
        print(f"Type: {self.obj}\nName: {self.name}\nAge: {self.age}\nJob: {self.job}\nSalery: {self.salery}\nWork Hours: {self.work_hours[0]} - {self.work_hours[1]}\nCompany: {self.company}")
    
    @staticmethod
    def loadFromString(string: str):
        data = json.loads(string.strip())

        sub_classes = {}
        for clazz in Person.__subclasses__():
            sub_classes[clazz.__name__] = clazz

        constructor = Person
        if data["obj"] in sub_classes.keys():
            constructor = sub_classes[data["obj"]]

        return constructor(**data)

    def __str__(self):
        return json.dumps(self)

class Worker(Person):
    def __init__(self, obj, name, age, job, salery, work_hours, company, manager: str):
        super().__init__(obj, name, age, job, salery, work_hours, company)
        self.manager = manager

    def printMe(self):
        print(f"Type: {self.obj}\nName: {self.name}\nAge: {self.age}\nJob: {self.job}\nSalery: {self.salery}\nWork Hours: {self.work_hours[0]} - {self.work_hours[1]}\nCompany: {self.company}\nManager: {self.manager}")

class Manager(Person):
    def __init__(self, obj, name, age, job, salery, work_hours, company, number_managed: int):
        super().__init__(obj, name, age, job, salery, work_hours, company)
        self.number_managed = number_managed

    def printMe(self):
        print(f"Type: {self.obj}\nName: {self.name}\nAge: {self.age}\nJob: {self.job}\nSalery: {self.salery}\nWork Hours: {self.work_hours[0]} - {self.work_hours[1]}\nCompany: {self.company}\nManages: {self.number_managed}")

people: Dict[str, Person] = {}

with open("people.jsonl") as file:
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