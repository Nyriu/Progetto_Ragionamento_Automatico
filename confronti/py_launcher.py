from minizinc import Instance, Model, Solver

def read_dzn(fpath):
    # TODO try catch
    f = open(fpath)

    comment_char = '%'
    values = {'K':-1,'H':-1,'M':-1,'P':-1,'O':-1,'Q':-1}

    lines = f.readlines()
    for l in lines:
        if comment_char in l:
            index = l.find(comment_char)
            l = l[0:index]

        l = l.replace(" ","")
        l = l.replace("\t","")
        l = l.replace("\n","")
        if not l=='' and '=' in l and ';' in l:
            l = l.replace(";","")
            k,v = l.split('=')
            if k in values.keys():
                # TODO try catch su int
                values[k] = int(v)


    for k in values.keys():
        if values[k] == -1:
            print("Not well formatted input")
            exit(2)

    return values


# Load model from file
model = Model("./008_covid19.mzn")

# Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("gecode")

# Create an Instance of the n-Queens model for Gecode
instance = Instance(gecode, model)


instance["K"]=1; # corridoi
instance["H"]=3; # stanze per lato

instance["M"]=1; # malati
instance["P"]=2; # positivi
instance["O"]=0; # osservazione
instance["Q"]=2; # quarantena precauzionale


result = instance.solve()

# Output the array q
print("Min : %d" %(result.objective))

for k in result.statistics.keys():
    print("%s : %s" %(k, str(result.statistics[k])))


pretty.py
