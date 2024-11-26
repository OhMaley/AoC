# Puzzle:            https://adventofcode.com/2023/day/20
# Video explanation: https://youtu.be/zw7WwUZfYrs

# 1. part - What do you get if you multiply the total number of low pulses sent by the total number of high pulses sent?
from collections import defaultdict
import queue

with open('input.txt') as f:
    # input parsing
    modules = defaultdict(lambda: {"dest": [], "type": None, "val": dict()})
    for line in f.readlines():
        name, destinations = line.strip().split(" -> ")
        t, value = None, None
        if name[0] in ["%", "&"]:       # if flip-flop or conjuction
            t, name = name[0], name[1:] # split type and name
        module = modules[name]
        module["dest"] = destinations.split(", ")
        module["type"] = t
        if t == "%": # flip-flop has one value instead of a dictionary
            module["val"] = False

        # init values for destinations which are conjuction modules
        for d in module["dest"]:
            if type(modules[d]["val"]) is dict:
                modules[d]["val"][name] = False

    # simulation
    counter = {False: 0, True: 0} # pulse usage: False=low, True=high
    for _ in range(1000):
        pulses = queue.Queue()
        pulses.put(("button", False, "broadcaster"))  # start by pressing button - sending low (False)

        while not pulses.empty():  # while there are pulses in circulation
            u, p, v = pulses.get() # u - sender, p - type of pulse, v - receiver
            
            counter[p] += 1 # increment counter of pulse usage

            if modules[v]["type"] == '&':               # conjuction module
                modules[v]["val"][u] = p                # first updates its memory
                p = not all(modules[v]["val"].values()) # NAND gate
            elif modules[v]["type"] == '%':                   # flip-flop module
                if p == True: 
                    continue                                  # high pulses get ignored
                p = modules[v]["val"] = not modules[v]["val"] # on -> high, off -> low

            # send modified pulse to destination modules
            for d in modules[v]["dest"]:
                pulses.put((v, p, d))

    print(counter[False] * counter[True])

# 2. part - What is the fewest number of button presses required to deliver a single low pulse to the module named rx?
from collections import defaultdict
import queue
import math

with open('input.txt') as f:
    # input parsing
    modules = defaultdict(lambda: {"dest": [], "type": None, "val": dict()})
    for line in f.readlines():
        name, destinations = line.strip().split(" -> ")
        t, value = None, None
        if name[0] in ["%", "&"]:       # if flip-flop or conjuction
            t, name = name[0], name[1:] # split type and name
        module = modules[name]
        module["dest"] = destinations.split(", ")
        module["type"] = t
        if t == "%": # flip-flop has one value instead of a dictionary
            module["val"] = False

        # init values for destinations which are conjuction modules
        for d in module["dest"]:
            if type(modules[d]["val"]) is dict:
                modules[d]["val"][name] = False

    conjuction_module_cycles = {}
    for i in range(1, 5000): # 5000 is a magic number
        pulses = queue.Queue()
        pulses.put(("button", False, "broadcaster"))  # start by pressing button - sending low (False)

        while not pulses.empty():  # while there are pulses in circulation
            u, p, v = pulses.get() # u - sender, p - type of pulse, v - receiver
            
            counter[p] += 1 # increment counter of pulse usage

            if modules[v]["type"] == '&':               # conjuction module
                modules[v]["val"][u] = p                # first updates its memory
                p = not all(modules[v]["val"].values()) # NAND gate

                # CHANGE HERE: find how long it takes for conjuction module to produce low (False)
                if p == False and v not in conjuction_module_cycles:
                    conjuction_module_cycles[v] = i

            elif modules[v]["type"] == '%':                   # flip-flop module
                if p == True: 
                    continue                                  # high pulses get ignored
                p = modules[v]["val"] = not modules[v]["val"] # on -> high, off -> low

            # send modified pulse to destination modules
            for d in modules[v]["dest"]:
                pulses.put((v, p, d))
    
    # print(math.lcm(*conjuction_module_cycles))
    print(math.prod(conjuction_module_cycles.values())) # only prime numbers
