# Exercise Thirteen

'exercise_therteen' is a library with the most simple operations: addition, subtraction, multiplication, and division; looking for easy and efficient usage and learning of these operations.

## Simple operations:

### 1. Method addition(integer value_one, integer value_two)
Returns the sum of the values value_one and value_two

### 2. Method subtraction(integer value_one, integer value_two)
Returns the subtraction of the values value_one and value_two

### 3. Method multiplication(integer value_one, integer value_two)
Returns the multiplication of the values value_one and value_two

### 4. Method division(integer value_one, integer value_two)
Returns the division of the values value_one and value_two
Raise 'ZeroDivisionError' exception with a message if value_two is zero

## Installation with pip:
`pip install exercise_thirteen`

## Quickstart:
After installation, run the following code from anywhere:
````
from functions.exercise_thirteen import addition, subtraction, multiplication, division

# returns 8
result_addition = addition(3, 5)

# returns -2
result_subtraction = subtraction(3, 5)

# returns 15
result_multiplication = multiplication(3, 5)

# returns 5
result_division = division(10, 2)

# show 8 in console
print(result_addition)

# show -2 in console
print(result_subtraction)

# show 15 in console
print(result_multiplication)

# show 5 in console
print(result_division)
````

## Run tests:
requires the installation of the 'pytest' library before running the tests. Then, having the terminal located in the project folder, run the following command:
`pytest`