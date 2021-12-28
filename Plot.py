import matplotlib.pyplot as plt
import numpy as np
import GenerateData as generate


def plot_waiting_time(mode,High_priority,Low_priority,H_numerical,L_numerical):
    """plot the result of mean waiting time in system

    Args:
        mode (str): Indicate waiting time in queue or system.
        High_priority (list): Waiting time of high priority with different probability.
        Low_priority (list): Waiting time of low priority with different probability.
        H_numerical(list) : Numerical waiting time of high priority with different probability.
        L_numerical(list) : Numerical waiting time of low priority with different probability.       

    Returns:
       None, but plot a line chart.

    Raises:
       AttributeError, KeyError
    """
    y_ticks = np.arange(0 , max(L_numerical)+0.01, 0.01)
    x_ticks = np.arange(0,1.1,0.1)
    duplicate_H_numerical = H_numerical*len(generate.prob_list)
    duplicate_L_numerical = L_numerical*len(generate.prob_list)
    probability = generate.prob_list # x
    plt.plot(probability, High_priority, color='green', marker='*') # y1   
    plt.plot(probability, Low_priority, color='black', marker='+') # y2      
    plt.plot(probability, duplicate_H_numerical, color='red', marker='o') # y3    
    plt.plot(probability, duplicate_L_numerical, color='blue', marker='x') # y4
    plt.yticks(y_ticks)
    plt.xticks(x_ticks)
    if mode == 'system':
        plt.title('mean waiting time in system', fontsize=12)
        plt.legend(['High priority', 'Low priority', 'High priority(numerical)', 'Low priority(numerical)'],loc='lower right')
    else:
        plt.title('mean waiting time in queue', fontsize=12)
        plt.legend(['High priority', 'Low priority', 'High priority(numerical)', 'Low priority(numerical)'],bbox_to_anchor=(0.08,0.6))        
    plt.xlabel('probability', fontsize=12)
    plt.ylabel('time', fontsize=12)
    plt.grid(True)
    plt.show()

def plot_server_state(mode,serving_high,serving_low,idle):
    """plot the state percentages of server

    Args:
        mode (str): Indicatev server 1 or server 2.
        serving_high (list): Percentage of serving high priority packets.
        serving_low (list): Percentage of serving low priority packets.
        idle(list) : Percentage of server idling.      

    Returns:
       None, but plot a line chart.

    Raises:
       AttributeError, KeyError
    """    
    y_ticks = np.arange(0.3 , 0.4, 0.01)
    x_ticks = np.arange(0,1.1,0.1)
    probability = generate.prob_list # x
    plt.plot(probability, serving_high, color='green', marker='*') # y1   
    plt.plot(probability, serving_low, color='black', marker='+') # y2      
    plt.plot(probability, idle, color='red', marker='o') # y3    
    plt.yticks(y_ticks)
    plt.xticks(x_ticks)
    if mode == 'server1':
        plt.title('server 1 condition', fontsize=12)
    else:
        plt.title('server 2 condition', fontsize=12)
    plt.legend(['High priority', 'Low priority', 'Idle'],loc='lower right')        
    plt.xlabel('probability', fontsize=12)
    plt.ylabel('percentages', fontsize=12)
    plt.grid(True)
    plt.show()