

def decorator(stop):
        print("hello" + stop)

        def act_dec(func):

            def wrapper(*args, **kwargs):
                func(*args, **kwargs)
                print(stop)
            return wrapper
        return act_dec

        

@decorator("wodkodk")
def funct(go):
    print("world" + go)


def main():

    
   

    funct("wodkw")


if __name__ == '__main__':
    main()