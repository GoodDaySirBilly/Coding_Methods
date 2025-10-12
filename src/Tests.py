from GaluaField import GaluaField as gf
from GaluaElement import GaluaElement as el
import numpy as np

def run_all_tests():
    gf1 = gf(3, 2, np.array([2, 2, 1]))
    check_field(gf1)

    gf2 = gf(2, 4, np.array([1, 1, 0, 0, 1]))
    check_field(gf2)

    check_add_sub()

    check_multiply()

    check_division()

    check_unique()


def check_add_sub():
    gf1 = gf(3, 2, np.array([2, 2, 1]))

    el1 = el(gf1, np.array([1, 2]))
    
    el2 = el(gf1, np.array([2, 1]))

    assert np.all((el1+el2).value == 0)

    print("Checks passed for add")

    assert np.all((el1-el2).value == np.array([2, 1]))

    print("Checks passed for sub")

def check_field(field: gf):

    # shape
    assert field.values.shape == (field.pow, field.orp)

    # zero and one
    assert np.all(field.values[0] == 0)

    one = np.zeros(field.orp, dtype=np.int64)
    one[0] = 1
    assert np.array_equal(field.values[1], one)

    # uniqueness of all nonzero elements
    uniq_nonzero = np.unique(field.values[1:], axis=0)
    assert uniq_nonzero.shape[0] == field.pow - 1, "Nonzero elements must be unique; check irreducible/primitive polynomial."
    print(f"Checks passed for {field}")


def check_multiply():
    gf1 = gf(3, 2, np.array([2, 2, 1]))
    
    el1 = el(gf1, gf1.values[1])

    for i in range(1, gf1.pow):

        el2 = el(gf1, gf1.values[i])
        assert (el1 * el2) == el2

    i, j = 3, 7

    el1 = el(gf1, gf1.values[i])
    el2 = el(gf1, gf1.values[j])

    z = 1 if i + j > 9 else 0

    assert np.all((el1*el2).value == gf1.values[(i + j - 1) % 9 + z])
    print("Checks passed for multiply")


def check_division():
    gf1 = gf(3, 2, np.array([2, 2, 1]))

    for k in range(1, gf1.pow):

        i, j = k, k

        el1 = el(gf1, gf1.values[i])
        el2 = el(gf1, gf1.values[j])

        res = el1 // el2

        b = np.array([1, 0])
        assert np.all(res.value == b)

    print("Checks passed for division")


def check_unique():
    gf1 = gf(3, 2, np.array([2, 2, 1]))
    gf2 = gf(11, 3, np.array([4, 1, 0, 1]))

    un1 = np.unique(gf1.values, axis = 0)
    un2 = np.unique(gf2.values, axis = 0)

    print(f"\nNumber of unique elements in {str(gf1)} : {len(un1)}")
    print(f"Number of all elements in {str(gf1)} : {len(gf1.values)}\n")
    print(f"Number of unique elements in {str(gf2)} : {len(un2)}")
    print(f"Number of all elements in {str(gf2)} : {len(gf2.values)}")
    