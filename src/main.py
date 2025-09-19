from GaluaField import GaluaField as gf
from GaluaElement import GaluaElement as el
import numpy as np


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
    



if __name__ == '__main__':
    main()