import time

class cm_timer_1:
    def __enter__(self):
        self.start_time = time.time() 
        return self

    def __exit__(self, *_):
        print(f'time: {time.time() - self.start_time}') 


from contextlib import contextmanager

@contextmanager
def cm_timer_2():
    start_time = time.time() 
    try:
        yield
    finally:
        print(f'time: {time.time() - start_time}')  

