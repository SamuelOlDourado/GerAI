const endereco = "/gerar";
const limite = 250;
const textarea = document.querySelector(".texto-pagina");
const contador = document.querySelector(".contador-atual");
const mensagemLimite = document.querySelector(".mensagem-limite");
const botao = document.querySelector(".btn-gerar");

textarea.addEventListener("input", () => {

    let tamanho = textarea.value.length;
    contador.textContent = tamanho;

    if (tamanho >= limite) {
        mensagemLimite.classList.add("mostrar");

    } else {
        mensagemLimite.classList.remove("mostrar");
    }

});

botao.addEventListener("click", gerarCodigo);

async function gerarCodigo() {
    let texto = textarea.value.trim();
    if (!texto) {
        alert("Descreva o negócio primeiro.");
        return;
    }

    botao.disabled = true;
    botao.innerHTML =`<div class="spinner"></div>`;

    try {
        let resposta = await fetch(endereco, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                prompt: texto
            })
        });

        let dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error(dados.erro);
        }

        let resultado = dados.choices[0].message.content;
        let codigo = document.querySelector(".bloco-codigo code");
        let preview = document.querySelector(".bloco-site");

        codigo.textContent = resultado;
        Prism.highlightElement(codigo);
        preview.srcdoc = resultado;

        document
            .querySelector(".caixa-resultado")
            .classList.add("mostrar");
    }

    catch (erro) {
        console.error(erro);
        alert(erro.message);
    }

    finally {
        botao.disabled = false;
        botao.innerHTML = `<img src="/static/icons/send-horizontal.svg">`;
    }

}

async function copiarCodigo() {

    let codigo = document.querySelector(".bloco-codigo code").textContent;
    await navigator.clipboard.writeText(codigo);
    let botao = document.querySelector(".btn-copiar");

    botao.innerHTML = `<img src="/static/icons/check.svg">`;

    setTimeout(() => {
        botao.innerHTML = `<img src="/static/icons/copy.svg">`;
    }, 2000);

}

const f = document.querySelector(".bloco-site");

console.log(
    f.offsetWidth,
    f.offsetHeight,
    getComputedStyle(f).display,
    getComputedStyle(f).visibility,
    getComputedStyle(f).opacity
);

const iframe = document.querySelector(".bloco-site");

iframe.style.height = "600px";

getComputedStyle(document.querySelector(".bloco-site")).height