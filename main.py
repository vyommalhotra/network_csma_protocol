from node import Node
from network import Network
import csv
import math
import random

if __name__ == "__main__":

    R = 1000000
    L = 1500
    D = 10
    S = 2*100000000
    T = 100
    
    def run_stimulation(N, A, R, L, D, S, persistent):
        t_prop = float(D/S)
        t_trans = float(L/R)

        #create network with N nodes
        network = Network(N, t_prop, t_trans, L, R)

        #populate nodes with arrival times
        network.setup(A)

        #run stimulation, start sending
        network.stimulate(persistent)

        return network.successes, network.attempts
    
    def persistent_csv(e_results, t_results):
        
        # write results to efficiency csv
        file = 'persistent_efficiency.csv'
        headers = ['Arrival Rate', 'Nodes', 'Efficiency']

        with open(file, mode='w') as output_file:
            output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            output_writer.writerow(headers)

            for result in e_results:
                output_writer.writerow(result)

        print('Results written to {}'.format(file))

        # write results to throughput csv
        file = 'persistent_throughput.csv'
        headers = ['Arrival Rate', 'Nodes', 'Throughput']

        with open(file, mode='w') as output_file:
            output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            output_writer.writerow(headers)

            for result in t_results:
                output_writer.writerow(result)

        print('Results written to {}'.format(file))

    def non_persistent_csv(e_results, t_results):
        # write results to efficiency csv
        file = 'non_persistent_efficiency.csv'
        headers = ['Arrival Rate', 'Nodes', 'Efficiency']

        with open(file, mode='w') as output_file:
            output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            output_writer.writerow(headers)

            for result in e_results:
                output_writer.writerow(result)

        print('Results written to {}'.format(file))

        # write results to throughput csv
        file = 'non_persistent_throughput.csv'
        headers = ['Arrival Rate', 'Nodes', 'Throughput']

        with open(file, mode='w') as output_file:
            output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            output_writer.writerow(headers)

            for result in t_results:
                output_writer.writerow(result)

        print('Results written to {}'.format(file))

    def get_results():

        quantities = [20, 40, 60, 80, 100]
        rates = [7, 10, 20]

        e_results = []
        t_results = []

        row = []

        #persistent efficiency & throughput
        persistent = True

        #run simulation for different arrival rates and number of Nodes
        for A in rates:
            for N in quantities:
                successes, attempts = run_stimulation(N, A, R, L, D, S, persistent)
                efficiency = float(successes / attempts)
                throughput = float((successes * L) / T) / 1000000.0
                row = [A, N, efficiency]
                e_results.append(row)
                row = [A, N, throughput]
                t_results.append(row)

        #write to csv
        persistent_csv(e_results, t_results)

        #reset lists
        e_results = []
        t_results = []

        #non persistent efficiency and throughput
        persistent = False
        
        #run simulation for different arrival rates and number of Nodes
        for A in rates:
            for N in quantities:
                successes, attempts = run_stimulation(N, A, R, L, D, S, persistent)
                efficiency = float(successes / attempts)
                throughput = float((successes * L) / T) / 1000000.0
                row = [A, N, efficiency]
                e_results.append(row)
                row = [A, N, throughput]
                t_results.append(row)

        #write to csv
        non_persistent_csv(e_results, t_results)

    get_results()



    




        









