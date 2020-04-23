from collections import deque
import math
import random

T = 30

class Node:
    
    def __init__(self, number):

        self.queue = deque()
        self.number = number

        self.collission_counter = 0
        self.sensing_counter = 0

        self.attempts = 0
        self.transmitted = 0

    def create_arrivals(self, A):
        current_time = 0

        while current_time < T:
            #random generated arrival time
            arrival_gap = -(1/A) * math.log(1 - random.random())
            current_time += arrival_gap
            self.queue.append(current_time)
    
    def reciever_back_off(self, transmitter_time, L, R, t_prop, distance):
        rand_backoff = random.uniform(0.0, (2.0**self.collission_counter) - 1.0)
        backoff_time = rand_backoff * float(512/R)
        
        #backoff current node by the sending node's time + t_prop + backoff
        self.queue[0] = transmitter_time + t_prop*distance + backoff_time

        for time in self.queue:
            #TODO: transmission time might be referring to a different time
            if time < self.queue[0]:
                time = self.queue[0]

            # alternatively check just the packet before the head
                    
            # if len(node.queue) > 1:
            #     if node.queue[1] < node.queue[0]:
            #         node.queue[1] = node.queue[0]        
    
    def transmitter_back_off(self, L, R, t_trans, t_prop, max_colliding_distance):
        rand_backoff = random.uniform(0.0, (2.0**self.collission_counter) - 1.0)
        backoff_time = rand_backoff * float(512/R)

        #TODO: not sure about t_trans
        self.queue[0] = self.queue[0] + t_prop * max_colliding_distance + backoff_time

        for time in self.queue:
            if time < self.queue[0]:
                time = self.queue[0]

        # alternatively check just the packet before the head

        # if len(transmitter.queue) > 1:
        #     if transmitter.queue[1] < transmitter.queue[0]:
        #         transmitter.queue[1] = transmitter.queue[0]
    
    def wait_back_off(self, transmitter_time, distance, t_prop, t_trans):
        self.queue[0] = transmitter_time + t_prop * distance + t_trans

        for time in self.queue:
            if time < self.queue[0]:
                time = self.queue[0]
    
    def wait_back_off_np(self, transmitter_time, distance, t_prop, t_trans, R):
        #add random wait time once
        rand_backoff = random.uniform(0.0, (2.0**self.sensing_counter) - 1.0)
        backoff_time = rand_backoff * float(512/R)

        self.queue[0] = self.queue[0] + backoff_time
        self.sensing_counter += 1

        #bus is busy even after wait time, keep adding more wait time
        while (self.queue[0] <= transmitter_time + t_prop * distance + t_trans):
            rand_backoff = random.uniform(0.0, (2.0**self.sensing_counter) - 1.0)
            backoff_time = rand_backoff * float(512/R)
            
            self.queue[0] = self.queue[0] + backoff_time
            self.sensing_counter += 1

            #sensed 10 times, drop and break
            if(self.sensing_counter > 10):
                self.queue.popleft()
                break
        
        #reset counter once bus is no longer busy
        self.sensing_counter = 0
