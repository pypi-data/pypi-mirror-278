from pydantic import BaseModel

from typing import List, Optional

from .sintese_servico import SinteseServico
from .anexo import Anexo

class NotaServico(BaseModel):
    empresa: str="HFNT"
    tipo: str="ZCOR"
    org_compras: Optional[str] = None
    grp_compradores: str
    cod_fornecedor: Optional[str] = None
    # valor_bruto: float=0.0
    sintese_itens: List[SinteseServico]
    anexo: List[Anexo]

    # def __init__(self, **data):
    #     super().__init__(**data)
    #     self.handleAllocationValue()

    # def handleAllocationValue(self):
    #     if self.valor_liquido:
    #         self.handle_montante()
    #         for sintese_item in self.sintese_itens:
    #             percentage = sintese_item.item.percentage
    #             valor_liquido_total = self.valor_liquido
    #             sintese_item.item.valor_liquido = valor_liquido_total * (percentage / 100)
    #             sintese_item.item.handle_montante()
    #     pass

    # def handle_montante(self):
    #     self.valor_bruto = self.montante
    #     if self.valor_liquido:
    #         self.montante = self.valor_liquido