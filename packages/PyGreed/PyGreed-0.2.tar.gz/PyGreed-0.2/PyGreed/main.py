import os
import threading
import time

# Add the current directory to the PATH to locate DLLs and the .pyd file
current_dir = os.path.dirname(os.path.abspath(__file__))

os.environ['PATH'] += os.pathsep + current_dir

os.chdir(current_dir)
current_directory = os.getcwd()

try:
    import PyGreed.Greed as Greed
except ImportError as e:
    print("Error importing Greed module: ", e)
    print(current_directory)
    raise

def release_gil():
    while True:
        time.sleep(1)
        pass

gil_release_thread = threading.Thread(target=release_gil)
gil_release_thread.daemon = True
gil_release_thread.start()

def user_algorithm(ob):
    raise NotImplementedError("User must define this function")

def set_user_algorithm(algo):
    global user_algorithm
    user_algorithm = algo

def start_game():
    pl1 = Greed.coords(10, 10, 0)
    print(pl1.r, ' ', pl1.c)

    thread = threading.Thread(target=Greed.start)
    thread.start()


    print(type(Greed.my_id))

    ship_pointer = Greed.getPointer()

    thread1 = threading.Thread(target=user_algorithm, args=(ship_pointer,))
    thread1.start()

    thread.join()
    thread1.join()
