from scales import eff_calc

import pprint

#-------------------------------------------------
def test_simple():
    obj         = eff_calc(proc=None, year=None, trig=['ETOS'])
    obj.out_dir = 'tests/effcalc/simple'
    d_eff       = obj.get_efficiencies()

    pprint.pprint(d_eff, indent=4)
#-------------------------------------------------
def main():
    test_simple()
#-------------------------------------------------
if __name__ == '__main__':
    main()

