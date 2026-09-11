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

## Botões e checkout

**Todos** os botões ancoram em `#oferta`, menos **um**: o que fica junto ao preço,
marcado com `data-checkout`. Ele abre o modal de captura.

O modal coleta nome e WhatsApp e leva ao checkout da Hotmart já preenchido:

```
https://pay.hotmart.com/S58109644P?checkoutMode=10
  &name=<nome>&phoneac=<DDD>&phonenumber=<número>
```

Verificado contra o checkout real: a Hotmart recebe `NAME` e `PHONE` prontos.

### O lead não fica em lugar nenhum

Isto é HTML estático: **não há servidor para guardar o lead**. Nome e telefone
viajam pela URL até a Hotmart e acabam ali. Quem desiste na tela de pagamento
some sem deixar rastro.

Para capturar de verdade, preencha a constante `WEBHOOK` no bloco de script do
`index.html` com um endpoint que aceite `POST` de JSON. O envio já está escrito,
com `keepalive` para sobreviver à navegação:

```js
const WEBHOOK = '';   // ex.: 'https://seu-endpoint/lead'
```

## Como hospedar

O repositório é para ser importado — Vercel, Netlify, Cloudflare Pages ou qualquer
hospedagem estática. Não há build: é só apontar a raiz.

## Antes de anunciar

- [ ] Ligar o `WEBHOOK`, senão só chega quem completa a compra
- [ ] Completar o endereço no rodapé e nas páginas legais (falta cidade/UF e CEP)
- [ ] Instalar o pixel da Meta — o código já dispara `InitiateCheckout` se o `fbq` existir
- [ ] Revisão jurídica dos dois documentos legais
- [ ] Conferir as credenciais: aqui consta +10 anos / +5.000 atendimentos
