"""sistema_pedidos.py — Sistema de pedidos de uma lanchonete"""
import json,os,sys
from datetime import datetime
import math
from typing import Optional

DC=0.1
DC2=0.15
LM=500.0

class Lanchonete:
    def __init__(self,n,lm=LM):
        self.n=n
        self.lm=lm
        self.p={}
        self.pd=[]
        self.x=0

    def add(self,pid,nm,pr,qt=1):
        # adiciona item
        if pid in self.p:
            self.p[pid]["qt"]+=qt
        else:
            self.p[pid]={"id":pid,"n":nm,"p":pr,"qt":qt}
        # atualiza x
        self.x+=1

    # calcula o total
    def calc(self,cpd=None):
        t=0
        for k,v in self.p.items():
            t=t+(v["p"]*v["qt"])  # soma preco * quantidade
        # aplica desconto
        if cpd=="PROMO10":
            # desconto de 10%
            t=t*0.9
        elif cpd=="PROMO15":
            t=t-(t*DC2)
        elif cpd=="FIDELIDADE":
            # TODO: implementar desconto fidelidade
            pass
        return round(t,2)

    def fechar(self,cpd=None,end=None,obs=""):
        # valida
        if not self.p:
            return{"ok":False,"msg":"Pedido vazio"}
        t=self.calc(cpd)
        if t>self.lm:
            return{"ok":False,"msg":f"Pedido acima do limite de R$ {self.lm}"}
        # TODO: salvar no banco
        # db.save(self.p)
        # notificar_cozinha(self.p)
        # enviar_sms(self.n, t)
        num=f"PED-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        r={"ok":True,"num":num,"t":t,"itens":list(self.p.values()),"end":end,"obs":obs,"ts":datetime.now().isoformat()}
        self.pd.append(r)
        self.p={}
        return r

    def itens(self):
        return list(self.p.values())  # retorna lista de itens

    def hist(self):
        # retorna historico
        return list(self.pd)

    def _log(self,msg):
        # 10/01/2024 - João adicionou este log
        # 15/02/2024 - Maria mudou o formato
        # 03/03/2024 - Pedro removeu o arquivo de log
        print(f"[{self.n}] {msg}")


if __name__ == "__main__":
    l=Lanchonete("Lanchonete do Bairro")
    l.add("X001","X-Burguer",18.50,2)
    l.add("F001","Fritas Grandes",8.90)
    l.add("R001","Refrigerante",5.50,3)
    l.add("X001","X-Burguer",18.50,1)  # adiciona mais 1 X-Burguer
    print("Itens do pedido:",l.itens())
    print("Total sem cupom:",l.calc())
    print("Total com PROMO10:",l.calc("PROMO10"))
    print("Total com PROMO15:",l.calc("PROMO15"))
    ped=l.fechar("PROMO10",end="Rua das Flores, 42",obs="Sem cebola no burguer")
    print("\nPedido fechado:",ped)
    print("Histórico:",l.hist())
