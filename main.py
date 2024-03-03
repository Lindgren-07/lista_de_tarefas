from flask import Flask,redirect,request,render_template,flash
import json, os.path


app = Flask(__name__)
app.secret_key = 'joao07'
app.config['DEBUG'] = True

concluidos = []

class Tarefas:
    def __init__(self,incremento,tarefa):
        self.incremnto = incremento
        self.nome_tarefa = tarefa

    def __str__(self):
        return f'{self.incremnto}, {self.nome_tarefa}'



def obterId():
    if os.path.isfile('tarefas.json') and os.path.getsize('tarefas.json') > 0:
        with open('tarefas.json') as tf:
            tarefas_py = json.load(tf)
            if tarefas_py:
                return tarefas_py[-1]['id']
    return 0

    



@app.route('/')
def home():
    tarefas_json = []  
    if os.path.isfile('tarefas.json') and os.path.getsize('tarefas.json') > 0:
        with open('tarefas.json') as tf:
            tarefas_json = json.load(tf)
    return render_template('index.html',tarefas_json=tarefas_json)


@app.route('/adicionar_tarefa',methods=['POST'])
def adicionar_tarefa():

    tarefaD = request.form.get('tarefa')
    novo_id = obterId() + 1
    tarefa_obj = Tarefas(novo_id,tarefaD)
    

    tarefa_dict = dict()
    tarefa_dict['id'] = tarefa_obj.incremnto
    tarefa_dict['nome_tarefa'] = tarefa_obj.nome_tarefa

   

    tarefa_list = list()

    if os.path.isfile('tarefas.json') and os.path.getsize('tarefas.json') > 0:
        with open('tarefas.json') as tf:
            tarefas_py = json.load(tf)
            tarefa_list.extend(tarefas_py)
    tarefa_list.append(tarefa_dict)
    with open('tarefas.json', 'w') as tf:
        json.dump(tarefa_list,tf,indent=2)

    flash(f'"{tarefa_obj.nome_tarefa}" adicionado(a) com sucesso !')

    return redirect('/')



@app.route('/concluir_excluir',methods=['POST'])
def concluir_excluir():
    
   
    
    tarefa_id = int(request.form.get('id_ta'))
    tarefa_nome = request.form.get('nome_ta')
    btn = request.form.get('btn')
    
  


    

    
    if btn == 'excluir':
        with open('tarefas.json') as tf:
                tarefas_py = json.load(tf)
                # Criar uma cópia da lista
                tarefas_copia = tarefas_py[:]
                for tarefa in tarefas_copia:
                    if tarefa['id'] == tarefa_id:
                        tarefas_py.remove(tarefa)
                        flash(f'"{tarefa_nome}" excluido(a) com sucesso')
                        break
    else:
        with open('tarefas.json') as tf:
            tarefas_py = json.load('tarefas.json')
            tarefas_copia = tarefas_py[:]
            for tarefa in tarefas_copia:


        
    with open('tarefas.json', 'w') as tf:
            json.dump(tarefas_py, tf, indent=2)
    return redirect('/')










if __name__ == '__main__':
    app.run(debug=True)

