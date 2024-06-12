
import sys
from multiprocessing import Process, Queue
from queue import Empty
import threading
import time
import os
from .recosu.sampling.sampling import run_sampler
from .recosu.pso import global_best

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def run_process(stdout_queue, stderr_queue, results_queue, data, folder):
    steps = data['steps']
    args = data['arguments']
    calib = data['calibration_parameters']
    
    my_mode = args["mode"]

    # If "mode" in args remove it
    if "mode" in args:
        del args["mode"]
    
    calibration_map = {}
    for param in calib:
        param_name = param['name']
        param_value = param['value']
        calibration_map[param_name] = param_value
        
    if not os.path.exists(folder):
        os.makedirs(folder)

    if (os.path.exists(os.path.join(folder, 'output.txt'))):
        os.remove(os.path.join(folder, 'output.txt'))
        
    if (os.path.exists(os.path.join(folder, 'error.txt'))):
        os.remove(os.path.join(folder, 'error.txt'))
    
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    read_stdout, write_stdout = os.pipe()
    read_stderr, write_stderr = os.pipe()
    
    sys.stdout = os.fdopen(write_stdout, 'w')
    sys.stderr = os.fdopen(write_stderr, 'w')
    
    stdout_thread = threading.Thread(target=enqueue_output, args=(os.fdopen(read_stdout, 'r'), stdout_queue))
    stderr_thread = threading.Thread(target=enqueue_output, args=(os.fdopen(read_stderr, 'r'), stderr_queue))
    stdout_thread.daemon = True
    stderr_thread.daemon = True
    stdout_thread.start()
    stderr_thread.start()
    
    try:
        
        options = {}
        oh_strategy = {}
        
        for key in calibration_map.keys():
            if "options_" in key:
                options[key.replace("options_", "")] = float(calibration_map[key])
            if "strategy_" in key:
                oh_strategy[key.replace("strategy_", "")] = calibration_map[key]

        config = {}

        if my_mode == "Sampling: Halton" or my_mode == "Sampling: Random":
            config = {
                'service_timeout': int(calibration_map['service_timeout']),
                'http_retry': int(calibration_map['http_retry']),
                'allow_redirects': True if calibration_map['allow_redirects'] == "True" else False,
                'async_call': True if calibration_map['async_call'] == "True" else False,
                'conn_timeout': int(calibration_map['conn_timeout']),
                'read_timeout': int(calibration_map['read_timeout']),
                'step_trace': os.path.join(folder, 'pso_step_trace.json')
            }
        else:
            config = {
                'service_timeout': int(calibration_map['service_timeout']),
                'http_retry': int(calibration_map['http_retry']),
                'http_allow_redirects': True if calibration_map['allow_redirects'] == "True" else False,
                'async_call': True if calibration_map['async_call'] == "True" else False,
                'http_conn_timeout': int(calibration_map['conn_timeout']),
                'http_read_timeout': int(calibration_map['read_timeout']),
                'particles_fail': int(calibration_map['particles_fail']),
                'step_trace': os.path.join(folder, 'pso_step_trace.json')
            }

        print("\n")
        print(steps)
        print("\n")
        print(args)
        print("\n")
        print(calibration_map)
        print("\n")
        print(options)
        print("\n")
        print(oh_strategy)
        print("\n")
        print(config)
        print("\n", flush=True)

        if my_mode == "Sampling: Halton":
            print("Running Halton Sampling..\n", flush=True)
            trace = run_sampler(steps, 
                                args, 
                                int(calibration_map['count']), 
                                int(calibration_map['num_threads']), 
                                "halton", 
                                conf=config, 
                                trace_file=os.path.join(folder, 'halton_trace.txt'),
                                offset=int(calibration_map['offset']))
            results_queue.put(trace)
            print(trace, flush=True)
            
        elif my_mode == "Sampling: Random":
            print("Running Random Sampling...\n", flush=True)
            trace = run_sampler(steps, 
                    args, 
                    int(calibration_map['count']), 
                    int(calibration_map['num_threads']), 
                    "random", 
                    conf=config, 
                    trace_file=os.path.join(folder, 'random_trace.txt'))
            results_queue.put(trace)
            print(trace, flush=True)
        else:
            print("Running MG-PSO Optimization...\n", flush=True)
            optimizer, trace = global_best(steps,   
                    rounds=(int(calibration_map['min_rounds']), int(calibration_map['max_rounds'])),              
                    args=args,      
                    n_particles=int(calibration_map['n_particles']),      
                    iters=int(calibration_map['iters']),  
                    n_threads=int(calibration_map['n_threads']),      
                    options=options,
                    oh_strategy=oh_strategy, 
                    conf=config
                )
            
            results_queue.put(trace)
            print(trace, flush=True)
        
        print("Finishing up...", flush=True)
        time.sleep(5)
    except Exception as e:
        print("An exception occurred: ", flush=True)
        print(str(e))
        # Print stack trace
        import traceback
        traceback.print_exc()

        # Write all of this information to a crash file
        with open(os.path.join(folder, 'crash.txt'), 'w') as f:
            f.write(str(e))
            f.write("\n")
            traceback.print_exc(file=f)
    finally:
        stdout_thread.join()
        stderr_thread.join()
        
        sys.stdout = old_stdout
        sys.stderr = old_stderr