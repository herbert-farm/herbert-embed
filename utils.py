

def flatten(l):
    for subl in l:
        for i in subl:
            yield i
