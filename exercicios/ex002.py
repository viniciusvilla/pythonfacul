lista = []

def principal():
    print("Sistema de registro de notas - Instituição Fortnelson\n")
    print('Cadastro de novo aluno')
    cadastro()
    exibir_lista()
   

def cadastro():
    n = int(input('Digite a quantidade de alunos que serão cadastrados: '))
    for i in range(n):
        matricula = '000'+str(i+1)
        print('')
        print(f'Cadastro aluno {matricula}')
        nome = input('Digite o nome do aluno: ')
        print('Informe o curso desejado:\n')
        curso = input('1 - TI\n2 - ADM\n3 - PEDAG\n\nCURSO: ')
        turma = input('Código da turma: ')
    
        aluno = [nome,curso,turma,matricula]
        lista.append(aluno)
        
def exibir_lista():
    for aluno in lista:
        print(aluno)
        
principal()

        
    
    
    
    
    
