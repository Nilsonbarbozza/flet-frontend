import flet as ft
import requests

API_BASE_URL = "http://localhost:8000/api"

def main(page: ft.Page):
    page.title = "PageTeste"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER


    #Campo da aplicação
    nome_field = ft.TextField(label="Nome")
    email_field = ft.TextField(label="email")
    faixa_field = ft.TextField(label="faixa")
    data_nascimento_field = ft.TextField(label="Data nascimento (yyyy-mm-aaa)")
    create_result = ft.Text()

    #Criar a função de orientação a evento
    def criar_aluno_click(e):

        payload = {
            "nome": nome_field.value,
            "email": email_field.value,
            "faixa": faixa_field.value,
            "data_nascimento": data_nascimento_field.value
        }
        response = requests.post(API_BASE_URL + '/', json=payload)

        if response.status_code == 200:
            aluno = response.json()
            create_result.value = f'Aluno criado{aluno}'
        else:
            create_result.value = f'Error ao criar aluno{response.text}'
        
        page.update()

    create_button = ft.ElevatedButton(text="Cadastrar", on_click=criar_aluno_click) 


    #Cria uma page Container colunas
    criar_tabela_aluno = ft.Column(
        [
            nome_field,
            email_field,
            faixa_field,
            data_nascimento_field,
            create_result,
            create_button
        ], scroll=True
    )

    #Listar alunos - funcionalidade
    #Criar uma tabela de exibição
    students_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('NOME')),
            ft.DataColumn(ft.Text('EMAIL')),
            ft.DataColumn(ft.Text('FAIXA')),
            ft.DataColumn(ft.Text('DATA NASCIMENTO')),
        ],
        rows=[]
    )

    def listar_alunos_click(e):
        payload = {
            "nome": nome_field.value,
            "email": email_field.value,
            "faixa": faixa_field.value,
            "data_nascimento": data_nascimento_field.value
        }

        response = requests.get(API_BASE_URL + '/alunos/', json=payload)
        alunos = response.json()

        students_table.rows.clear()
        for aluno in alunos:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(aluno.get('nome'))),
                    ft.DataCell(ft.Text(aluno.get('email'))),
                    ft.DataCell(ft.Text(aluno.get('faixa'))),
                    ft.DataCell(ft.Text(aluno.get('data_nascimento'))),
                ]
            )
            students_table.rows.append(row)
            list_result.value = f"{len(alunos)} alunos encontrados"
            page.update()

    list_result = ft.Text()
    list_button = ft.ElevatedButton(text="Listar Alunos", on_click=listar_alunos_click )
    listar_alunos_tab = ft.Column([students_table, list_result, list_button], scroll=True)

    #Registrar aula
    email_aula_field = ft.TextField(label="Email Aluno")
    qtd_field = ft.TextField(label="Quantidade de aula", value=1)
    aula_result = ft.Text()

    def marca_aula(e):
        payload = {
            'qtd': int(qtd_field.value),
            'email_aluno': email_aula_field.value,
        }

        response = requests.post(API_BASE_URL + '/aula_realizada/', json=payload)
        if response.status_code == 200:
            aula_result.value = f"Aula cadastrada{response.json()}"
        else:
            aula_result.value = f"Error: {response.text}" 
        
        page.update()

    aula_button = ft.ElevatedButton(text="Registrar", on_click=marca_aula)
    aula_tab = ft.Column([email_aula_field, qtd_field, aula_result, aula_button], scroll=True)

    #

    #criar uma navegação entre tabs
    tabs = ft.Tabs(
        selected_index = 0,
        animation_duration= 300,

        tabs=[
            ft.Tab(text="Cadastro", content=criar_tabela_aluno),
            ft.Tab(text="Alunos", content=listar_alunos_tab),
            ft.Tab(text="Aulas Concluida", content=aula_tab)
        ]
    )

    page.add(tabs)

if __name__ == "__main__":
    ft.app(target=main)
