from collections import deque
from node import Node
import math
import random

class Network:
     
    def __init__(self, quantity, t_prop, t_trans, L, R):
        self.quantity = quantity
        self.nodes = []

        self.t_prop = t_prop
        self.t_trans = t_trans
        self.L = L
        self.R = R

        self.attempts = 0
        self.successes = 0
        self.collissions = 0
        self.discarded = 0

        self.col1 = 0
        self.col2 = 0

        for node in range(0, quantity):
            self.nodes.append(Node(node))
    
    def setup(self, A):
        for node in self.nodes:
            node.create_arrivals(A)

    def all_queues_empty(self):
        #count the empty nodes
        counter = 0
        for node in self.nodes:
            if(len(node.queue) == 0):
                counter += 1
        
        #check if all nodes are empty
        if counter == len(self.nodes):
            return True

        else:
            return False

    def get_next_transmitter(self):
        
        #find the transmitter
        transmitter = Node(-1)

        #start the transmitter as the first non empty node
        for node in self.nodes:
            if len(node.queue) > 0:
                transmitter = node
                break
        
        #transmitter becomes the node with the lowest time
        for node in self.nodes:
            if len(node.queue) > 0:
                if node.queue[0] < transmitter.queue[0]:
                    transmitter = node

        return transmitter

    def send_to_recievers(self, transmitter, persistent):

        # whether the transmitter collided with any when sending
        collided = False
        max_colliding_distance = 0

        self.attempts += 1
        transmitter.attempts += 1

        for node in self.nodes:
            distance = abs(transmitter.number - node.number)
            
            #don't compare with self
            if distance != 0:                            

                #could collide
                if len(node.queue) > 0:

                    #collission
                    if (transmitter.queue[0] + (distance * self.t_prop)) >= node.queue[0]:
                        self.attempts += 1 
                        self.collissions += 1
                        node.collission_counter += 1
                        collided = True
                        self.col1 += 1
                        
                        #keep track of the max collided distance from transmitting node
                        if distance > max_colliding_distance:
                            max_colliding_distance = distance

                        #drop packet if collided 10 times
                        if node.collission_counter > 10:
                            #TODO: might need to pop on transmitter instead
                            node.queue.popleft()
                            self.discarded += 1
                            node.collission_counter = 0

                        #exponential back-off
                        else:
                            node.reciever_back_off(transmitter.queue[0], self.L, self.R, self.t_prop, distance)

                    elif (transmitter.queue[0] + (self.t_prop * distance)) < node.queue[0] <= (transmitter.queue[0] + (self.t_prop * distance) + self.t_trans):
                         
                         if (persistent):
                            node.wait_back_off(transmitter.queue[0], distance, self.t_prop, self.t_trans)
                         else:
                             node.wait_back_off_np(transmitter.queue[0], distance, self.t_prop, self.t_trans, self.R)

                    #no collission
                    else:
                        node.transmitted += 1
                        #TODO:check if we need to do this
                        #node.collission_counter = 0
                        #self.successes += 1
                
                #no collission
                else :
                    node.transmitted += 1
                    #TODO: check if we need to do this
                    #node.collission_counter = 0
                    #self.successes += 1

        return collided, max_colliding_distance

    def update_transmitter(self, transmitter, collided, max_colliding_distance):
        #transmitter collided with any recieiving nodes
        if collided:
            transmitter.collission_counter += 1
            self.collissions += 1
            self.col2+=1

            #TODO: not sure if we need this
            
            #transmitter's collision counter reaches more than 10
            if transmitter.collission_counter > 10:
                transmitter.queue.popleft()
                self.discarded += 1
                transmitter.collission_counter = 0

            #transmitter exponential backoff
            else:
                transmitter.transmitter_back_off(self.L, self.R, self.t_trans, self.t_prop, max_colliding_distance)        

        #transmitter doesn't collide with any recieving nodes
        else:
            transmitter.queue.popleft()
            transmitter.collission_counter = 0
            transmitter.transmitted += 1
            self.successes += 1
    
    def stimulate(self, persistent):

        #loop until all nodes are empty
        while(1):

            if (self.all_queues_empty()):
                break

            transmitter = self.get_next_transmitter()

            collided, max_colliding_distance = self.send_to_recievers(transmitter, persistent)

            self.update_transmitter(transmitter, collided, max_colliding_distance)



        


