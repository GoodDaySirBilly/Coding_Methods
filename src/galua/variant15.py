from GaluaField import GaluaField as gf
from GaluaElement import GaluaElement as el
import numpy as np

# Creating Galua Field GF(2^6)
gf1 = gf(2, 6, np.array([1, 1, 0, 0, 0, 0, 1]))

gf2 = gf(11, 3, np.array([4, 1, 0, 1]))

print("-------------------------------")
#print(gf1)

# Creating elements of field
el1 = el(gf1, np.array([1, 0, 0, 0, 1, 1]))
el2 = el(gf1, np.array([1, 0, 0, 1, 0, 1]))

one = el(gf1, np.array([1, 0, 0, 0, 0, 0]))
zero = el(gf1, np.array([0, 0, 0, 0, 0, 0]))

print("Element 1")
print(el1)
print("Element 2")
print(el2)

print("Sum of elements")
print(el1 + el2)

print("Sub of elements")
print(el1 - el2)

print("Mul of elements")
print(el1 * el2)

print("Div of elements")
print(el1 // el2)

print("Multiplying by one")
print(el1 * one)

print("Division by one")
print(el1 // one)

print("Multiplying by zero")
print(el1 * zero)

print("-------------------------------")
# print(gf2)

el1 = el(gf2, np.array([1, 4, 0]))
el2 = el(gf2, np.array([0, 1, 0]))

one = el(gf2, np.array([1, 0, 0]))
zero = el(gf2, np.array([0, 0, 0]))

print("Element 1")
print(el1)
print("Element 2")
print(el2)

print("Sum of elements")
print(el1 + el2)

print("Sub of elements")
print(el1 - el2)

print("Mul of elements")
print(el1 * el2)

print("Div of elements")
print(el1 // el2)

print("Multiplying by one")
print(el1 * one)

print("Division by one")
print(el1 // one)

print("Multiplying by zero")
print(el1 * zero)