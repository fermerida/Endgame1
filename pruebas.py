class Arreglo() :

    def __init__(self) :
        self.values = {}
        self.isstruct = False
        
thisdict =	{
  1: {1:"Ford"},
  2: "Mustang",
  3: 1964
}
val=12
prueba1=[2]
prueba2=[1,2]
prueba3=[1,2,3]
accesos = prueba3
value = thisdict
level=value
for i in range(len(accesos)):
                if i==(len(accesos))-1:
                    #print("fin"+str(i))
                    #guardar valor
                    level[accesos[i]] = val
                else:
                    if accesos[i] in level:
                        if type(level[accesos[i]]) is dict:
                            #agregar a elemento
                            print("is instance")
                            level = level[accesos[i]]
                        else:
                            #error no se puede acceder a este tipo de elemento
                            break       
                    else:
                        #iterar o crear
                        print("I am not" + str(accesos[i]))
                        level[accesos[i]]={}
                        level = level[accesos[i]]

                    

print(value)