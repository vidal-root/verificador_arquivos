import os
import time
from datetime import datetime, timedelta
import PySimpleGUI as sg
from model.appDAO import appDAO

class VerificadorArquivos:

    def __init__(self):
        self.arquivos = []
        self.arr_historico = []
        self.nm_theme = None
        self.janela = None
        self.appDAO = appDAO()
        self.carrega_config()
        self.iniciar()

    def carrega_config(self):
        nm_tema = self.appDAO.select_tema()
        if not nm_tema:
            self.nm_theme = 'SystemDefault'
        else:
            self.nm_theme = nm_tema[0][0]

        self.carrega_historico()

    def carrega_historico(self, nm_caminho=''):
        if nm_caminho != '':
            self.appDAO.insert_historico(nm_caminho)
        arr_historico = self.appDAO.select_historico()

        for path in arr_historico:
            self.arr_historico.append(path[1])

    def deletar_historico(self):
        self.appDAO.deletar_historico()

    def iniciar(self):
        self.janela = self.layout()
        while True:
            button, values = self.janela.Read()

            if button == sg.WIN_CLOSED:
                print('oi')
                break

            self.acoes_btn(button, values)

            self.janela['output'].update('')
            self.arquivos = []
            try:
                fl_ultima_hora = values['fl_ultima_hora']
                nm_dir = values['nm_dir']
                nr_horas = ''

                if fl_ultima_hora == True:
                    self.janela['col1'].update(visible=True)
                    nr_horas = values['nr_horas']
                else:
                    self.janela['nr_horas'].update('')
                    self.janela['col1'].update(visible=False)

                if button == 'btn_gerar' or button == 'btn_visualizar':
                    if nr_horas != '':
                        minutos = int(nr_horas) * 60
                        data_seach = datetime.today() - timedelta(minutes=minutos)

                    root = f"{nm_dir}"
                    if root != '' and root:
                        self.arr_historico = []
                        self.carrega_historico(root)
                        self.janela['nm_dir'].update(values=self.arr_historico, size=(85, 25), value=root)

                    count_arquivos = 0
                    for diretorio, subpastas, arquivos in os.walk(root):
                        for arquivo in arquivos:
                            nm_arquivo = os.path.join(diretorio, arquivo)
                            c_time = os.path.getmtime(nm_arquivo)
                            local_time = time.ctime(c_time)
                            data_modificacao = datetime.strptime(local_time, "%a %b %d %H:%M:%S %Y")
                            if fl_ultima_hora == True:
                                if data_modificacao > data_seach:
                                    count_arquivos = count_arquivos + 1
                                    if button == 'btn_visualizar':
                                        print(nm_arquivo)
                                    if button == 'btn_gerar':
                                        self.arquivos.append(nm_arquivo)
                            else:
                                count_arquivos = count_arquivos + 1
                                if button == 'btn_visualizar':
                                    print(nm_arquivo)
                                if button == 'btn_gerar':
                                    self.arquivos.append(nm_arquivo)

                    if self.arquivos:
                        nm_arquivo = self.gerar_arquivo()
                        print('Arquivo gerado com sucesso em ' + nm_arquivo)

                    if count_arquivos == 0:
                        self.janela['nr_total'].update('0')
                        print('Nenhum arquivo foi modificado neste diretório!')
                    else:
                        self.janela['nr_total'].update(count_arquivos)

            except Exception as e:
                print('Ocorreu um erro! Informações do Erro:')
                print(e)
                continue

        self.janela.close()

    def acoes_btn(self, button, values):
        if button == 'nm_theme':
            self.janela.close()
            self.nm_theme = values['nm_theme']
            self.appDAO.insert_tema(self.nm_theme)
            self.iniciar()

        if button == 'btn_limpar_tela':
            self.janela.close()
            self.iniciar()

        if button == 'btn_delete_historico':
            self.arr_historico = []
            self.deletar_historico()
            self.janela['nm_dir'].update(values=self.arr_historico, size=(85, 25))

    def input_usuario(self):
        opcao = int(
            input("[1] - Todos os arquivos de um diretório\n[2] - Arquivos com modificações nas últimas horas\n"))
        root_alvo = input('Informe o caminho da pasta, ex: "C:\\Users\\vidal_root\\Documents": ')
        qtd_horas = ''
        if opcao == 2:
            qtd_horas = input("Informe a quantidade de horas atrás: ")

        arr = [root_alvo, qtd_horas]

        return arr

    def apresentacao(self):
        ds_apresentacao = """Este programa gera um txt dos arquivos modi\nEscolha uma opção:"""
        print(ds_apresentacao)

    def layout(self):

        sg.theme(self.nm_theme)

        col = [[sg.Radio('Arquivos com modificações nas últimas horas', 'op', enable_events=True, default=True,
                         key='fl_ultima_hora'),
                sg.Radio('Todos os arquivos de um diretório', 'op', enable_events=True, key='fl_todos')]]

        col1 = [[sg.Text('Qtd. Horas', size=(8, 0), key='nm_input_horas'),
                 sg.Combo(values=list(range(1, 9999)), size=(8, 24), default_value=1, key='nr_horas')]]

        col2 = [[sg.Text('Caminho', size=(6, 0)), sg.Combo(values=self.arr_historico, size=(85, 25), key='nm_dir')]]

        col3 = [[sg.Button('Visualizar arquivos', key='btn_visualizar'), sg.Button('Gerar txt', key='btn_gerar')]]

        col3_1 = [[sg.Text('Total de arquivos: ', size=(13, 0)), sg.Text('0', size=(20, 0), key='nr_total')]]

        col4 = [[sg.Output(size=(120, 15), key='output')]]

        col5 = [[sg.Text('Escolher tema: ', size=(12, 0)),
                 sg.Combo(values=sg.theme_list(), size=(30, 24), default_value=sg.theme(), enable_events=True,
                          key='nm_theme'), sg.Button('Limpar tela', size=(30, 0), key='btn_limpar_tela'),
                 sg.Button('Limpar histórico', size=(30, 0), key='btn_delete_historico')]]

        layout_app = [
            [sg.Column(col, element_justification='c')],
            [sg.Column(col2, element_justification='c'),
             sg.Column(col1, element_justification='c', key='col1')],
            [sg.Column(col3, element_justification='c')],
            [sg.Column(col3_1, element_justification='c')],
            [sg.Column(col4, element_justification='c')],
            [sg.Column(col5, element_justification='c')],
        ]

        janela = sg.Window('Verificador de Arquivos').layout(layout_app)

        return janela

    def gerar_arquivo(self):
        data = datetime.now()
        data_geracao = data.strftime("%d%m%Y_%H%M%S")
        nm_arquivo = os.getcwd() + os.sep + 'arquivos_modificados_' + data_geracao + '.txt'
        for arquivo_modificado in self.arquivos:
            with open(nm_arquivo, 'a', newline='',
                      encoding='utf-8') as arquivo:
                arquivo.write(arquivo_modificado + os.linesep)

        return nm_arquivo


app = VerificadorArquivos()
