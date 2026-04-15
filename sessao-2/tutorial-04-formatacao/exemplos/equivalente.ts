/**
 * EQUIVALENTE TypeScript — Formatação (ESLint + Prettier)
 * Referência: Clean Code, Cap. 5
 *
 * Prettier cuida do estilo automático (aspas, vírgulas, largura de linha).
 * ESLint cuida das regras semânticas (imports não usados, any implícito, etc).
 * Configure ambos em conjunto: prettier é o "formatador", eslint o "linter".
 */

// ════════════════════════════════════════════════════════════════
// ANTES — imports desorganizados, sem espaçamento, linhas longas
// ════════════════════════════════════════════════════════════════

// ❌ Ruim
import {calcularDesconto} from './descontos';import {Logger} from './logger';import {Produto,Categoria} from './tipos';import {validarCodigo} from './validadores';import axios from 'axios';

const DESCONTO=0.05;const IMPOSTO=0.12;const MAX=100;

interface Prod {id:string;nm:string;pr:number;qt:number;cat:string;ativo:boolean}

class GerenciadorEstoque_Ruim {
  private produtos:{[k:string]:Prod}={};
  adicionarProduto(id:string,nm:string,pr:number,qt:number,cat:string='geral',ativo:boolean=true):void{
    if(id in this.produtos)throw new Error(`Produto ${id} já existe`);
    if(pr<=0)throw new Error('Preço inválido');
    this.produtos[id]={id,nm,pr,qt,cat,ativo};
  }
  calcularTotal(desconto:boolean=false,imposto:boolean=false):number{
    return Object.values(this.produtos).reduce((total,p)=>{let v=p.pr*p.qt;if(desconto)v*=(1-DESCONTO);if(imposto)v*=(1+IMPOSTO);return total+v;},0);
  }
}


// ════════════════════════════════════════════════════════════════
// DEPOIS — Prettier + ESLint aplicados
// ════════════════════════════════════════════════════════════════

// ✅ Imports agrupados: 1) libs externas, 2) imports locais, em ordem alfabética
import axios from "axios";

import { calcularDesconto } from "./descontos";
import { Logger } from "./logger";
import { Categoria, Produto } from "./tipos";
import { validarCodigo } from "./validadores";

// ── Constantes ────────────────────────────────────────────────────────────────

const DESCONTO_PADRAO = 0.05;
const ALIQUOTA_IMPOSTO = 0.12;
const CAPACIDADE_MAXIMA = 100;

// ── Tipos ─────────────────────────────────────────────────────────────────────

interface ProdutoEstoque {
  codigo: string;
  nome: string;
  preco: number;
  quantidade: number;
  categoria: string;
  ativo: boolean;
}

// ── Classes ───────────────────────────────────────────────────────────────────

class GerenciadorDeEstoque {
  private produtos: Record<string, ProdutoEstoque> = {};

  // ── Operações públicas ────────────────────────────────────────────────

  adicionarProduto(
    codigo: string,
    nome: string,
    preco: number,
    quantidade: number,
    categoria: string = "geral",
    ativo: boolean = true,
  ): void {
    this.validarProdutoNovo(codigo, preco);

    this.produtos[codigo] = { codigo, nome, preco, quantidade, categoria, ativo };
  }

  calcularValorTotal(
    aplicarDesconto: boolean = false,
    incluirImpostos: boolean = false,
  ): number {
    return Object.values(this.produtos).reduce((total, produto) => {
      let valorItem = produto.preco * produto.quantidade;

      if (aplicarDesconto) {
        valorItem *= 1 - DESCONTO_PADRAO;
      }

      if (incluirImpostos) {
        valorItem *= 1 + ALIQUOTA_IMPOSTO;
      }

      return total + valorItem;
    }, 0);
  }

  // ── Operações privadas ────────────────────────────────────────────────

  private validarProdutoNovo(codigo: string, preco: number): void {
    if (codigo in this.produtos) {
      throw new Error(`Produto ${codigo} já existe no estoque`);
    }

    if (preco <= 0) {
      throw new Error("Preço deve ser positivo");
    }

    if (Object.keys(this.produtos).length >= CAPACIDADE_MAXIMA) {
      throw new Error(`Estoque cheio. Capacidade máxima: ${CAPACIDADE_MAXIMA}`);
    }
  }
}
