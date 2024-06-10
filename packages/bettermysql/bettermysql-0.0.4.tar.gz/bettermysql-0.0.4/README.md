# **About**

A simple and lightweight ORM that facilitate some operations on MySQL using of pymysql.

# How to use

## **Preparation**

```python
# Single call it once to setup the inner settings
BetterMYSQL.setup("name of the database", "db user", "db password", "host", 1234) #port

# Creating a DB Model
class Fruits():
  _table = "fruit_table_name"

class People():
  _table = "people_table_name"
```

## **Select**

```python
# Select the first fruit ordered by name and retrieve the first row
Fruits().select("name").order("name").row()  # returns one row

# Select all data from the top 15 fruits
Fruits().select("*").limit("15").run() # returns a row list

# Select all data from the top 15 fruits
Fruits().select("*").limit("15").run() # returns a row list

# Select the name of the first person with 34 years old
People().select("name").where("age = ?").cell(34) # returns the first cell of the first row
```

## **Insert**

```python
# Inserting a person given its name and age
People().insert("name, age").run(["Matt", 34])
```

## **Update**

```python
# Updating all ages to 16 where the name is Matt
People().update("age = ?").where("name = ?").run([16, "Matt"])
```

## **Delete**

```python
# Delete all persons
People().delete()
```
