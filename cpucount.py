import os

def main():
    n_cores = os.cpu_count()
    print(f'Number of Logical CPU cores: {n_cores}')


if __name__ == "__main__":
    main()
