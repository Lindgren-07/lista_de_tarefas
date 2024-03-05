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

def obterIdConcluido():
    if os.path.isfile('concluido.json') and os.path.getsize('concluido.json'):
        with open('concluido.json') as c:
            concluido_py = json.load(c)
            return concluido_py[-1]['id'] + 1
    
    return 1

    



@app.route('/')
def home():
    tarefas_json = []  
    concluido_json = []
    if os.path.isfile('tarefas.json') and os.path.getsize('tarefas.json') > 0:
        with open('tarefas.json') as tf:
            tarefas_json = json.load(tf)
    if os.path.isfile('concluido.json') and os.path.getsize('concluido.json') > 0:
        with open('concluido.json') as c:
            concluido_json = json.load(c)
    return render_template('index.html',tarefas_json=tarefas_json,concluido_json=concluido_json)


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
    novo_id = obterIdConcluido() 
    tarefa_nome = request.form.get('nome_ta')
    btn_excluir = request.form.get(f'btn_excluir_{tarefa_id}')
    
    
  


    

    
    if btn_excluir:
        
        with open('tarefas.json') as tf:
                tarefas_py = json.load(tf)
               
                for tarefa in tarefas_py:
                    if tarefa['id'] == tarefa_id:
                        print(tarefa['id'])
                        print(tarefa)
                        tarefas_py.remove(tarefa)
                        flash(f'"{tarefa_nome}" excluido(a) com sucesso')
                        break
    else:
        tarefa_dict = {
            'id':novo_id,
            'nome_tarefa':tarefa_nome
        }
        concluido = []
        with open('tarefas.json') as tf:

            tarefas_py = json.load(tf)
            for tarefa in tarefas_py:
                if tarefa['id'] == tarefa_id:
                    tarefas_py.remove(tarefa)
        
        if os.path.isfile('concluido.json') and os.path.getsize('concluido.json') > 0:
            with open('concluido.json') as c:
                concluido_py = json.load(c)
                concluido.extend(concluido_py)

        concluido.append(tarefa_dict)
        
        with open('concluido.json','w') as c:
            json.dump(concluido,c,indent=2)
        flash(f'"{tarefa_nome}" concluido(a) com sucesso ')


        
    with open('tarefas.json', 'w') as tf:
        json.dump(tarefas_py, tf, indent=2)
        return redirect('/')










if __name__ == '__main__':
    app.run(debug=True)

