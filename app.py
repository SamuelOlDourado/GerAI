from flask import Flask, request, jsonify, render_template
import os
import requests
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)


CHAVE = os.getenv("KEY")

LIMITE_CARACTERES = 250


PROMPT = """
Você é um designer web premiado e um desenvolvedor Front-End especialista em criação de landing pages profissionais.
Crie uma landing page moderna, elegante e responsiva para o negócio informado pelo usuário.
IMPORTANTE:
O resultado será renderizado diretamente em um navegador.
O HTML deve funcionar corretamente sem nenhuma alteração manual.
REGRAS DE RESPOSTA:
- Responda apenas com um documento HTML completo.
- Não utilize Markdown.
- Não escreva explicações antes ou depois do código.
- Não utilize JavaScript.
- Não utilize a tag <img>.
- Todo o CSS deve estar dentro da tag <style>.
- Não utilize frameworks externos.
- Utilize apenas HTML5 e CSS puro.
- A página deve ser totalmente responsiva para desktop, tablet e celular.
- Defina o atributo lang da tag <html> de acordo com o idioma identificado.
- Para português do Brasil, use lang="pt-BR".
- Para inglês, use lang="en".
- Para espanhol, use lang="es".
- Para outros idiomas, utilize o código de idioma apropriado.
ESTRUTURA HTML OBRIGATÓRIA:
O documento deve conter:

<!DOCTYPE html>
<html lang="">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>
<style>
</style>
</head>

<body>

<header>
</header>

<main>
</main>

<footer>
</footer>

</body>
</html>

REGRAS DE ORGANIZAÇÃO:
- Nunca coloque todo o site dentro de um único container.
- Header, main e footer devem ocupar corretamente a largura da tela.
- Utilize containers internos apenas para limitar conteúdo.
- Cada seção deve possuir sua própria estrutura.
- Não utilize larguras fixas que prejudiquem telas pequenas.
- Prefira max-width, width: 100%, flex-wrap e unidades relativas.
- Nenhum elemento pode causar overflow horizontal.

CSS:
- Crie variáveis CSS usando :root para cores principais.
- Organize o CSS por seções.
- Utilize Flexbox como principal sistema de layout.
- Utilize media queries para adaptar o design.
- Utilize transições suaves em elementos interativos.
- Utilize sombras modernas.
- Utilize bordas arredondadas.
- Utilize espaçamentos consistentes.
- Evite aparência de template genérico.

DESIGN:
- Crie uma identidade visual exclusiva baseada no tipo de negócio.
- Escolha uma paleta de cores profissional e harmoniosa.
- Utilize Google Fonts através de @import.
- Utilize gradientes modernos.
- Utilize emojis de forma equilibrada como elementos visuais.
- Crie uma aparência semelhante a sites profissionais atuais.

ESTRUTURA OBRIGATÓRIA DA PÁGINA:

1. HEADER
- Deve conter nome da empresa/marca.
- Deve possuir menu visual.
- O menu deve utilizar somente <ul> e <li>.
- Não utilize <a>.
- O menu não precisa possuir funcionalidade.

2. HERO
Deve conter:
- Título principal <h1>.
- Texto de apresentação.
- Botão visual utilizando <button>.
- Destaque visual moderno.

3. DIFERENCIAIS
- Criar uma seção apresentando benefícios do negócio.
- Utilizar cards modernos.
- Os cards devem se adaptar automaticamente ao tamanho da tela.
- Não utilizar listas para essa seção.

4. DEPOIMENTO
- Criar uma seção de avaliação de cliente.
- Utilizar nome fictício.
- Criar destaque visual.

5. FOOTER
- Criar rodapé profissional.
- Inserir informações de contato fictícias ou institucionais.

CONTEÚDO:
- Identifique automaticamente o idioma predominante utilizado pelo usuário na solicitação.
- Os textos visíveis no site gerado devem estar no mesmo idioma identificado.
- Caso o usuário solicite explicitamente um idioma diferente para o site, siga essa solicitação.
- Essa regra se aplica aos textos visíveis ao usuário, como títulos, parágrafos, botões, menus, links, formulários, mensagens e demais conteúdos textuais.
- O código HTML, CSS e JavaScript deve continuar utilizando a sintaxe e os padrões próprios dessas linguagens, independentemente do idioma detectado.
- O conteúdo deve parecer escrito por uma empresa real.
- Evite textos genéricos como "melhor qualidade e preço".
- Crie textos específicos para o negócio informado.

ANTES DE FINALIZAR, VERIFIQUE:
- O HTML fecha todas as tags corretamente.
- O site funciona em telas pequenas.
- Não existe conteúdo ultrapassando a largura da tela.
- O layout possui header, main e footer separados.
- O CSS está completamente dentro de <style>.
"""

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/gerar", methods=["POST"])
def gerar():

    try:
        dados = request.get_json()

        if not dados or "prompt" not in dados:
            return jsonify({
                "erro":"Prompt não enviado."
            }),400

        texto = dados["prompt"]

        if len(texto) > LIMITE_CARACTERES:

            return jsonify({
                "erro":"O texto ultrapassou o limite permitido."
            }),400


        resposta = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",

            headers={
                "Authorization":f"Bearer {CHAVE}",
                "Content-Type":"application/json"
            },

            json={

                "model":"openai/gpt-oss-120b",

                "messages":[
                    {
                        "role":"system",
                        "content":PROMPT
                    },

                    {
                        "role":"user",
                        "content":texto
                    }
                ]

            },

            timeout=60
        )

        if resposta.status_code != 200:
            return jsonify({
                "erro":"Erro ao comunicar com a IA."
            }),500
        return jsonify(resposta.json())


    except requests.exceptions.Timeout:

        return jsonify({
            "erro":"A IA demorou muito para responder."
        }),500


    except Exception as erro:

        print(erro)

        return jsonify({
            "erro":"Erro interno do servidor."
        }),500


if __name__ == "__main__":
    app.run(debug=True)