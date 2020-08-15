def cargar_estudiantes(nombre_archivo:str)->dict:
    estudiantes = {}
    archivo = open (nombre_archivo,"r")
    encabezado= archivo.readline()
    linea=archivo.readline()
    while len(linea)>0:
        datos=linea.split(",")
        estudiante=datos[0]
        materia_esp={}
        materia_esp["materia"]= datos[1]
        materia_esp["profesor"]=datos[2]
        materia_esp["creditos"]=int(datos[3])
        materia_esp["fallas"]=int(datos[4])
        materia_esp["nota"]=float(datos[5].strip("\n"))
        linea=archivo.readline()
        if estudiante in estudiantes.keys():
            estudiantes[estudiante].append(materia_esp)
        else:
            estudiantes[estudiante]=[materia_esp]
    archivo.close()
    return estudiantes
x=cargar_estudiantes("./estudiantes.csv")


#print(consultar_estudiante(x,"202040003"))
def consultar_estudiante(estudiantes:dict, codigo_estudiante:str)->list:
    lista_materias=estudiantes.get(codigo_estudiante)
    return lista_materias

def materia_en_peligro(estudiantes:dict,codigo_estudiante:str,nota_minima:float)->bool:
    esta_peligro=False
    materias=consultar_estudiante(estudiantes,codigo_estudiante)
    for materia in materias:
        if materia["nota"]<nota_minima:
            esta_peligro=True
    return esta_peligro
#print(materia_en_peligro(x,"202040001",1.74))


def sobrecredito(estudiantes:dict,codigo_estudiante:str)->bool:
    sobreacreditado=False
    materias= consultar_estudiante(estudiantes,codigo_estudiante)
    contador=0
    for materia in materias:
        contador+=materia["creditos"]
    if contador >20:
        sobreacreditado=True
    return sobreacreditado
#print(sobrecredito(x,"202040001"))


def promedio_estudiante(estudiantes:dict,codigo_estudiante)->float:
    materias= consultar_estudiante(estudiantes,codigo_estudiante)
    suma_divisor=0
    suma_dividendo=0
    for materia in materias:
        dividendo= materia["creditos"]*materia["nota"]
        suma_dividendo+=dividendo
        suma_divisor+=materia["creditos"]
    ecuacion=suma_dividendo/suma_divisor
    return round(ecuacion,2)


def candidatos_beca(estudiantes:dict)->list:
    cuenta_creditos=0
    becados=[]
    for codigo in estudiantes:
        promedio= promedio_estudiante(estudiantes,codigo)
        materias=consultar_estudiante(estudiantes,codigo)
        materia_peligro= materia_en_peligro( estudiantes,codigo,3.5)
        cuenta_creditos=0
        for materia in materias:
            cuenta_creditos+=materia["creditos"]
        if promedio>=4 and cuenta_creditos>=15 and materia_peligro is False:
                becados.append({"codigo":codigo,"promedio":promedio,"creditos":cuenta_creditos})
    return becados
#print(candidatos_beca(x))


def desafortunados(estudiantes: dict) -> list:

    estudiantes_desadortunados=[]
    estudiante_desafortunado={}
    for codigo in estudiantes:
        materias= consultar_estudiante(estudiantes,codigo)
        for materia in materias:
            estudiante_desafortunado={}
            fallas=materia["fallas"]
            nota=materia["nota"]
            if fallas>6 and nota>=3:
                estudiante_desafortunado["codigo"]= codigo
                estudiante_desafortunado["materia"]=materia["materia"]
                estudiante_desafortunado["nota"]=materia["nota"]
                estudiante_desafortunado["fallas"]=fallas
                estudiantes_desadortunados.append(estudiante_desafortunado)
    return estudiantes_desadortunados
#print(desafortunados(x))
#print(len(desafortunados(x)))


def promedio_profesor(estudiantes: dict, nombre_profesor:str) -> float:
    promedio=0
    cuenta_notas=0
    numero_de_notas=0
    cuenta_notas=0
    for codigo in estudiantes:
        materias= estudiantes[codigo]
        for materia in materias:
            profesor= materia["profesor"]
            nota=materia["nota"]
            if profesor ==nombre_profesor:
                cuenta_notas+=nota
                numero_de_notas+=1
    if numero_de_notas==0:
        promedio =0
    else:
        promedio= cuenta_notas/numero_de_notas
    return promedio
#print(promedio_profesor(x, "Veronica Salguero Mar"))
    
def promedio_materia(estudiantes: dict,nombre_profesor:str,nombre_materia:str)->float:
    promedio=0
    cuenta_notas=0
    numero_de_notas=0
    for codigo in estudiantes:
        materias= consultar_estudiante(estudiantes,codigo)
        for materia in materias:
            materia_n= materia["materia"]
            profesor = materia["profesor"]
            nota=materia["nota"]
            if materia_n ==nombre_materia and profesor==nombre_profesor:
                cuenta_notas+=nota
                numero_de_notas+=1
    if numero_de_notas==0:
        promedio =0
    else:
        promedio= cuenta_notas/numero_de_notas
    return promedio
#print (promedio_materia(x,"Veronica Salguero Martin","Ingles: Speaking"))

def materias_coco(estudiantes: dict) -> dict:
    coco={}
    for codigo in estudiantes:
        materias= consultar_estudiante(estudiantes,codigo)
        for materia in materias:
            profesor= materia["profesor"]
            materia_n= materia["materia"]
            promedio= promedio_materia(estudiantes,profesor,materia_n)
            coco[materia_n+" - "+profesor]=promedio
    coco_respuesta={}
    for profesor in coco:
        if len(coco_respuesta)<3:
            coco_respuesta[profesor]=coco[profesor]
        
        else:
            mayor=0
            llave_mayor=""
            for llave in coco_respuesta:
                
                if mayor < coco_respuesta[llave]:
                    llave_mayor= llave
                    mayor=coco_respuesta[llave]
            if coco[profesor]< mayor:
                del coco_respuesta[llave_mayor]
                coco_respuesta[profesor]=coco[profesor]
    return coco_respuesta
#print(materias_coco(x))
    
    
def aplicar_curva_curso(estudiantes: dict,nombre_profesor:str,nombre_materia:str) -> None:
    for codigo in estudiantes:
        materias= consultar_estudiante(estudiantes, codigo)
        for materia in materias:
            materia_n= materia["materia"]
            profesor= materia["profesor"]
            if nombre_profesor== profesor and materia_n==nombre_materia:
                materia["nota"]*=1.05
            if materia["nota"]>=5:
                materia["nota"]=5

#print(aplicar_curva_curso(x,"Veronica Salguero Martin","Ingles: Speaking"))




def dar_estudiante_cumplido(estudiantes:dict)->dict:
    fallas_estudiantes={}
    for codigo in estudiantes:
        materias= consultar_estudiante(estudiantes,codigo)
        for materia in materias:
            contador=0
            contador+=materia["fallas"]
            fallas_estudiantes[codigo]=contador
        respuesta={}
        for estudiante in fallas_estudiantes:
            if len(respuesta)<1:
                respuesta[codigo ]= fallas_estudiantes[estudiante]
            else: 
                menor=0
                llave_menor=""
                for llave in respuesta:
                    if respuesta[llave] > menor :
                        llave_menor= llave
                        menor=respuesta[llave]
                if fallas_estudiantes[estudiante]< menor:
                    del respuesta[llave_menor]
                    respuesta[estudiante]=fallas_estudiante[estudiante]
    return respuesta
    
print (dar_estudiante_cumplido(x))









