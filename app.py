import flet as ft
import requests

API_BASE_URL = "http://localhost:8000/api"

def main(page: ft.Page):
    page.title = "PageTeste"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER


    #Campo da aplicaçã
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
            create_result.color = "green"
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
            list_result.color = "green"
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
            aula_result.color = "green"
        else:
            aula_result.value = f"Error: {response.text}" 
        
        page.update()

    aula_button = ft.ElevatedButton(text="Registrar", on_click=marca_aula)
    aula_tab = ft.Column([email_aula_field, qtd_field, aula_result, aula_button], scroll=True)

    #Progresso aluno
    email_progress_field = ft.TextField(label="Email-Aluno")
    progress_aluno_field = ft.Text()

    

    def progress_click(e):
        email = email_progress_field.value
        response = requests.get(API_BASE_URL + '/progresso_aluno/', params={'email_aluno':email})

        if response.status_code == 200:
            progress = response.json()
            progress_aluno_field.value = (
            f"Nome:{progress.get('nome')}\n"
            f"Email:{progress.get('email')}\n"
            f"Faixa:{progress.get('faixa')}\n"
            f"Aulas:{progress.get('total_aulas')}\n"
            f"Aulas Necessaria para proxima faixa:{progress.get('aulas_necessarios_para_proxima_faixa')}\n"
            )
            progress_aluno_field.color = "green"
        else:
            progress_aluno_field.value = "Error404"

        page.update()

    progress_button = ft.ElevatedButton(text="Ver progresso", on_click=progress_click)
    progress_tab = ft.Column([email_progress_field,progress_aluno_field,progress_button ], scroll=True)


    id_aluno_field = ft.TextField(label="ID do Aluno")
    nome_update_field = ft.TextField(label="Novo Nome")
    email_update_field = ft.TextField(label="Novo Email")
    faixa_update_field = ft.TextField(label="Nova Faixa")
    data_nascimento_update_field = ft.TextField(label="Nova Data de Nascimento (YYYY-MM-DD)")
    update_result = ft.Text()

    def atualizar_aluno_click(e):
        try:
            aluno_id = id_aluno_field.value
            if not aluno_id:
                update_result.value = "ID do aluno é necessário."
                update_result.color = "red"
            else:
                payload = {
                    "nome": nome_update_field.value,
                    "email": email_aula_field.value,
                    "faixa": faixa_update_field.value,
                    "data_nascimento": data_nascimento_field.value,
                }

                response = requests.put(API_BASE_URL + f"/alunos/{aluno_id}", json=payload)
                print(response)
                if response.status_code == 200:
                    aluno = response.json()
                    update_result.value = f"Aluno atualizado: {aluno}"
                    update_result.color = "green"
                else:
                    update_result.value = f"Erro: {response.text}"
        except Exception as ex:
            update_result.value = f"Exceção: {ex}"

        page.update()

    update_button = ft.ElevatedButton(text="Atualizar Aluno", on_click=atualizar_aluno_click)
    atualizar_tab = ft.Column(
        [
            id_aluno_field,
            nome_update_field,
            email_update_field,
            faixa_update_field,
            data_nascimento_update_field,
            update_button,
            update_result,
        ],
        scroll=True,
    )


    # Deletar usuário
    id_aluno_field = ft.TextField(label="ID do aluno a deletar")
    email_aluno_field = ft.TextField(label="E-mail")
    result_delet = ft.Text(color="red")  # Exibir erros em vermelho

    def delete_aluno(e):
        aluno_id2 = id_aluno_field.value
        email = email_aluno_field.value

        if not aluno_id2 or email:
            result_delet.value = "Preencha todos os campos!"
            page.update()
            return

        try:
            response = requests.delete(
                f"{API_BASE_URL}/delete/{aluno_id2}",
                params={"email_aluno": email}
            )

            if response.status_code == 200:
                result_delet.value = "Usuário excluído com sucesso!"
                result_delet.color = "green"
                id_aluno_field.visible = False
                email_aluno_field.visible = False
                delet_button.visible = False
            elif response.status_code == 404:
                result_delet.value = "Usuário não encontrado!"
            else:
                result_delet.value = f"Erro ao excluir: {response.text}"
        except requests.exceptions.RequestException as err:
            result_delet.value = f"Erro de conexão: {err}"

        page.update()

    delet_button = ft.ElevatedButton(text="Deletar", on_click=delete_aluno)
    delet_tab = ft.Column([id_aluno_field, email_aluno_field, result_delet, delet_button], scroll=True)
    


    #criar uma navegação entre tabs
    tabs = ft.Tabs(
        selected_index = 0,
        animation_duration= 300,

        tabs=[
            ft.Tab(text="Cadastro", content=criar_tabela_aluno),
            ft.Tab(text="Alunos", content=listar_alunos_tab),
            ft.Tab(text="Concluida", content=aula_tab),
            ft.Tab(text="Progresso", content=progress_tab),
            ft.Tab(text="Atualizar", content=atualizar_tab),
            ft.Tab(text="Deletar", content=delet_tab, ),
        ]
    )

    page.add(tabs)

if __name__ == "__main__":
    ft.app(target=main)
