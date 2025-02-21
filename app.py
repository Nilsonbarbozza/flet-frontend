import flet as ft
import requests

API_BASE_URL = "http://localhost:8000/api"

def main(page: ft.Page):
    page.title = "Area de Cadastro"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.colors.WHITE
    page.margin= ft.margin.only(left=16, top=20, right=16, bottom=20)

    #Tab - Criar aluno
    nome_field = ft.TextField(label="Nome", label_style= ft.TextStyle(size=12, color="black"), border_radius=10)
    email_field = ft.TextField(label="Email",label_style= ft.TextStyle(size=12, color="black"), border_radius=10)
    faixa_field = ft.TextField(label="Faixa",label_style= ft.TextStyle(size=12, color="black"), border_radius=10)
    data_nascimento_field = ft.TextField(label="Data nascimento (yyyy-mm-aaa)",label_style= ft.TextStyle(size=12, color="black"), border_radius=10)
    create_result = ft.Text()
    container = ft.Container(height=8)

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

    create_button = ft.ElevatedButton(
        text="Enviar", height=40, width=100, bgcolor=ft.colors.BLUE_600, color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12),
        padding=ft.padding.symmetric(horizontal=20, vertical=14),
        overlay_color=ft.colors.BLUE_600,
        elevation=4,), on_click=criar_aluno_click) 

    criar_tabela_aluno = ft.Column(
        [   container,
            nome_field,
            email_field,
            faixa_field,
            data_nascimento_field,
            create_button,
            create_result
            
        ], scroll=True
    )

    #Tab - Listar alunos   
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
            
    list_button = ft.ElevatedButton(
        text="Listar Alunos", height=40, width=200, bgcolor=ft.colors.BLUE_600, color="white",style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=ft.padding.symmetric(horizontal=20, vertical=14),
        overlay_color=ft.colors.BLUE_600,
        elevation=4,), on_click=listar_alunos_click )
    
    container = ft.Container(height=8)
    list_result = ft.Text()
    listar_alunos_tab = ft.Column([container, students_table, list_button, list_result], scroll=True)

    #Tab - Registrar aulas   
    email_aula_field = ft.TextField(label="Email Aluno",label_style= ft.TextStyle(size=12, color="black"), border_radius=10)
    qtd_field = ft.TextField(label="Quantidade de aula", value=1,label_style= ft.TextStyle(size=12, color="black"), border_radius=10)
    aula_result = ft.Text()
    container = ft.Container(height=8)

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

    aula_button = ft.ElevatedButton(
        text="Registrar", height=40, width=100, bgcolor=ft.colors.BLUE_600, color="white",style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=ft.padding.symmetric(horizontal=20, vertical=14),
        overlay_color=ft.colors.BLUE_600,
        elevation=4,), on_click=marca_aula)
    
    aula_tab = ft.Column([container, email_aula_field, qtd_field, aula_button,aula_result], scroll=True)

    #Tab - Progresso 
    email_progress_field = ft.TextField(label="Email-Aluno",label_style= ft.TextStyle(size=12, color="black"), border_radius=10)
    progress_aluno_field = ft.Text()

    def progress_click(e):
        container = ft.Container(height=8)
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

    progress_button = ft.ElevatedButton(
        text="Ver progresso", height=40, width=200, bgcolor=ft.colors.BLUE_600, color="white",style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=ft.padding.symmetric(horizontal=20, vertical=14),
        overlay_color=ft.colors.BLUE_600,
        elevation=4,), on_click=progress_click)
    
    progress_tab = ft.Column([container, email_progress_field,progress_button, progress_aluno_field ], scroll=True)

    #Tab - Atualizar Aluno 
    container = ft.Container(height=8)
    id_aluno_field = ft.TextField(label="ID do Aluno",label_style= ft.TextStyle(size=12, color="black"), border_radius=10)
    nome_update_field = ft.TextField(label="Novo Nome",label_style= ft.TextStyle(size=12, color="black"), border_radius=10)
    email_update_field = ft.TextField(label="Novo Email",label_style= ft.TextStyle(size=12, color="black"), border_radius=10)
    faixa_update_field = ft.TextField(label="Nova Faixa",label_style= ft.TextStyle(size=12, color="black"), border_radius=10)
    data_nascimento_update_field = ft.TextField(label="Nova Data de Nascimento (YYYY-MM-DD)",label_style= ft.TextStyle(size=12, color="black"), border_radius=10)
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

    update_button = ft.ElevatedButton(
        text="Atualizar Aluno", height=40, width=200, bgcolor=ft.colors.BLUE_600, color="white",style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=ft.padding.symmetric(horizontal=20, vertical=14),
        overlay_color=ft.colors.BLUE_600,
        elevation=4,), on_click=atualizar_aluno_click)
    
    atualizar_tab = ft.Column(
        [   container,
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

    #Tab - Deletar aluno  
    container = ft.Container(height=8)
    id_aluno_field = ft.TextField(label="ID do aluno a deletar",label_style= ft.TextStyle(size=12, color="black"), border_radius=10)
    email_aluno_field = ft.TextField(label="Email",label_style= ft.TextStyle(size=12, color="black"), border_radius=10)
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

    delet_button = ft.ElevatedButton(
        text="Deletar", height=40, width=100, bgcolor=ft.colors.RED, color="white",style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=ft.padding.symmetric(horizontal=20, vertical=14),
        overlay_color=ft.colors.BLUE_600,
        elevation=4,), on_click=delete_aluno)
    
    delet_tab = ft.Column([container, id_aluno_field, email_aluno_field, delet_button,result_delet], scroll=True)
    
    #Navegação tabs
    tabs = ft.Tabs(
        selected_index = 0,
        animation_duration= 300,
        expand=True,  # Faz com que as tabs ocupem toda a largura
        indicator_color="blue",  # Cor do indicador da aba selecionada
        divider_color="transparent",  # Remove a linha divisória
    
        tabs=[
            ft.Tab(text="Cadastro", icon=ft.icons.PERSON_ADD, content=criar_tabela_aluno),
            ft.Tab(text="Alunos", icon=ft.icons.GROUP, content=listar_alunos_tab),
            ft.Tab(text="Concluida", icon=ft.icons.CHECK_CIRCLE, content=aula_tab),
            ft.Tab(text="Progresso", icon=ft.icons.TRENDING_UP, content=progress_tab),
            ft.Tab(text="Atualizar", icon=ft.icons.EDIT, content=atualizar_tab),
            ft.Tab(text="Deletar", icon=ft.icons.DELETE,  content=delet_tab),
        ]
    )
    
    page.add(tabs)

if __name__ == "__main__":
    ft.app(target=main)
