/**
 * ==============================================================================
 * REGRAS DE DOMÍNIO - REFRIGERAÇÃO ÁGIL & SERVIÇO EM CAMPO
 * Foco: Pequenas empresas, autônomos, comércios locais e clientes residenciais.
 * ==============================================================================
 */

export type StatusOS = 'ABERTA' | 'EM_ANDAMENTO' | 'CONCLUIDA' | 'CANCELADA';
export type TipoCliente = 'RESIDENCIAL' | 'COMERCIAL';
export type TipoServico = 
  | 'LIMPEZA_HIGIENIZACAO'
  | 'CARGA_DE_GAS'
  | 'CONSERTO_VAZAMENTO'
  | 'TROCA_CAPACITOR_MOTOR'
  | 'INSTALACAO';

export interface DadosServicoFeito {
  servicoRealizado: string;
  temperaturaInsuflamentoC?: number; // Ex: 10 a 14 °C no ar condicionado
  pressaoGasPsi?: number;           // Ex: 110-130 PSI em R410A
  teveRecargaGas: boolean;
  valorPecas: number;
  valorMaoDeObra: number;
  formaPagamento: 'PIX' | 'DINHEIRO' | 'CARTAO_CREDITO' | 'CARTAO_DEBITO' | 'A_PRAZO';
  pago: boolean;
}

export class OrdemServicoSimples {
  public id: string;
  public clienteId: string;
  public tipoServico: TipoServico;
  public status: StatusOS;
  public defeitoReclamado: string;
  public servicoRealizado?: string;
  public temperaturaInsuflamentoC?: number;
  public pressaoGasPsi?: number;
  public teveRecargaGas: boolean = false;
  public valorPecas: number = 0;
  public valorMaoDeObra: number = 0;
  public formaPagamento?: string;
  public pago: boolean = false;
  public garantiaDias: number = 90; // CDC: 90 dias de garantia padrão

  constructor(id: string, clienteId: string, tipoServico: TipoServico, defeito: string) {
    if (!defeito || defeito.trim().length < 3) {
      throw new Error("INVARIANTE: O defeito/solicitação inicial do cliente é obrigatório.");
    }
    this.id = id;
    this.clienteId = clienteId;
    this.tipoServico = tipoServico;
    this.defeitoReclamado = defeito;
    this.status = 'ABERTA';
  }

  public iniciarAtendimento(): void {
    if (this.status !== 'ABERTA') {
      throw new Error("Apenas ordens ABERTAS podem iniciar atendimento.");
    }
    this.status = 'EM_ANDAMENTO';
  }

  public concluirServico(dados: DadosServicoFeito): void {
    if (this.status !== 'EM_ANDAMENTO') {
      throw new Error("Para concluir, a OS precisa estar em andamento.");
    }

    if (!dados.servicoRealizado || dados.servicoRealizado.trim().length < 5) {
      throw new Error("INVARIANTE: Descreva o serviço realizado para constar no recibo/garantia.");
    }

    if (dados.valorMaoDeObra < 0 || dados.valorPecas < 0) {
      throw new Error("Valores de peças e mão de obra não podem ser negativos.");
    }

    this.servicoRealizado = dados.servicoRealizado;
    this.temperaturaInsuflamentoC = dados.temperaturaInsuflamentoC;
    this.pressaoGasPsi = dados.pressaoGasPsi;
    this.teveRecargaGas = dados.teveRecargaGas;
    this.valorPecas = dados.valorPecas;
    this.valorMaoDeObra = dados.valorMaoDeObra;
    this.formaPagamento = dados.formaPagamento;
    this.pago = dados.pago;
    this.status = 'CONCLUIDA';
  }

  public calcularTotal(): number {
    return Number((this.valorPecas + this.valorMaoDeObra).toFixed(2));
  }

  /**
   * Mensagem amigável para envio instantâneo via WhatsApp ao cliente
   */
  public gerarMensagemWhatsApp(nomeCliente: string): string {
    const total = this.calcularTotal().toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    return `Olá ${nomeCliente}! ❄️\nSeu atendimento de refrigeração foi concluído com sucesso.\n\n*Serviço:* ${this.servicoRealizado}\n*Total:* ${total} (${this.pago ? 'PAGO' : 'Pendente'})\n*Garantia:* 90 dias.\nQualquer dúvida estamos à disposição!`;
  }
}
