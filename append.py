
def appends(n):
    l = []
    for i in range(n):
        l.append(i ** 2)

def list_comprehension(n):
    l = [i ** 2 for i in range(n)]

def main():
    n = 100000000
    # appends(n)
    list_comprehension(n)

if __name__ == "__main__":
    main()