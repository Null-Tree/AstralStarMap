



dict={-2: 2000, 
      -1: 800, 
      0: 400, 
      1: 200, 
      2: 120, 
      3: 80, 
      4: 20, 
      5: 8,
        6: 4, 7: 2, 8: 1}

for key in dict:
    dict[key]=int(dict[key] * (1/.025))




print(dict)