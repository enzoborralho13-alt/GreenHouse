
import os
import random
import asyncio
import discord
from discord.ext import commands

# ==========================================
# CONFIGURAÇÃO
# ==========================================

# O ID do canal permitido que você informou
CANAL_PERMITIDO_ID = CHAT_ID

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# Evita investigações simultâneas do mesmo usuário
investigacoes_ativas = set()

# ==========================================
# DICAS ECOLÓGICAS
# ==========================================

dicas = [
    "💡 Apague as luzes ao sair de um cômodo.",
    "💧 Feche a torneira enquanto escova os dentes.",
    "♻️ Separe os recicláveis conforme a coleta da sua região.",
    "🛍️ Prefira sacolas reutilizáveis.",
    "🔌 Evite deixar aparelhos ligados sem necessidade.",
    "📦 Reutilize objetos antes de descartá-los.",
    "🥕 Evite o desperdício de alimentos.",
    "🌞 Aproveite a luz natural durante o dia.",
    "🌱 Converse com sua família sobre hábitos sustentáveis.",
    "🚰 Avise um adulto se perceber vazamentos de água."
]

# ==========================================
# MISSÕES SUSTENTÁVEIS
# ==========================================

missoes = [
    "Apague as luzes desnecessárias hoje.",
    "Descubra quais materiais são reciclados na sua região.",
    "Encontre um objeto que possa ser reutilizado.",
    "Observe se existe desperdício de água em casa.",
    "Ajude sua família a evitar o desperdício de alimentos.",
    "Use uma garrafa reutilizável.",
    "Reaproveite papel que ainda possa ser usado.",
    "Converse com sua família sobre economia de energia.",
    "Reduza o uso de embalagens descartáveis.",
    "Descubra como separar corretamente os resíduos domésticos."
]

# ==========================================
# PERGUNTAS DA INVESTIGAÇÃO
# ==========================================

perguntas = [
    (
        "💡 Você apaga as luzes ao sair de um cômodo?",
        "Apague as luzes ao sair e aproveite a iluminação natural."
    ),
    (
        "💧 Você fecha a torneira enquanto escova os dentes?",
        "Feche a torneira durante a escovação."
    ),
    (
        "♻️ Você separa os materiais recicláveis do lixo comum?",
        "Confira quais materiais são aceitos na coleta seletiva local."
    ),
    (
        "🛍️ Você evita produtos descartáveis?",
        "Experimente usar copos, garrafas e sacolas reutilizáveis."
    ),
    (
        "📦 Você reutiliza objetos antes de jogá-los fora?",
        "Veja se algum objeto pode ser reaproveitado ou doado."
    )
]

# ==========================================
# RESTRIÇÃO DE CANAL
# ==========================================

@bot.check
async def verificar_canal(ctx):
    # Comandos permitidos apenas no canal configurado
    return (
        ctx.guild is not None
        and ctx.channel.id == CANAL_PERMITIDO_ID
    )

# ==========================================
# QUANDO O BOT FICA ONLINE
# ==========================================

@bot.event
async def on_ready():
    print("=" * 40)
    print("🌱 CASA VERDE ESTÁ ONLINE!")
    print(f"🤖 Bot: {bot.user}")
    print(f"📍 Canal permitido: {CANAL_PERMITIDO_ID}")
    print("=" * 40)

# ==========================================
# TRATAMENTO DE ERROS
# ==========================================

@bot.event
async def on_command_error(ctx, error):
    # Não responder em outros canais
    if isinstance(error, commands.CheckFailure):
        return

    # Ignorar comandos que não existem
    if isinstance(error, commands.CommandNotFound):
        return

    # Avisar sobre limite de uso
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"⏳ Aguarde {error.retry_after:.1f} segundos "
            "antes de usar esse comando novamente."
        )
        return

    print(f"Erro no comando: {error}")

    await ctx.send(
        "⚠️ Ocorreu um erro. Tente novamente."
    )

# ==========================================
# COMANDO: !AJUDA
# ==========================================

@bot.command()
async def ajuda(ctx):
    await ctx.send(
        "🌱 **CASA VERDE — MENU DE COMANDOS**\n\n"
        "📖 `!ajuda` — Mostra os comandos.\n"
        "💡 `!dica` — Recebe uma dica ecológica.\n"
        "🎯 `!missao` — Recebe uma missão sustentável.\n"
        "🔎 `!investigar` — Investiga seus hábitos em casa.\n"
        "🌎 `!planeta` — Descobre por que cuidar do ambiente importa.\n"
        "🛑 `!cancelar` — Cancela uma investigação em andamento.\n\n"
        "Pequenas atitudes fazem a diferença! 🌿"
    )

# ==========================================
# COMANDO: !DICA
# ==========================================

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def dica(ctx):
    dica_escolhida = random.choice(dicas)

    await ctx.send(
        f"🌎 **Dica ecológica para {ctx.author.display_name}:**\n"
        f"{dica_escolhida}"
    )

# ==========================================
# COMANDO: !MISSAO
# ==========================================

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def missao(ctx):
    missao_escolhida = random.choice(missoes)

    await ctx.send(
        f"🎯 **Sua missão ecológica, {ctx.author.display_name}!**\n\n"
        f"{missao_escolhida}\n\n"
        "Quando terminar, conte como foi! 🌱"
    )

# ==========================================
# COMANDO: !PLANETA
# ==========================================

@bot.command()
async def planeta(ctx):
    await ctx.send(
        "🌎 **POR QUE CUIDAR DO MEIO AMBIENTE?**\n\n"
        "💧 Economizar água ajuda a evitar desperdícios.\n"
        "💡 Economizar energia reduz o consumo desnecessário.\n"
        "♻️ Separar resíduos facilita a reciclagem.\n"
        "📦 Reutilizar objetos pode reduzir a quantidade de lixo.\n\n"
        "🌱 Comece com uma pequena mudança hoje!"
    )

# ==========================================
# COMANDO: !INVESTIGAR
# ==========================================

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def investigar(ctx):
    chave = (ctx.author.id, ctx.channel.id)

    if chave in investigacoes_ativas:
        await ctx.send(
            "🔎 Você já tem uma investigação em andamento!"
        )
        return

    investigacoes_ativas.add(chave)

    try:
        await ctx.send(
            "🔎 **INVESTIGAÇÃO AMBIENTAL INICIADA!**\n\n"
            "Responda às perguntas com `sim` ou `não`.\n"
            "Você terá 60 segundos para responder cada pergunta.\n"
            "Digite `!cancelar` a qualquer momento para encerrar. 🌱"
        )

        pontuacao = 0
        sugestoes = []

        def verificar_resposta(mensagem):
            return (
                mensagem.author.id == ctx.author.id
                and mensagem.channel.id == ctx.channel.id
                and not mensagem.author.bot
            )

        for pergunta, sugestao in perguntas:
            await ctx.send(pergunta)

            while True:
                try:
                    resposta = await bot.wait_for(
                        "message",
                        check=verificar_resposta,
                        timeout=60
                    )
                except asyncio.TimeoutError:
                    await ctx.send(
                        "⏰ O tempo acabou! Use `!investigar` "
                        "para começar novamente."
                    )
                    return

                texto = resposta.content.lower().strip()

                if texto in ("!cancelar", "cancelar"):
                    await ctx.send("🛑 Investigação cancelada!")
                    return

                if texto in ("sim", "não", "nao"):
                    break

                await ctx.send(
                    "❓ Responda apenas com `sim` ou `não`."
                )

            if texto == "sim":
                pontuacao += 2
            else:
                sugestoes.append(sugestao)

        await ctx.send(
            f"📋 **RELATÓRIO AMBIENTAL DE "
            f"{ctx.author.display_name}**\n\n"
            f"🌱 Pontuação: **{pontuacao}/10**"
        )

        if pontuacao >= 9:
            await ctx.send(
                "🏆 **GUARDIÃO DO PLANETA!**\n"
                "Você relatou ótimos hábitos sustentáveis. Continue assim!"
            )
        elif pontuacao >= 6:
            await ctx.send(
                "🌿 **DETETIVE VERDE!**\n"
                "Você está no caminho certo. Algumas mudanças podem ajudar."
            )
        else:
            await ctx.send(
                "🌱 **APRENDIZ VERDE!**\n"
                "Comece com pequenas mudanças. Cada atitude conta!"
            )

        if sugestoes:
            texto_missoes = "\n".join(
                f"🎯 {sugestao}" for sugestao in sugestoes
            )

            await ctx.send(
                f"**SUAS MISSÕES PERSONALIZADAS:**\n\n"
                f"{texto_missoes}"
            )
        else:
            await ctx.send(
                "🌟 Você respondeu sim a todas as perguntas! "
                "Continue com esses bons hábitos."
            )

    finally:
        investigacoes_ativas.discard(chave)

# ==========================================
# TOKEN E INICIALIZAÇÃO
# ==========================================

if __name__ == "__main__":
    token = os.getenv("CASA_VERDE_TOKEN")

    if not token:
        raise RuntimeError(
            "Token não encontrado! Configure CASA_VERDE_TOKEN "
            "no terminal do VS Code."
        )

    bot.run(token)
