import numpy
import random
import GenerateData as generate
import Plot as plot
import time

### generate data ###
h_inter_arrival = generate.generate(20)
l_inter_arrival = generate.generate(30)
service_time_1 = generate.generate(30)
service_time_2 = generate.generate(30)

if_serve_first = [] # a list of float betwween 0-1 used to decide whether serving first or not
h_arrival = [] # arrival time for high priority packets
l_arrival = []  # arrival time for low priority packets
departure_time_1 = [0]*2*generate.DataNum # departure time of server 1
departure_time_2 = [0]*2*generate.DataNum # departure time of server 2
h_waiting_time = l_waiting_time = 0
h_waiting_time_sys = l_waiting_time_sys = 0

### list use to save result for figure 1 ###
all_hp_waiting_time = []
all_lp_waiting_time = []
all_hp_waiting_time_sys = []
all_lp_waiting_time_sys = []
numerical_hp_wt_system = []
numerical_lp_wt_system = []
numerical_hp_wt_queue = []
numerical_lp_wt_queue = []
### list use to save result for figure 2 ###
serve_hp_time_1 = serve_lp_time_1 = idle_1 = 0
serve_hp_time_2 = serve_lp_time_2 = idle_2 = 0
all_serve_hp_time_1 = [] # save result of different probabilities
all_serve_lp_time_1 = [] # save result of different probabilities
all_idle_time_1 = [] # total - serve_hp_time - seve_hp_time
all_serve_hp_time_2 = [] # save result of different probabilities
all_serve_lp_time_2 = [] # save result of different probabilities
all_idle_time_2 = [] # total - serve_hp_time - seve_hp_time

# calculate arrival time using inter arrival time
for i in range(generate.DataNum):
    h_arrival.append(sum(h_inter_arrival[0:i+1]))
    l_arrival.append(sum(l_inter_arrival[0:i+1]))
    if_serve_first.append(random.random())

def Simulation(probability):
    """Simulate the priority queue with 2 output link

    Args:
        probability (float): The probability of serving the high priority packet first.

    Returns:
       None, but save the result into a list.

    Raises:
       AttributeError, KeyError
    """
    global h_waiting_time , l_waiting_time, h_waiting_time_sys, l_waiting_time_sys, serve_hp_time_1, serve_lp_time_1, serve_hp_time_2, serve_lp_time_2
    h_waiting_time = l_waiting_time = h_waiting_time_sys = l_waiting_time_sys = 0
    serve_hp_time_1 = serve_lp_time_1 = serve_hp_time_2 = serve_lp_time_2 = 0
    l_count = h_count = 0
    dep_ptr_1 = dep_ptr_2 = 0 # point at the last none zero departure time
    # will see total DataNum*2 packets
    for i in range(generate.DataNum*2):
        # first packet
        if (i == 0):
            if l_arrival < h_arrival:
                if(random.random() < 0.5):
                    # go to server 1
                   departure_time_1[i] = l_arrival[l_count] + service_time_1[i]
                   l_waiting_time_sys = l_waiting_time_sys + service_time_1[i]
                   l_count = l_count + 1
                   dep_ptr_1 = i
                else:
                   departure_time_2[i] = l_arrival[l_count] + service_time_2[i]
                   l_waiting_time_sys = l_waiting_time_sys + service_time_2[i]
                   l_count = l_count + 1
                   dep_ptr_2 = i
            else:
                if(random.random() < 0.5):
                   departure_time_1[i] = h_arrival[l_count] + service_time_1[i]
                   h_waiting_time_sys = h_waiting_time_sys + service_time_1[i]
                   h_count = h_count + 1
                   dep_ptr_1 = i
                else:
                   departure_time_2[i] = h_arrival[l_count] + service_time_2[i]
                   h_waiting_time_sys = h_waiting_time_sys + service_time_2[i]                   
                   h_count = h_count + 1
                   dep_ptr_2 = i    
        else:
            if((h_count != generate.DataNum) & (l_count != generate.DataNum)):
                who = h_arrival[h_count] - l_arrival[l_count] # which priority comes next

                # high priority comes next
                if(who < 0): 
                    # server 1 and server 2 are both idle
                    if((departure_time_1[dep_ptr_1] - h_arrival[h_count] < 0) & (departure_time_2[dep_ptr_2] - h_arrival[h_count] < 0)):
                        if(random.random() < 0.5):
                            # goes to server 1
                            departure_time_1[i] = h_arrival[h_count] + service_time_1[h_count]
                            h_waiting_time_sys = h_waiting_time_sys + service_time_1[h_count]
                            serve_hp_time_1 = serve_hp_time_1 + service_time_1[h_count]
                            h_count = h_count + 1
                            dep_ptr_1 = i
                            
                        else:
                            departure_time_2[i] = h_arrival[h_count] + service_time_2[h_count]
                            h_waiting_time_sys = h_waiting_time_sys + service_time_2[h_count]
                            serve_hp_time_2 = serve_hp_time_2 + service_time_2[h_count]
                            h_count = h_count + 1
                            dep_ptr_2 = i 

                    # server 1 busy server 2 idle
                    elif((departure_time_1[dep_ptr_1] - h_arrival[h_count] > 0) & (departure_time_2[dep_ptr_2] - h_arrival[h_count] < 0)):
                        departure_time_2[i] = h_arrival[h_count] + service_time_2[h_count]
                        h_waiting_time_sys = h_waiting_time_sys + service_time_2[h_count]
                        serve_hp_time_2 = serve_hp_time_2 + service_time_2[h_count]
                        h_count = h_count + 1
                        dep_ptr_2 = i

                    # server 2 busy server 1 idle                     
                    elif((departure_time_1[dep_ptr_1] - h_arrival[h_count] < 0) & (departure_time_2[dep_ptr_2] - h_arrival[h_count] > 0)):                
                        departure_time_1[i] = h_arrival[h_count] + service_time_1[h_count]
                        h_waiting_time_sys = h_waiting_time_sys + service_time_1[h_count]
                        serve_hp_time_1 = serve_hp_time_1 + service_time_1[h_count]
                        h_count = h_count + 1
                        dep_ptr_1 = i
                    
                    else:
                        # server 1 idle first
                        if( (departure_time_1[dep_ptr_1] - h_arrival[h_count]) < (departure_time_2[dep_ptr_2] - h_arrival[h_count])):
                            departure_time_1[i] = h_arrival[h_count] + service_time_1[h_count] + departure_time_1[dep_ptr_1] - h_arrival[h_count]
                            h_waiting_time = h_waiting_time + departure_time_1[dep_ptr_1] - h_arrival[h_count] # accumulate the waiting time                              
                            h_waiting_time_sys = h_waiting_time_sys + service_time_1[h_count] + (departure_time_1[dep_ptr_1] - h_arrival[h_count])
                            serve_hp_time_1 = serve_hp_time_1 + service_time_1[h_count]
                            h_count = h_count + 1
                            dep_ptr_1 = i

                        else:
                            departure_time_2[i] = h_arrival[h_count] + service_time_2[h_count] + departure_time_2[dep_ptr_2] - h_arrival[h_count]
                            h_waiting_time = h_waiting_time + departure_time_2[dep_ptr_2] - h_arrival[h_count] # accumulate the waiting time                              
                            h_waiting_time_sys = h_waiting_time_sys + service_time_2[h_count] + (departure_time_2[dep_ptr_2] - h_arrival[h_count])
                            serve_hp_time_2 = serve_hp_time_2 + service_time_2[h_count]                                  
                            h_count = h_count + 1
                            dep_ptr_2 = i                         

                # low priority comes next
                else:
                    # print("2-2: ",h_arrival[h_count] - departure_time_1[dep_ptr_1],h_arrival[h_count] - departure_time_2[dep_ptr_2])
                    if((departure_time_1[dep_ptr_1] - l_arrival[l_count] < 0) & (departure_time_2[dep_ptr_2] - l_arrival[l_count] < 0)):
                        if(random.random() < 0.5):
                            # goes to server 1
                            departure_time_1[i] = l_arrival[l_count] + service_time_1[l_count]
                            l_waiting_time_sys = l_waiting_time_sys + service_time_1[l_count]
                            serve_lp_time_1 = serve_lp_time_1 + service_time_1[l_count]
                            l_count = l_count + 1
                            dep_ptr_1 = i
                        else:
                            departure_time_2[i] = l_arrival[l_count] + service_time_2[l_count]
                            l_waiting_time_sys = l_waiting_time_sys + service_time_2[l_count]
                            serve_lp_time_2 = serve_lp_time_2 + service_time_2[l_count]
                            l_count = l_count + 1
                            dep_ptr_2 = i 
                    # server 1 busy server 2 idle
                    elif((departure_time_1[dep_ptr_1] - l_arrival[h_count] > 0) & (departure_time_2[dep_ptr_2] - l_arrival[h_count] < 0)):
                        departure_time_2[i] = l_arrival[l_count] + service_time_2[l_count]
                        l_waiting_time_sys = l_waiting_time_sys + service_time_2[l_count]
                        serve_lp_time_2 = serve_lp_time_2 + service_time_2[l_count]
                        l_count = l_count + 1
                        dep_ptr_2 = i
                    # server 2 busy server 1 idle                     
                    elif((departure_time_1[dep_ptr_1] - l_arrival[h_count] < 0) & (departure_time_2[dep_ptr_2] - l_arrival[h_count] > 0)):                
                        departure_time_1[i] = l_arrival[l_count] + service_time_1[l_count]
                        l_waiting_time_sys = l_waiting_time_sys + service_time_1[l_count]
                        serve_lp_time_1 = serve_lp_time_1 + service_time_1[l_count]
                        l_count = l_count + 1
                        dep_ptr_1 = i   
                    else:
                        # see whether high priority comes before one server become idle  
                        if((h_arrival[h_count]<departure_time_1[dep_ptr_1]) & (h_arrival[h_count]<departure_time_2[dep_ptr_2]) & (if_serve_first[h_count]<=probability)):
                            # high priority serves first
                            # server 1 idle first
                            if((departure_time_1[dep_ptr_1] - h_arrival[h_count]) < (departure_time_2[dep_ptr_2]-h_arrival[h_count])):
                                departure_time_1[i] = h_arrival[h_count] + service_time_1[h_count] + departure_time_1[dep_ptr_1] - h_arrival[h_count]
                                h_waiting_time = h_waiting_time + departure_time_1[dep_ptr_1] - h_arrival[h_count] # accumulate the waiting time                                
                                h_waiting_time_sys = h_waiting_time_sys + service_time_1[h_count] + (departure_time_1[dep_ptr_1] - h_arrival[h_count])
                                serve_hp_time_1 = serve_hp_time_1 + service_time_1[h_count]
                                h_count = h_count + 1
                                dep_ptr_1 = i
                            else:
                                departure_time_2[i] = h_arrival[h_count] + service_time_2[h_count] + departure_time_2[dep_ptr_2]-h_arrival[h_count]
                                h_waiting_time = h_waiting_time + departure_time_2[dep_ptr_2] - h_arrival[h_count] # accumulate the waiting time                              
                                h_waiting_time_sys = h_waiting_time_sys + service_time_2[h_count] + (departure_time_2[dep_ptr_2] - h_arrival[h_count])
                                serve_hp_time_2 = serve_hp_time_2 + service_time_2[h_count]   
                                h_count = h_count + 1
                                dep_ptr_2 = i  

                        else:
                            # server 1 idle first
                            if((departure_time_1[dep_ptr_1] - l_arrival[l_count]) < (departure_time_2[dep_ptr_2]-l_arrival[l_count])):
                                departure_time_1[i] = l_arrival[l_count] + service_time_1[l_count] + departure_time_1[dep_ptr_1] - l_arrival[l_count]
                                l_waiting_time = l_waiting_time + departure_time_1[dep_ptr_1] - l_arrival[l_count] # accumulate the waiting time                              
                                l_waiting_time_sys = l_waiting_time_sys + service_time_1[l_count] + (departure_time_1[dep_ptr_1] - l_arrival[l_count])
                                serve_lp_time_1 = serve_lp_time_1 + service_time_1[l_count]
                                l_count = l_count + 1
                                dep_ptr_1 = i
                            else:
                                departure_time_2[i] = l_arrival[l_count] + service_time_2[l_count] + departure_time_2[dep_ptr_2]-l_arrival[l_count]
                                l_waiting_time = l_waiting_time + departure_time_2[dep_ptr_2] - l_arrival[l_count] # accumulate the waiting time                              
                                l_waiting_time_sys = l_waiting_time_sys + service_time_2[l_count] + (departure_time_2[dep_ptr_2] - l_arrival[l_count])
                                serve_lp_time_2 = serve_lp_time_2 + service_time_2[l_count]
                                l_count = l_count + 1
                                dep_ptr_2 = i

            elif((l_count != generate.DataNum) & (h_count == generate.DataNum)):
                if((departure_time_1[dep_ptr_1] - l_arrival[l_count] < 0) & (departure_time_2[dep_ptr_2] - l_arrival[l_count] < 0)):
                    if(random.random() < 0.5):
                        # goes to server 1
                        departure_time_1[i] = l_arrival[l_count] + service_time_1[l_count]
                        l_waiting_time_sys = l_waiting_time_sys + service_time_1[l_count]
                        serve_lp_time_1 = serve_lp_time_1 + service_time_1[l_count]
                        l_count = l_count + 1
                        dep_ptr_1 = i
                    else:
                        departure_time_2[i] = l_arrival[l_count] + service_time_2[l_count]
                        l_waiting_time_sys = l_waiting_time_sys + service_time_2[l_count]
                        serve_lp_time_2 = serve_lp_time_2 + service_time_2[l_count]
                        l_count = l_count + 1
                        dep_ptr_2 = i 
                # server 1 busy server 2 idle
                elif((departure_time_1[dep_ptr_1] - l_arrival[l_count] > 0) & (departure_time_2[dep_ptr_2] - l_arrival[l_count] < 0)):
                    departure_time_2[i] = l_arrival[l_count] + service_time_2[l_count]
                    l_waiting_time_sys = l_waiting_time_sys + service_time_2[l_count]
                    serve_lp_time_2 = serve_lp_time_2 + service_time_2[l_count]
                    l_count = l_count + 1
                    dep_ptr_2 = i
                # server 2 busy server 1 idle                     
                elif((departure_time_1[dep_ptr_1] - l_arrival[l_count] < 0) & (departure_time_2[dep_ptr_2] - l_arrival[l_count] > 0)):                
                    departure_time_1[i] = l_arrival[l_count] + service_time_1[l_count]
                    l_waiting_time_sys = l_waiting_time_sys + service_time_1[l_count]
                    serve_lp_time_1 = serve_lp_time_1 + service_time_1[l_count]
                    l_count = l_count + 1
                    dep_ptr_1 = i  
                else:
                    # server 1 idle first
                    if((departure_time_1[dep_ptr_1] - l_arrival[l_count]) < (departure_time_2[dep_ptr_2]- l_arrival[l_count])):
                        departure_time_1[i] = l_arrival[l_count] + service_time_1[l_count] + departure_time_1[dep_ptr_1] - l_arrival[l_count]
                        l_waiting_time = l_waiting_time + departure_time_1[dep_ptr_1] - l_arrival[l_count] # accumulate the waiting time
                        l_waiting_time_sys = l_waiting_time_sys + service_time_1[l_count] + (departure_time_1[dep_ptr_1] - l_arrival[l_count])
                        serve_lp_time_1 = serve_lp_time_1 + service_time_1[l_count]
                        l_count = l_count + 1
                        dep_ptr_1 = i
                    else:
                        departure_time_2[i] = l_arrival[l_count] + service_time_2[l_count] + departure_time_2[dep_ptr_2]- l_arrival[l_count]
                        l_waiting_time = l_waiting_time + departure_time_2[dep_ptr_2] - l_arrival[l_count] # accumulate the waiting time
                        l_waiting_time_sys = l_waiting_time_sys + service_time_2[l_count] + (departure_time_2[dep_ptr_2] - l_arrival[l_count])
                        serve_lp_time_2 = serve_lp_time_2 + service_time_2[l_count]
                        l_count = l_count + 1
                        dep_ptr_2 = i                                                                      
            
            elif((l_count == generate.DataNum) & (h_count != generate.DataNum)):
                if((departure_time_1[dep_ptr_1] - h_arrival[h_count] < 0) & (departure_time_2[dep_ptr_2] - h_arrival[h_count] < 0)):
                    if(random.random() < 0.5):
                        # goes to server 1
                        departure_time_1[i] = h_arrival[h_count] + service_time_1[h_count]
                        h_waiting_time_sys = h_waiting_time_sys + service_time_1[h_count]
                        serve_hp_time_1 = serve_hp_time_1 + service_time_1[h_count]
                        h_count = h_count + 1
                        dep_ptr_1 = i
                    else:
                        departure_time_2[i] = h_arrival[h_count] + service_time_2[h_count]
                        h_waiting_time_sys = h_waiting_time_sys + service_time_2[h_count]
                        serve_hp_time_2 = serve_hp_time_2 + service_time_2[h_count]
                        h_count = h_count + 1
                        dep_ptr_2 = i 
                # server 1 busy server 2 idle
                elif((departure_time_1[dep_ptr_1] - h_arrival[h_count] > 0) & (departure_time_2[dep_ptr_2] - h_arrival[h_count] < 0)):
                    departure_time_2[i] = h_arrival[h_count] + service_time_2[h_count]
                    h_waiting_time_sys = h_waiting_time_sys + service_time_2[h_count]
                    serve_hp_time_2 = serve_hp_time_2 + service_time_2[h_count]
                    h_count = h_count + 1
                    dep_ptr_2 = i
                # server 2 busy server 1 idle                     
                elif((departure_time_1[dep_ptr_1] - h_arrival[h_count] < 0) & (departure_time_2[dep_ptr_2] - h_arrival[h_count] > 0)):                
                    departure_time_1[i] = h_arrival[h_count] + service_time_1[h_count]
                    h_waiting_time_sys = h_waiting_time_sys + service_time_1[h_count]
                    serve_hp_time_1 = serve_hp_time_1 + service_time_1[h_count]
                    h_count = h_count + 1
                    dep_ptr_1 = i  
                else:
                    # server 1 idle first
                    if((departure_time_1[dep_ptr_1] - h_arrival[h_count]) <  (departure_time_2[dep_ptr_2]- h_arrival[h_count])):
                        departure_time_1[i] = h_arrival[h_count] + service_time_1[h_count] + departure_time_1[dep_ptr_1] - h_arrival[h_count]
                        h_waiting_time = h_waiting_time + departure_time_1[dep_ptr_1] - h_arrival[h_count] # accumulate the waiting time
                        h_waiting_time_sys = h_waiting_time_sys + service_time_1[h_count] + (departure_time_1[dep_ptr_1] - h_arrival[h_count])
                        serve_hp_time_1 = serve_hp_time_1 + service_time_1[h_count]
                        h_count = h_count + 1
                        dep_ptr_1 = i
                    else:
                        departure_time_2[i] = h_arrival[h_count] + service_time_2[h_count] + departure_time_2[dep_ptr_2]- h_arrival[h_count]
                        h_waiting_time = h_waiting_time + departure_time_2[dep_ptr_2] - h_arrival[h_count] # accumulate the waiting time
                        h_waiting_time_sys = h_waiting_time_sys + service_time_1[h_count] + (departure_time_2[dep_ptr_2] - h_arrival[h_count])
                        serve_hp_time_2 = serve_hp_time_2 + service_time_2[h_count]
                        h_count = h_count + 1
                        dep_ptr_2 = i
    idle_1 = max(departure_time_1[2*generate.DataNum-1],departure_time_2[2*generate.DataNum-1]) - serve_hp_time_1 - serve_lp_time_1
    idle_2 = max(departure_time_1[2*generate.DataNum-1],departure_time_2[2*generate.DataNum-1]) - serve_hp_time_2 - serve_lp_time_2
    all_hp_waiting_time.append(h_waiting_time/generate.DataNum)
    all_lp_waiting_time.append(l_waiting_time/generate.DataNum)
    all_hp_waiting_time_sys.append(h_waiting_time_sys/generate.DataNum)
    all_lp_waiting_time_sys.append(l_waiting_time_sys/generate.DataNum) 

    all_serve_hp_time_1.append(serve_hp_time_1/max(departure_time_1[2*generate.DataNum-1],departure_time_2[2*generate.DataNum-1]))
    all_serve_lp_time_1.append(serve_lp_time_1/max(departure_time_1[2*generate.DataNum-1],departure_time_2[2*generate.DataNum-1]))
    all_idle_time_1.append(idle_1/max(departure_time_1[2*generate.DataNum-1],departure_time_2[2*generate.DataNum-1]))
    all_serve_hp_time_2.append(serve_hp_time_2/max(departure_time_1[2*generate.DataNum-1],departure_time_2[2*generate.DataNum-1]))
    all_serve_lp_time_2.append(serve_lp_time_2/max(departure_time_1[2*generate.DataNum-1],departure_time_2[2*generate.DataNum-1]))
    all_idle_time_2.append(idle_2/max(departure_time_1[2*generate.DataNum-1],departure_time_2[2*generate.DataNum-1]))

def Numerical(model,mu,lambda_h,lambda_l):
    """This function calculates the numerical result

    Args:
        model (str):  The model to use.
        mu (int): Service time of the server.
        lambda_h (int): Arrival rate of the high priority packets.
        lambda_l (int): Arrival rate of the low priority packets.

    Returns:
       None, but save the result into a list.

    Raises:
       AttributeError, KeyError

    """
    rho = (lambda_h+lambda_l)/mu
    if model == 'MM1_queue':
        T_qh = (lambda_h+lambda_l)/(mu*(mu-lambda_h))
        T_ql = (lambda_h+lambda_l)/((mu-lambda_h-lambda_l)*(mu-lambda_h))
        numerical_hp_wt_queue.append(T_qh)
        numerical_lp_wt_queue.append(T_ql)

    if model == 'MM1_system':
        N_h = ((lambda_h/mu)*(1+rho-lambda_h/mu))/(1-lambda_h/mu) # N_1 in the handout
        N_l = ((lambda_l/mu)*(1+(rho*(lambda_h/mu))-lambda_h/mu))/((1-rho)*(1-lambda_h/mu)) # N_2 in the handout 
        numerical_hp_wt_system.append(N_h/lambda_h)
        numerical_lp_wt_system.append(N_l/lambda_l)

if __name__ == '__main__':

    # 開始測量
    start = time.process_time()

    for i in generate.prob_list:
        Simulation(i)
    Numerical('MM1_queue',60,20,30)
    Numerical('MM1_system',60,20,30)
    plot.plot_waiting_time('queue', all_hp_waiting_time, all_lp_waiting_time, numerical_hp_wt_queue, numerical_lp_wt_queue)
    plot.plot_waiting_time('system', all_hp_waiting_time_sys, all_lp_waiting_time_sys, numerical_hp_wt_system, numerical_lp_wt_system)
    plot.plot_server_state('server1', all_serve_hp_time_1, all_serve_lp_time_1, all_idle_time_1)
    plot.plot_server_state('server2', all_serve_hp_time_2, all_serve_lp_time_2, all_idle_time_2)
    
    # 結束測量
    end = time.process_time()
    print("執行時間: %f 秒" % (end - start))