# Arquitetura do Sistema — MatrUFSC

Este documento detalha a infraestrutura e o modelo arquitetural do **MatrUFSC**, especificando a divisão de responsabilidades entre os containers, os mecanismos de comunicação e a estratégia de resiliência adotada.

---

## 1. Diagrama da Arquitetura

![Arquitetura Multi-Container do MatrUFSC](./diagrams/arquitetura.svg)

---

## 2. Visão Geral

O MatrUFSC adota uma **Arquitetura Multi-Container Orquestrada** (via Docker Compose), baseada em serviços desacoplados e isolamento de processos.

O principal diferencial desta arquitetura é a **Integração Baseada em Arquivos Compartilhados (File-Based Integration)** entre o ecossistema web e o sistema de captura de dados (Crawler). Isso elimina a necessidade de comunicação síncrona via HTTP/REST para a listagem de turmas, aumentando drasticamente a resiliência do sistema.

---

## 3. Componentes da Infraestrutura

### 3.1. Container `web` (Frontend & Backend)

- **Função:** Camada de apresentação e regras de negócio da aplicação.
- **Características:** Centraliza o ecossistema de interface com o usuário (Frontend) e a API de aplicação (Backend). É o único container exposto diretamente para a rede externa (internet).
- **Interações:**
  - Consome de forma assíncrona o arquivo de turmas do volume compartilhado.
  - Realiza operações de leitura e escrita no banco de dados para gerenciar as combinações de horários dos usuários.

### 3.2. Container `db` (Banco de Dados)

- **Função:** Persistência de dados do usuário.
- **Tecnologia:** MongoDB.
- **Características:** Totalmente isolado do ambiente externo. Não possui exposição de portas para o _host_ e não tem ciência sobre o processo de raspagem de dados.
- **Interações:** Comunica-se exclusivamente com o Backend do container `web` para o armazenamento de grades salvas.

### 3.3. Volume de Arquivos Compartilhado

- **Função:** Zona neutra de transferência de dados (Buffer de Ingestão).
- **Artefato Central:** `num_semestre.json`
- **Características:** Permite que o ciclo de vida do Crawler seja totalmente independente do ciclo de vida da aplicação Web.

### 3.4. Container `Crawler-API` (Pipeline de Ingestão)

Atua como um ecossistema isolado de processamento de dados estruturado em duas etapas internas:

- **Crawler:** Componente especializado em realizar _web scraping_ automatizado no sistema externo do **CAGR (Cadastro de Turmas)**. Ele extrai os dados brutos no formato `SEMESTRE_CAMPUS.xml`.
- **Parser:** Componente responsável por ler o XML bruto, aplicar as regras de tratamento de dados, higienizar as informações e convertê-las para o formato padronizado `num_semestre.json`, descarregando-o no volume compartilhado.
