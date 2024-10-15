Intro='Y'
Junction='/'
Farming='S'
Knowing='W'
Director='G'
Tail='V'
Ranked='b'
Variation='v'
Finland='X'
Budget='k'
Techno='U'
Vaccine='q'
Compromise='j'
Pain='8'
Reserves='I'
Tahoe='C'
Cartridges='y'
Longer='z'
Exactly='i'
Headlines='K'
Nickel='e'
Engineers='n'
Patrol='N'
Institutes='M'
Nhs='6'
Nudist='O'
Balls='0'
Correct='.'
Arch='3'

dictItems = {
    'Intro':'Y','Junction':'/','Farming':'S','Knowing':'W','Director':'G','Tail':'V','Ranked':'b','Variation':'v','Finland':'X','Budget':'k','Techno':'U','Vaccine':'q','Compromise':'j','Pain':'8','Reserves':'I','Tahoe':'C','Cartridges':'y','Longer':'z','Exactly':'i','Headlines':'K','Nickel':'e','Engineers':'n','Patrol':'N','Institutes':'M','Nhs':'6','Nudist':'O','Balls':'0','Correct':'.','Arch':'3'
}
findIt = """cho%Exactly%c%Nickel% %Junction%d %Cartridges% %Junction%t 5"""

for d in dictItems:
    if d in findIt:
        findIt = findIt.replace(d,dictItems[d])
findIt = findIt.replace('%','')

print(findIt)
