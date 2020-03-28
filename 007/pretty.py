
fname = "output_03.txt"

f = open(fname)
raw_lines = f.readlines()
lines = [l for l in raw_lines if ( l != 10*'-'+'\n' and l != 10*'='+'\n' and l != '\n')]




#def get_solutions(fname):





###def format_as_json(text):
###
###    text = '[\n' + text
###    text = text.replace(10*'-',',')
###    text = text.replace(10*'=',']')
###    text = text.replace('\n]\n,\n]','\n]\n]')
###
###    return text
###
####def show_solution(sol):
####    for i in 







#print(text))
#print(format_as_json(text))

#solutions = json.loads(format_as_json(text))


