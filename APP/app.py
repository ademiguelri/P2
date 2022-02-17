import client

def main():
    print('Insert cuantity of thermostats: ')
    try:
        count = input()
    except TypeError as te:
        print(te)
        print('Invalid cuantity')
    except:
        print('Error')
    client.start_client(count)
    

if __name__ == "__main__":
   main()