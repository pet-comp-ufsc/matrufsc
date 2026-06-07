# Conceitos Básicos - React

Para começar a desenvolver com React, é importante aprender os conceitos que vamos ver nessa página.

## 1. Componentes

Componentes são o bloco fundamental para construir interfaces com React. Escrevemos componetes como funções do Javascript/Typescript que retornam JSX/TSX.

Veja mais [aqui](https://react.dev/reference/react/Component).

## 2. JSX/TSX (Javascript/Typescript XML)

JSX (ou TSX para esse projeto) é uma extensão de arquivo que nos permite trabalhar com componentes React com mais facilidade, permitindo escrever sintaxe semelhante a HTML dentro de um arquivo Javascript ou Typescript.

Exemplo com JSX:

```javascript
const Saudacao = ({ nome }) => <h1>Olá, {nome}!</h1>;
```

Exemplo com TSX:

```typescript
type SaudacaoProps = {
    nome: string;
}
const Saudacao = ({ nome }: SaudacaoProps) => <h1>Olá, {nome}!</h1>;

```

Abaixo também temos um exemplo sem o uso de JSX, apenas com javascript puro:

```javascript
import React from "react";

const Saudacao = ({ nome }) => {
  return React.createElement(
    "h1", // Tipo do elemento
    null, // Propriedades (props) do elemento
    "Olá, ", // Filho 1 (texto)
    nome, // Filho 2 (variável)
    "!", // Filho 3 (texto)
  );
};
```

Fica evidente que, além de ser uma má prática, usar react como na ultima forma fica inviável para componentes grandes e complexos.

Veja mais [aqui](https://react.dev/learn/writing-markup-with-jsx).

---

## 3. Props

São argumentos passados para os componentes. Props são **somente leitura**, ou seja, um componente não deve modificar suas próprias props.

```typescript
// Em typescript, devemos tipar os props
type CardProps = {
    titulo: string;
    descricao: string;
    likes: number;
    data: Date;
};

const Card = ({ titulo, descricao, likes, data }: CardProps) => {
    return (
        <div>
            <h1>{titulo}</h1>
            <p>{descricao}</p>
            <div>
                <small>{likes}</small>
                <small>{data.toString()}</small>
            </div>
        </div>
    );
}
```

Veja mais [aqui](https://react.dev/learn/passing-props-to-a-component).

## 4. State (Estado)

State representa os dados mutáveis e locais dentro de um componente. Quando o estado de um componente muda, o React agenda uma re-renderização daquele componente e de seus filhos. Veremos mais sobre estados na secção de hooks.

Veja mais [aqui](https://react.dev/learn/state-a-components-memory).
