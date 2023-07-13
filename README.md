# AirBnB clone - The console

This is the first step towards building a full web application: Writing a command interpreter to manage the AirBnB objects.

## The HBNB console

Manages the objects of our project:

- Create a new object (ex. a new User or a new Place)
- Retrieve an object from a file, a database etc...
- Do operations on objects (count, compute stats, etc...)
- Update attributes of an object
- Destroy an object

## Commands and how to use it

The command interpreter allows us to handle our data requirements with the following commands:

| Command | Function                                          |
| ------- | ------------------------------------------------- |
| create  | create a new instance of a class                  |
| show    | show the info of an instance of a class           |
| destroy | destroy an instance of a class                    |
| update  | update the info of the objects in an instance     |
| all     | prints all string representation of all instances |
| quit    | exit the console                                  |
| help    | show help of the commands                         |

## Objects

The objects that can be passed to the HBNB console:

| Object  | Function                         |
| ------- | -------------------------------- |
| city    | city of the reservation          |
| state   | country state of the reservation |
| place   | name of the place of reservation |
| user    | name of the user who reserves    |
| amenity | benefits of the place            |
| review  | review of the room and guest     |

### Using the console

To start the console in interactive mode run:

```
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb)
(hbnb)
(hbnb) quit
$
```

You can also do it in non-interactive mode:

```
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
$
```

### Examples:

#### Standard commands:

```
(hbnb)create User
993e570d-9b4e-449c-84b3-085ab454d3ce
(hbnb)
```

Will create a new User

```
(hbnb)create BaseModel
d711be23-73d9-4fbd-92f5-fe9ec7044d6d
(hbnb)show BaseModel d711be23-73d9-4fbd-92f5-fe9ec7044d6d
[BaseModel] (d711be23-73d9-4fbd-92f5-fe9ec7044d6d) {'id': 'd711be23-73d9-4fbd-92f5-fe9ec7044d6d', 'created_at': '2019-07-04T02:20:53.149558', 'updated_at': '2019-07-04T02:20:53.149791'}
(hbnb)
```

Will create a new BaseModel and show the objects of the instance

```
(hbnb)destroy BaseModel d711be23-73d9-4fbd-92f5-fe9ec7044d6d
['BaseModel', 'd711be23-73d9-4fbd-92f5-fe9ec7044d6d']
(hbnb)
```

Will destroy the BaseModel instance

## Authors

- [Karanja J. Njuguna](https://github.com/kei-en)
- [Faith Mwangi](https://github.com/Kezieh5)
