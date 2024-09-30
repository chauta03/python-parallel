import threading
import multiprocessing

def countdown():
    x = 100000000
    while x > 0:
        x -= 1

def implementation_1():
    thread_1 = threading.Thread(target=countdown)
    thread_2 = threading.Thread(target=countdown)

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()


def implementation_2():
    countdown()
    countdown()

def implementation_3():
    process_1 = multiprocessing.Process(target=countdown)
    process_2 = multiprocessing.Process(target=countdown)

    process_1.start()
    process_2.start()

    process_1.join()
    process_2.join()

def main():
    implementation_1()

if __name__ == "__main__":
    main()
