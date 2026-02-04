# Telegram Bot Setup

## Como criar seu bot Telegram (5 minutos)

### 1. Criar o bot

1. Abra o Telegram
2. Procure por `@BotFather`
3. Envie `/newbot`
4. Escolha um nome (ex: "Meu RAG Bot")
5. Escolha um username (ex: "meu_rag_bot")
6. Copie o token que o BotFather enviar

### 2. Configurar o projeto

Adicione o token no `.env`:

```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 3. Rodar o bot

```bash
poetry run python scripts/telegram_bot.py
```

### 4. Testar

1. Procure seu bot no Telegram pelo username
2. Envie `/start`
3. Faça perguntas!

## Vantagens do Telegram

- ✅ **Gratuito** - sem custos
- ✅ **Sem CNPJ** - qualquer pessoa pode criar
- ✅ **Simples** - apenas um token
- ✅ **Sem webhook** - usa polling (não precisa de servidor público)
- ✅ **Markdown** - suporta formatação rica
- ✅ **Rápido** - setup em 5 minutos

## Comandos disponíveis

- `/start` - Iniciar conversa
- Qualquer mensagem - Pergunta para o RAG

## Recursos avançados (opcional)

O bot suporta:
- Markdown formatting
- Typing indicator
- Comandos customizados
- Inline keyboards
- File uploads

Para adicionar mais funcionalidades, edite `src/integrations/telegram.py`
