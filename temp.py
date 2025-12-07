import math
def bounded_shift(val,delta,interval):
    """general shift, note start and end of interval are same, will go to int min"""
    vmin,vmax=interval
    vsum=val+delta
    interval_range=(vmax-vmin) 
    if vsum>vmax:
        d=vsum-vmax
        n=math.ceil(d/interval_range)
        vsum-=n*(vmax-vmin) 
    
    if vsum<vmin:
        d=vmin-vsum
        n=math.ceil(d/interval_range)
        vsum+=n*(vmax-vmin) 
    return vsum

# for i in range(-100,100):
#     i/=10
#     print(bounded_shift(0,i,(0,24)))

def input_until_valid(prompt,acceptable,errmsg=None):
    print(prompt,end="")
    vin=input()
    if vin in acceptable:
        return vin
    else:
        if errmsg:
            print(errmsg)
        return input_until_valid(prompt,acceptable,errmsg)
    
print(input_until_valid("test",['a','b']))