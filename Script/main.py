# ===================== BIBLIOTECAS
import pandas as pd
from tkinter import Tk, Checkbutton, Button, Frame, IntVar, Canvas, Scrollbar, Entry, StringVar
from tkinter.filedialog import askdirectory
from os import listdir
from os.path import isfile, join, splitext
import messagebox

# ===================== SCRIPT
print('\nSelecione a pasta que contém os arquivos a serem lidos.')
pasta = askdirectory(title='Selecione a pasta que contém os arquivos.')
arquivos = [f for f in listdir(pasta) if isfile(join(pasta, f))]

arquivos_selecionados = []

# Cria a janela para seleção dos arquivos
root = Tk()
root.title('Selecione os arquivos')
root.attributes('-topmost', True)
root.deiconify()
root.lift()
root.focus_force() 

def centralizar_janela():
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (w // 2)
    y = (screen_height // 2) - (h // 2)
    root.geometry(f'+{x}+{y}')

root.after(10, centralizar_janela)

# Cria os elementos da janela
check_items = []
checkbox_widgets = []
selecionar_tudo = False

def atualizar_filtro(*args):
    texto_pesquisado = var_pesquisa.get().lower()
    for i, nome_arquivo in enumerate(arquivos):
        widget = checkbox_widgets[i]
        if texto_pesquisado in nome_arquivo.lower():
            widget.pack(fill='x', anchor='w')
        else:
            widget.pack_forget()

def selecionar():
    global arquivos_selecionados
    arquivos_selecionados = [
        nome for nome, var in zip(arquivos, check_items) if var.get() == 1]
    root.destroy()

def toggle_all():
    global selecionar_tudo
    selecionar_tudo = not selecionar_tudo
    new_val = 1 if selecionar_tudo else 0

    for var, cb in zip(check_items, checkbox_widgets):
        if cb.winfo_viewable():
            var.set(new_val)

    toggle_btn.config(
        text='Deselecionar tudo' if selecionar_tudo else 'Selecionar tudo'
    )

top_frame = Frame(root)
top_frame.pack(side='top', fill='x')

var_pesquisa = StringVar()
var_pesquisa.trace_add('write', atualizar_filtro)  # Live filter
search_entry = Entry(top_frame, textvariable=var_pesquisa)
search_entry.pack(fill='x', padx=5, pady=5)

middle_frame = Frame(root)
middle_frame.pack(fill='both', expand=True)

bottom_frame = Frame(root)
bottom_frame.pack(side='bottom', fill='x')

# Toggle Button
toggle_btn = Button(top_frame, text='Selecionar todos', command=toggle_all, width=20)
toggle_btn.pack(pady=5)

# Opções (Scrollable)
canvas = Canvas(middle_frame)
scrollbar = Scrollbar(middle_frame, orient='vertical', command=canvas.yview)
scrollable_frame = Frame(canvas)

scrollable_frame.bind(
    '<Configure>',
    lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')

# Lista e botões de seleção
for nome_arquivo in arquivos:
    var = IntVar(value=0)
    check_items.append(var)
    cb = Checkbutton(scrollable_frame, text=nome_arquivo, variable=var, anchor='w')
    cb.pack(fill='x', anchor='w')
    checkbox_widgets.append(cb)

# Botão de confirmação
ok_btn = Button(bottom_frame, text='OK', command=selecionar, width=20)
ok_btn.pack(pady=10)

root.mainloop()


# Lê e concatena os arquivos selecionados
print(f'\n{len(arquivos_selecionados)} arquivos selecionados. Iniciando leitura...')


def read_csv(path):
    for sep in [';', ',']:
        try:
            df = pd.read_csv(path, sep=sep, encoding='utf-8')
            if df.shape[1] > 1:
                return df
        except Exception:
            continue
    raise ValueError('Falha ao ler o CSV com separadores ";" e ","')

readers = {
    '.xlsx': pd.read_excel,
    '.csv': read_csv
}

arquivos_concatenados = []
arquivos_ignorados = []

for nome_arquivo in arquivos_selecionados:
    caminho_arquivo = join(pasta, nome_arquivo)
    _, extensao = splitext(nome_arquivo)
    extensao = extensao.lower()

    try:
        if extensao in readers:
            df = readers[extensao](caminho_arquivo)
            arquivos_concatenados.append(df)
        else:
            arquivos_ignorados.append(nome_arquivo)
            print(f'Formato de arquivo {extensao} não suportado, ignorando {nome_arquivo}.')
    except Exception as e:
        print(f'Erro ao ler {nome_arquivo}.\nLog do erro: {e}')

if arquivos_ignorados:
    messagebox.showwarning('Arquivos Ignorados',f'Os seguintes arquivos foram ignorados por conterem uma extensão não suportada pelo programa:\n\n' + '\n'.join(arquivos_ignorados))

arquivos_concatenados = pd.concat(arquivos_concatenados)
arquivos_concatenados.to_excel('saida.xlsx', index=False)
print(f'Arquivos concatenados com sucesso. Total de {len(arquivos_concatenados)} linhas. Resultado salvo em "saida.xlsx".')