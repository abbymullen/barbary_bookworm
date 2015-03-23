from text_cleaning_BW import *


test_set = open("all_intros.txt")

for line in test_set:
    tester = Regexdate(line)
    print tester.find_daty_string(tester.string)

