from GaluaField import GaluaField as gf
from GaluaElement import GaluaElement as el
import numpy as np


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

def main():
    
    gf1 = gf(2, 6, np.array([1, 1, 0, 0, 0, 0, 1]))

    gf2 = gf(3, 2, np.array([2, 2, 1]))

    print(gf1)
    print(gf2)


    print(gf1 == gf1)
    print(gf1 == gf2)

    print(gf2 != gf2)
    print(gf2 != gf1)

    print(gf2.values)

    check_field(gf1)
    check_field(gf2)
    



if __name__ == '__main__':
    main()