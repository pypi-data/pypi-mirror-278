def add(*args):
    x=0
    for arg in args:
        x=x+arg
    return x
if __name__=="__main__":
    xx=add(1,2,3)
    print(xx)
