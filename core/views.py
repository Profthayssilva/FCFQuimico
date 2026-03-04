import os

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST


# =====================================
# TESTE DE EMAIL
# =====================================

def teste_email(request):
    try:
        send_mail(
            subject='Teste Render',
            message='Email funcionando!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['contato@r1k2quimicos.com.br'],
            fail_silently=False,
        )
        return HttpResponse("Email enviado com sucesso!")
    except Exception as e:
        return HttpResponse(f"Erro ao enviar email: {str(e)}")


# =====================================
# PÁGINAS
# =====================================

def index(request):
    return render(request, 'core/index.html')


def sobre(request):
    return render(request, 'core/sobre.html')


def produtos(request):
    return render(request, 'core/produtos.html')


def contato(request):
    return render(request, 'core/contato.html')


# =====================================
# FORMULÁRIO DE CONTATO
# =====================================

@require_POST
def enviar_contato(request):

    nome = request.POST.get("nome")
    email_usuario = request.POST.get("email")
    empresa = request.POST.get("empresa")
    telefone = request.POST.get("telefone")
    mensagem = request.POST.get("mensagem")

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

        email_empresa = EmailMessage(
            subject="Nova mensagem no site - FCF Químicos",
            body=html_empresa,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=["contato@r1k2quimicos.com.br"],
            reply_to=[email_usuario] if email_usuario else [],
        )

        email_empresa.content_subtype = "html"
        email_empresa.send(fail_silently=False)

        return render(request, "core/contato.html", {"sucesso": True})

    except Exception as e:
        return render(
            request,
            "core/contato.html",
            {"erro": f"Erro ao enviar mensagem: {str(e)}"}
        )


# =====================================
# FORMULÁRIO DE ENVIO DE FDS (VERSÃO ESTÁVEL)
# =====================================

@require_POST
def enviar_fds_form(request):
    try:
        nome = request.POST.get("nome")
        email_usuario = request.POST.get("email")
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

        dominio = request.build_absolute_uri('/')[:-1]

        links = ""

        for url in produtos_selecionados:
            nome_arquivo = os.path.basename(url)
            link_pdf = f"{dominio}/static/core/fds/{nome_arquivo}"
            links += f"\n{link_pdf}"

        mensagem = f"""
Olá {nome},

Segue abaixo os links para download das Fichas de Segurança (FDS):

{links}

Equipe FCF Químicos
        """

        send_mail(
            subject="Fichas de Segurança (FDS) - FCF Químicos",
            message=mensagem,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_usuario],
            fail_silently=False,
        )

        return JsonResponse({"status": "ok"})

    except Exception as e:
        return JsonResponse(
            {"status": "erro", "mensagem": str(e)},
            status=500
        )