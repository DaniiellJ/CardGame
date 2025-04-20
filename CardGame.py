import random
import time
import tkinter as tk
from tkinter import ttk, messagebox

class JogoCartas:
    def __init__(self, janela_principal):
        #janela inicial
        self.janela = janela_principal
        self.janela.title("Jogo de Ordenar Cartas")
        self.janela.geometry("650x650")
        
        #configuração das Cartas
        self.naipes = {0: '♣', 1: '♥', 2: '♠', 3: '♦'}
        self.valores_especiais = {1: 'A', 11: 'Q', 12: 'J', 13: 'K'}
        
        #tela inicial do jogo
        self.pontuacao = 100
        self.passo_atual = 0
        self.baralho = []
        self.tempo_inicio = 0
        self.tempo_decorrido = 0
        self.cronometro_rodando = False
        self.colunas_baralho = 10
        self.colunas_selecao = 8
        
        #estilo visual
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')
        self.configurar_estilos()
        self.mostrar_tela_inicial()

    def configurar_estilos(self):
        self.estilo.configure('Titulo.TLabel', 
                            font=('Arial', 16, 'bold'), 
                            foreground='#2E3440')
        self.estilo.configure('BotaoCarta.TButton', 
                            font=('Arial', 12, 'bold'),
                            padding=5,
                            width=5)
        self.estilo.map('BotaoCarta.TButton',
                      foreground=[('active', '#88C0D0')],
                      background=[('active', '#434C5E')])
        self.estilo.configure('Tempo.TLabel', 
                            font=('Arial', 12),
                            foreground='#4C566A')

    def mostrar_tela_inicial(self):
        self.tela_inicial = ttk.Frame(self.janela)
        self.tela_inicial.pack(expand=True, fill='both')
        
        ttk.Label(self.tela_inicial, 
                text="Bem-vindo ao Jogo de Ordenação de Cartas!", 
                style='Titulo.TLabel').pack(pady=20)
        
        regras = [
            "Como Jogar:",
            "1. Ordene as cartas primeiro por VALOR (1-13)",
            "2. Para valores iguais, ordene por NAIPE: ♣ < ♥ < ♠ < ♦",
            "3. Selecione a próxima carta correta para cada posição",
            "4. Acertos: +10 pontos | Erros: -15 pontos",
            "5. O cronômetro começa quando você inicia o jogo!",
            "\nDica: Cartas ordenadas aparecem em verde!"
        ]
        
        for texto in regras:
            ttk.Label(self.tela_inicial, text=texto, font=('Arial', 12)).pack(pady=2)
        
        ttk.Button(self.tela_inicial, text="Iniciar Jogo", command=self.iniciar_jogo).pack(pady=30)

    def iniciar_jogo(self):
        self.tela_inicial.destroy()
        self.criar_interface_jogo()
        self.novo_jogo()

    def criar_interface_jogo(self):
        self.principal = ttk.Frame(self.janela)
        self.principal.pack(expand=True, fill='both', padx=20, pady=10)
        
        self.criar_painel_superior()
        self.area_baralho = ttk.Frame(self.principal)
        self.area_baralho.pack(expand=True, fill='both', pady=10)
        
        self.label_status = ttk.Label(self.principal, text="", font=('Arial', 11))
        self.label_status.pack(pady=5)
        
        self.area_selecao = ttk.Labelframe(self.principal, 
             text="Selecione a Próxima Carta", padding=10)
        self.area_selecao.pack(fill='both', pady=10)

    def criar_painel_superior(self):
        painel_superior = ttk.Frame(self.principal)
        painel_superior.pack(fill='x', pady=5)

        botoes_frame = ttk.Frame(painel_superior)
        botoes_frame.pack(side='right')

        #restart
        ttk.Button(botoes_frame, text="Reiniciar", command=self.novo_jogo).pack(side='left', padx=5)
        
        #pontuação e passo
        painel_esquerda = ttk.Frame(painel_superior)
        painel_esquerda.pack(side='left', expand=True)
        
        ttk.Label(painel_esquerda, text="Pontuação:", font=('Arial', 12)).pack(side='left')
        self.label_pontuacao = ttk.Label(painel_esquerda, text="100", font=('Arial', 12, 'bold'))
        self.label_pontuacao.pack(side='left', padx=10)
        
        ttk.Label(painel_esquerda, text="Passo Atual:", font=('Arial', 12)).pack(side='left')
        self.label_passo = ttk.Label(painel_esquerda, text="0", font=('Arial', 12, 'bold'))
        self.label_passo.pack(side='left')
        
        #tempo e ajuda
        painel_direita = ttk.Frame(painel_superior)
        painel_direita.pack(side='right')
        
        ttk.Label(painel_direita, text="Tempo:", style='Tempo.TLabel').pack(side='left')
        self.label_tempo = ttk.Label(painel_direita, text="00:00", font=('Arial', 12, 'bold'))
        self.label_tempo.pack(side='left', padx=10)
        
        ttk.Button(botoes_frame, text="Ajuda", command=self.mostrar_ajuda).pack(side='left', padx=5)

    def novo_jogo(self):
        #novo jogo (zera o cronometro e embaralha novamente)
        self.parar_cronometro()
        self.baralho = [(valor, naipe) for valor in range(1, 14) for naipe in range(4)]
        random.shuffle(self.baralho)
        
        self.pontuacao = 100
        self.passo_atual = 0
        self.tempo_decorrido = 0
        self.label_status.config(text="")
        self.atualizar_interface()
        self.iniciar_cronometro()
        self.label_tempo.config(text="00:00")

    def iniciar_cronometro(self):
        self.tempo_inicio = time.time()
        self.cronometro_rodando = True
        self.atualizar_tempo()

    def atualizar_tempo(self):
        if self.cronometro_rodando:
            self.tempo_decorrido = time.time() - self.tempo_inicio
            minutos = int(self.tempo_decorrido // 60)
            segundos = int(self.tempo_decorrido % 60)
            
            self.label_tempo.config(text=f"{minutos:02d}:{segundos:02d}")
            self.janela.after(1000, self.atualizar_tempo)

    def parar_cronometro(self):
        self.cronometro_rodando = False

    def converter_carta(self, carta):
        """Converte valores numéricos para símbolos"""
        valor, naipe = carta
        valor_str = self.valores_especiais.get(valor, str(valor))
        return f"{valor_str}{self.naipes[naipe]}"

    def encontrar_menor_carta(self, cartas):
        """Encontra a posição da menor carta na lista"""
        posicao_menor = 0
        for i in range(1, len(cartas)):
            if (cartas[i][0] < cartas[posicao_menor][0]) or \
               (cartas[i][0] == cartas[posicao_menor][0] and 
                cartas[i][1] < cartas[posicao_menor][1]):
                posicao_menor = i
        return posicao_menor

    def atualizar_interface(self):
        for widget in self.area_baralho.winfo_children():
            widget.destroy()
        for widget in self.area_selecao.winfo_children():
            widget.destroy()
        
        self.label_pontuacao.config(text=str(self.pontuacao))
        self.label_passo.config(text=str(self.passo_atual + 1))
        
        #baralho atual
        for indice in range(self.passo_atual):
            carta = self.baralho[indice]
            linha = indice // self.colunas_baralho
            coluna = indice % self.colunas_baralho
            
            frame = ttk.Frame(self.area_baralho, padding=2)
            frame.grid(row=linha, column=coluna, padx=2, pady=2)
            
            ttk.Label(frame, 
                    text=self.converter_carta(carta),
                    font=('Arial', 10),
                    background='#A3BE8C',
                    width=5,
                    anchor='center').pack()
        
        cartas_restantes = self.baralho[self.passo_atual:]
        posicao_correta = self.encontrar_menor_carta(cartas_restantes)
        
        #botões para seleção
        for indice, carta in enumerate(cartas_restantes):
            linha = indice // self.colunas_selecao
            coluna = indice % self.colunas_selecao
            
            botao = ttk.Button(self.area_selecao,
                             text=self.converter_carta(carta),
                             style='BotaoCarta.TButton',
                             command=lambda i=indice: self.verificar_jogada(i, posicao_correta))
            botao.grid(row=linha, column=coluna, padx=5, pady=2, sticky='w')

    def mostrar_feedback(self, mensagem, cor):
        self.label_status.config(text=mensagem, foreground=cor)
        self.janela.after(2000, lambda: self.label_status.config(text=""))

    def verificar_jogada(self, escolha, resposta_correta):
        if escolha == resposta_correta:
            self.pontuacao += 10
            self.mostrar_feedback("✓ Correto! +10 pontos", '#2E8B57')
            self.label_pontuacao.config(foreground='#2E8B57')
        else:
            self.pontuacao -= 15
            carta_correta = self.converter_carta(self.baralho[self.passo_atual + resposta_correta])
            self.mostrar_feedback(f"✗ Errado! Carta correta: {carta_correta} (-15 pontos)", '#B22222')
            self.label_pontuacao.config(foreground='#B22222')
        
        self.janela.after(2000, lambda: self.label_pontuacao.config(foreground='black'))
        
        #move a carta escolhida para a posição atual
        self.baralho[self.passo_atual], self.baralho[self.passo_atual + resposta_correta] = \
            self.baralho[self.passo_atual + resposta_correta], self.baralho[self.passo_atual]
        
        self.passo_atual += 1
        
        #embaralha cartas restantes após cada jogada
        if self.passo_atual < len(self.baralho):
            restantes = self.baralho[self.passo_atual:]
            random.shuffle(restantes)
            self.baralho[self.passo_atual:] = restantes
        
        #verifica se o jogo terminou
        if self.passo_atual >= len(self.baralho):
            self.parar_cronometro()
            minutos = int(self.tempo_decorrido // 60)
            segundos = int(self.tempo_decorrido % 60)
            messagebox.showinfo("Fim do Jogo", 
                              f"🎉 Parabéns!\nPontuação final: {self.pontuacao}\nTempo: {minutos:02d}:{segundos:02d}")
            self.novo_jogo()
        else:
            self.atualizar_interface()

    def mostrar_ajuda(self):
        texto_ajuda = """Regras do Jogo:
        
• Objetivo: Ordenar o baralho primeiro por valor, depois por naipe
• Ordem dos valores: 1 (A) < 2 < 3 < ... < 13 (K)
• Ordem dos naipes: ♣ (Paus) < ♥ (Copas) < ♠ (Espadas) < ♦ (Ouros)
• Selecione sempre a menor carta restante
• Cartas já ordenadas aparecem em verde
• Pontuação inicial: 100 pontos
• Acerto: +10 pontos | Erro: -15 pontos
• O cronômetro começa automaticamente"""
        messagebox.showinfo("Ajuda", texto_ajuda)

if __name__ == "__main__":
    janela_principal = tk.Tk()
    jogo = JogoCartas(janela_principal)
    janela_principal.mainloop()