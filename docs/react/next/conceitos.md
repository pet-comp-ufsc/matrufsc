# Conceitos Básicos - NextJS

Aqui estão alguns conceitos básicos de NextJS que é interessante saber.

## 1. Roteamento Baseado em Arquivos (File-based Routing)

No React tradicional, você precisa instalar bibliotecas como o `react-router` e configurar rotas via código. No Next.js, a estrutura de pastas do seu projeto determina as rotas do site automaticamente.

```
app/
├── page.jsx          -> Rota padrão (/)
├── sobre/
│   └── page.jsx      -> Rota (/sobre)
└── produtos/
    └── [id]/
        └── page.jsx  -> Rota dinâmica (ex: /produtos/123, onde 'id' é um parâmetro)
```

Além do `page.jsx`, existem arquivos de convenção especiais como `layout.jsx` (para envolver a página com elementos fixos, como menus) e `loading.jsx` (para exibir um esqueleto de carregamento enquanto os dados abrem).

**OBS:** Para este projeto, é provável que tenhamos apenas o page.tsx mesmo.

Veja mais [aqui](https://nextjs.org/docs/app/getting-started/layouts-and-pages).

## 2. Server Components e Client Components

Por padrão, **todos os componentes criados são Server Components** (RSC). Isso significa que eles são executados exclusivamente no servidor.

- **Server Components:** Podem ser assíncronos (`async/await`) e buscar dados diretamente do banco de dados ou de APIs usando chaves secretas com total segurança. O JavaScript desses componentes não vai para o navegador do utilizador, deixando a página muito mais leve.

- **Client Components:** Se você precisar de interatividade (usar hooks como `useState`, `useEffect` ou eventos como `onClick`), você deve adicionar a diretiva "use client"; na primeira linha do arquivo. Eles ainda são pré-renderizados no servidor para garantir SEO, mas ganham vida no navegador.

Veja mais [aqui](https://nextjs.org/docs/app/getting-started/server-and-client-components).

## 3. Estratégias de Renderização

Uma das principais features do NextJS é permitir o uso de diferentes técnicas para renderizar interface para o cliente.

- **SSR (Server-Side Rendering / Renderização no Servidor):** O HTML de uma página é gerado no servidor a cada requisição feita pelo utilizador. É ideal para páginas que mostram dados em tempo real que mudam frequentemente (como o feed de uma rede social ou um painel financeiro). O SEO é excelente porque o robô de busca já recebe o texto pronto.

- **SSG (Static Site Generation / Geração Estática):** O HTML é gerado apenas uma vez, no momento do build (quando você compila o projeto para mandar para produção). É extremamente rápido e ótimo para blogs, páginas institucionais ou documentações.

- **ISR (Incremental Static Regeneration):** Uma evolução do SSG. Permite que você crie páginas estáticas, mas defina um tempo de expiração (ex: revalidar a cada 60 segundos). O Next.js atualiza a página estática em segundo plano sem que você precise refazer o build do site inteiro.

- **CSR (Client-Side Rendering):** O comportamento padrão do React puro. O servidor envia um HTML vazio e o navegador do utilizador processa todo o JavaScript para desenhar a tela.

Para este projeto utilizaremos uma combinação de CSR e SSR

## 4. Backend Integrado (Route Handlers)

O NextJS elimina a necessidade de desenvolver um servidor backend separado para tarefas simples. Podemos criar APIs HTTP completos dentro da própria estrutura do projeto em arquivos separados dos componentes.

Exemplo de uma API Backend simples (`app/api/usuarios/route.js`):

```javascript
import { NextResponse } from "next/server";

// Trata requisições GET para /api/usuarios
export async function GET() {
  const usuarios = [
    { id: 1, nome: "Ana" },
    { id: 2, nome: "Carlos" },
  ];

  return NextResponse.json(usuarios);
}

// Trata requisições POST para /api/usuarios
export async function POST(request) {
  const dados = await request.json();

  // Aqui você poderia salvar os dados direto no seu banco de dados

  return NextResponse.json({ enviado: true, recebido: dados }, { status: 201 });
}
```

Veja mais [aqui](https://nextjs.org/docs/app/getting-started/route-handlers).
