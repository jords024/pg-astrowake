# pg-astrowake

Página de vendas do **Astrowake** — astrologia aplicada à vida real, com Crassus Gobbi.

HTML estático, sem build e sem dependência de runtime. Único recurso externo são as
fontes do Google.

## Estrutura

```
index.html                      página de vendas
politica-de-privacidade.html    LGPD
termos-de-uso.html              CDC, uso do conteúdo, arrependimento em 7 dias
legal.css                       folha compartilhada das páginas legais
assets/
  hero-mobile.webp              arte composta do bloco 1
  secao-2.webp                  arte composta do bloco 2
  ponte.webp                    transição borrada entre os dois blocos
```

## As artes e a costura

Os blocos 1 e 2 são peças com a copy já desenhada. No celular sangram de borda a
borda; no desktop viram pôster emoldurado, porque a proporção é vertical.

`ponte.webp` é gerada a partir das próprias artes: a franja de baixo do hero e a de
cima da seção 2, borradas e misturadas em smoothstep. Ela avança **18px** por dentro
do hero e **60px** por dentro da seção 2 — assimétrico de propósito, porque do lado
do hero só existem 25px de escuro limpo abaixo da linha de credenciais, e entrar
mais borraria o texto.

Regra ao acrescentar uma arte nova: **uma mecânica por junta**. Onde há ponte, não
use máscara; onde a arte encosta em texto, use `.arte.fecha-embaixo`.

## Antes de publicar

- [ ] Ligar os CTAs ao checkout — hoje estão em `href="#"` com `data-checkout`
- [ ] Completar o endereço no rodapé e nas páginas legais (falta cidade/UF e CEP)
- [ ] Revisão jurídica dos dois documentos legais
- [ ] Conferir as credenciais: aqui consta +10 anos / +5.000 atendimentos
