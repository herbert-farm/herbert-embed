
import threading
import time

class Database(object):
    
    def save_activity(self, data):
        print("Got: {time:1f}  {id:8}  {name:15}  {data}".format(**data, time=time.time()))
        
    # Create a new thread to consume data in queue
    def wait_queue(self, q):
        while True:
            
            if not q.empty():
                
                # get reading
                data = q.get()
                
                print(data)
                
                # save to db
                self.save_activity(data)
                
                # mark as processed
                q.task_done()
    
    def listen(self, q):
        
        self.thread = threading.Thread(target=self.wait_queue, kwargs={ 'q' : q })
        self.thread.start()


# COOL NOTE: all other consumers of the data queue have to follow this pattern for now. task_done has to be called by last item.
