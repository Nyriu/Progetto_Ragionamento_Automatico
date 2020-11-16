import clingo
import json

ctl = clingo.Control()
ctl.load("./covid19_mod.lp")
ctl.load("./ins_01.lp")
ctl.ground([("base", [])])

#ctl.solve()
#ctl.solve(on_model=lambda m: print("Answer: {}".format("asdasd")))



# Lista di coppie (nome, len(args)) dei predicati e
# del loro numero di argomenti da usare per la soluzione
to_consider = [
  ("malato",       2),
  ("positivo",     2),
  ("osservazione", 2),
  ("quarantena",   2)
]

sol = {
  "M":[],
  "P":[],
  "O":[],
  "Q":[]
}

#print("="*20)
for symb in model:
  name = symb.name
  args = symb.arguments

  if (name, len(args)) in to_consider:
    # TODO fare qualche controllo... fidarsi e' bene ma...
    sol[name[0].upper()].append(args[1].number)

#print(sol)
#print("="*20)

statistics =ctl.statistics
#print("Stats\n",statistics)
#json.dump(statistics, open("statistics.json","w+"), indent=True)

stats = {
  "type" : "ASP",
  "obj" : int(statistics["summary"]["costs"][0]),

  "stats" : {
    "time" : statistics["summary"]["times"]["total"],
    "solveTime" : statistics["summary"]["times"]["solve"],
    #"solutions" : statistics["models"]["enumerated"],
  },

  "sol" : sol
}

json.dump(stats, open("stats.json","w+"), indent=True)
