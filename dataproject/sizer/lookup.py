



dict={
    -2: 50,
    -1: 20,
    0: 10,
    1: 5,
    2: 3,
    3: 2,
    4: .5,
    5: .2,
    6: .1,
    7: .05,
    8: .025
}

for key in dict:
    dict[key]=int(dict[key] * (1/.025))




print(dict)