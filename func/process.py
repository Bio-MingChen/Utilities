from multiprocessing import Process,Pool

def synchronize_multiple_processes(assignments):
    """
    assignments is a list of tuples which are
    composed by a function and its arguments(in tuple format)
    this function is synchronized by .join() method
    of Process 
    """
    for func,args,kwargs in assignments:
        p = Process(target=func,args=args,kwargs=kwargs)
        print('subprocess for %s is running...' % func)
        p.start()

    p.join() #block the main process to synchronize the subprocesses
    print('All assignments are completed!')

def multiple_processes_pool(assignments,number_of_process):
    """
    run multiple processes by specifying number of processes
    each time
    """
    p = Pool(number_of_process)
    for func,args,kwargs in assignments:
        p.apply_async(func,args=args,kwds=kwargs)

    p.close() # no other procee will be added into pool
    p.join() # synchronization
    print('All assignments are completed!')
