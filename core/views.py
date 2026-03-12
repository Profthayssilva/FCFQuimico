import os
import resend

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST


# =====================================
# CONFIGURAÇÃO RESEND
# =====================================

resend.api_key = settings.RESEND_API_KEY


def enviar_email_resend(subject, html, to_emails, reply_to=None):
    payload = {
        "from": settings.DEFAULT_FROM_EMAIL,
        "to": to_emails,
        "subject": subject,
        "html": html,
    }

    if reply_to:
        payload["reply_to"] = reply_to

    return resend.Emails.send(payload)


# =====================================
# TESTE DE EMAIL
# =====================================

def teste_email(request):
    try:
        enviar_email_resend(
            subject="Teste Render",
            html="""
                <div style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2>Email funcionando com Resend!</h2>
                    <p>Esse é um teste de envio do site FCF Químicos.</p>
                </div>
            """,
            to_emails=["contato@r1k2quimicos.com.br"],
        )
        return HttpResponse("Email enviado com sucesso!")
    except Exception as e:
        return HttpResponse(f"Erro ao enviar email: {str(e)}")


# =====================================
# PÁGINAS
# =====================================

def index(request):
    return render(request, "core/index.html")


def sobre(request):
    return render(request, "core/sobre.html")


def produtos(request):
    return render(request, "core/produtos.html")


def contato(request):
    return render(request, "core/contato.html")

def qualidade(request):
    return render(request, "core/qualidade.html")
# =====================================
# FORMULÁRIO DE CONTATO
# =====================================

@require_POST
def enviar_contato(request):
    nome = request.POST.get("nome", "").strip()
    email_usuario = request.POST.get("email", "").strip()
    empresa = request.POST.get("empresa", "").strip()
    telefone = request.POST.get("telefone", "").strip()
    mensagem = request.POST.get("mensagem", "").strip()

    try:
        html_empresa = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Nova mensagem recebida pelo site</h2>

            <p><strong>Nome:</strong> {nome}</p>
            <p><strong>Email:</strong> {email_usuario}</p>
            <p><strong>Empresa:</strong> {empresa}</p>
            <p><strong>Telefone:</strong> {telefone}</p>

            <h3>Mensagem:</h3>
            <p>{mensagem}</p>
        </div>
        """

        enviar_email_resend(
            subject="Nova mensagem no site - FCF Químicos",
            html=html_empresa,
            to_emails=["contato@r1k2quimicos.com.br"],
            reply_to=email_usuario if email_usuario else None,
        )

        return render(request, "core/contato.html", {"sucesso": True})

    except Exception as e:
        return render(
            request,
            "core/contato.html",
            {"erro": f"Erro ao enviar mensagem: {str(e)}"}
        )


# =====================================
# FORMULÁRIO DE ENVIO DE FDS
# =====================================

@require_POST
def enviar_fds_form(request):
    try:
        nome = request.POST.get("nome", "").strip()
        email_usuario = request.POST.get("email", "").strip()
        empresa = request.POST.get("empresa", "").strip()
        telefone = request.POST.get("telefone", "").strip()
        produtos_selecionados = request.POST.getlist("produtos")

        if not email_usuario:
            return JsonResponse(
                {"status": "erro", "mensagem": "E-mail obrigatório"},
                status=400
            )

        if not produtos_selecionados:
            return JsonResponse(
                {"status": "erro", "mensagem": "Selecione ao menos um produto"},
                status=400
            )

        dominio = request.build_absolute_uri("/")[:-1]

        links_html = ""
        links_texto = ""

        for url in produtos_selecionados:
            nome_arquivo = os.path.basename(url)
            link_pdf = f"{dominio}/static/core/fds/{nome_arquivo}"
            links_html += f'<li><a href="{link_pdf}" target="_blank">{nome_arquivo}</a></li>'
            links_texto += f"{link_pdf}\n"

        html_cliente = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Olá, {nome}!</h2>
            <p>Segue abaixo os links para download das Fichas de Segurança (FDS):</p>

            <ul>
                {links_html}
            </ul>

            <p>Equipe FCF Químicos</p>
        </div>
        """

        html_empresa = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Nova solicitação de FDS</h2>

            <p><strong>Nome:</strong> {nome}</p>
            <p><strong>Email:</strong> {email_usuario}</p>
            <p><strong>Empresa:</strong> {empresa}</p>
            <p><strong>Telefone:</strong> {telefone}</p>

            <h3>Produtos solicitados:</h3>
            <pre style="white-space: pre-wrap; font-family: Arial, sans-serif;">{links_texto}</pre>
        </div>
        """

        enviar_email_resend(
            subject="Fichas de Segurança (FDS) - FCF Químicos",
            html=html_cliente,
            to_emails=[email_usuario],
        )

        enviar_email_resend(
            subject="Nova Solicitação de FDS - FCF Químicos",
            html=html_empresa,
            to_emails=["contato@r1k2quimicos.com.br"],
            reply_to=email_usuario,
        )

        return JsonResponse({"status": "ok"})

    except Exception as e:
        return JsonResponse(
            {"status": "erro", "mensagem": str(e)},
            status=500
        )