from fastapi import FastAPI, Response, status
from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

app = FastAPI()

class Fila(BaseModel):
    id: Optional[int] = 0
    nome: constr(max_length=20)
    atendimento: constr(max_length=1)
    data: Optional[str] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    atendido: Optional[bool] = False

db_fila = [
    Fila(id=1, nome="João", atendimento = "P", data="17-10-22", atendido = False),
    Fila(id=2, nome="Ana", atendimento = "N", data="17-10-22", atendido = False),
    Fila(id=3, nome="Duda", atendimento = "N", data="17-10-22", atendido = False),
    Fila(id=4, nome="Pedro", atendimento = "P", data="17-10-22", atendido = False),
    Fila(id=5, nome="Rafael", atendimento = "N", data="17-10-22", atendido = False),
    Fila(id=6, nome="Maria", atendimento = "N", data="17-10-22", atendido = False),
    Fila(id=7, nome="José", atendimento = "P", data="17-10-22", atendido = False),
    Fila(id=8, nome="Antônio", atendimento = "N", data="17-10-22", atendido = False),
    Fila(id=9, nome="Regina", atendimento = "N", data="17-10-22", atendido = False),
    Fila(id=10, nome="Rose", atendimento = "P", data="17-10-22", atendido = False),
]

last_id = db_fila[-1].id
cnt = 0

@app.get("/")
def home():
    return {"Mensagem":"API, gerenciador de fila, funciona por ordem de chegada e sistema de Prioridade (A cada 2 prioritarios chama 1 Normal [caso haja prioritario])"}

@app.get("/fila")
def mostrar_fila():
    if not db_fila:
        return {"Aviso":"A fila está vazia"}
    else:
        return {"Fila": db_fila}

@app.get("/fila/{id}")
def mostrar_id(id: int, response: Response):
    try:
        for x in db_fila:
            if x.id == id:
                aux = x
                break
        return {"Pessoa":aux}
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Aviso":"Não existe ninguem na posição informada"}

@app.post("/fila")
def adicionar_fila(fila: Fila):
    global last_id
    fila.id = last_id + 1
    fila.data = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    db_fila.append(fila)
    last_id += 1
    return {"Aviso":"Pessoa adicionada a fila"}
    

@app.put("/fila")
def chamar_fila():
    if not db_fila:
        return {"Aviso":"A fila está vazia"}
    else:
        global cnt
        aux = 0
        pri = None
        #Ao chamar a fila o sistema verifica se tem alguem como "P"(prioritario), caso tenha ele guarda a posição do primeiro.
        for n in db_fila:
            aux += 1
            if n.atendimento.upper() == "P":
                pri = aux - 1
                break
        #Em seguida verifica se o contador (cnt) é menor que 2 (a cada dois prioritarios ele automaticamente chama um normal), e se existe alguem como prioritario, senão chama o atendimento normal
        if pri != None and cnt < 2:
            atual = db_fila.pop(pri)
            cnt += 1
            return {"Chamando": atual}
        else:
            atual = db_fila.pop(0)
            cnt = 0
            return {"Chamando": atual}

@app.delete("/fila/{id}")
def apagar_id(id: int, response: Response):
    try:
        aux = -1
        for pessoa in db_fila:
            aux += 1
            if pessoa.id == id:
                msg = db_fila.pop(aux)
                break
        return {"Removido": msg}
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Aviso":"Não existe ninguem na posição informada"}