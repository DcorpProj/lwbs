import gc
import os
import machine
import sys
import time

print(r"""___       ___       __   ________  ________      
|\  \     |\  \     |\  \|\   __  \|\   ____\     
\ \  \    \ \  \    \ \  \ \  \|\ /\ \  \___|_    
 \ \  \    \ \  \  __\ \  \ \   __  \ \_____  \   
  \ \  \____\ \  \|\__\_\  \ \  \|\  \|____|\  \  
   \ \_______\ \____________\ \_______\____\_\  \ 
    \|_______|\|____________|\|_______|\_________\
                                      \|_________|
                - lightweight board shell""")
print("       [v1.1 stable = LTS]")
gc.collect()
print("      free ram : {} bytes".format(gc.mem_free()))
print("      used ram : {} bytes".format(gc.mem_alloc()))
print("          freq : {} MHz".format(machine.freq() // 1000000))
print("  [initialized] hello from lwbs!")
print("            [ => enter help to get all commands]")
try:
    p = int(input("enter led pin (needed for led function) >>> "))
except:
    p = 2
def ed(filename=""):
    buffer = []
    if filename in os.listdir():
        with open(filename, 'r') as f:
            buffer = f.read().splitlines()
    
    print("lw-ed for v1 ('.' to end input)")
    
    while True:
        try:
            cmd = input(": ").strip()
            
            if cmd == "a":
                while True:
                    line = input()
                    if line == ".": break
                    buffer.append(line)
            
            elif cmd == "p":
                for i, line in enumerate(buffer):
                    print("{}: {}".format(i + 1, line))
            
            elif cmd == "d":
                if buffer: buffer.pop()
            
            elif cmd == "w":
                if filename:
                    with open(filename, 'w') as f:
                        f.write("\n".join(buffer))
                    print(len("\n".join(buffer)))
            
            elif cmd == "q":
                break
                
            else:
                print("?")
        except Exception as e:
            print("err:", e)


def shell():
    global p
    while True:
        try:
            line = input("lwbs $ ").strip().split()
            if not line: continue
            cmd = line[0]
            args = line[1:]
            print(args)
            if cmd == "help":
                print("ls, cd, pwd, free, cpu, echo, cat, rm, mkdir, led, reset, info, exit")
            elif cmd == "ls":
                print("  ".join(os.listdir()))
            elif cmd == "pwd":
                print(os.getcwd())
            elif cmd == "cd":
                os.chdir(args[0] if args else "/")
            elif cmd == "free":
                gc.collect()
                print("F: {} U: {}".format(gc.mem_free(), gc.mem_alloc()))
            elif cmd == "cpu":
                if args: machine.freq(int(args[0]))
                print(machine.freq())
                print("(hz)")
            elif cmd == "echo":
                print(" ".join(args))
            elif cmd == "cat":
                with open(args[0], 'r') as f: print(f.read())
            elif cmd == "rm":
                os.remove(args[0])
            elif cmd == "mkdir":
                os.mkdir(args[0])
            elif cmd == "led":
                l = machine.Pin(p, machine.Pin.OUT)
                l.value(int(args[0].strip()) if args else not p.value())
            elif cmd == "info":
                print(sys.implementation.name, sys.version)
            elif cmd == "reset":
                machine.reset()
            elif cmd == "ed":
                ed(args[0] if args else "new.txt")
            elif cmd == "exit":
                break
            else:
                print("not found")
        except Exception as e:
            print("err:", e)

shell()
