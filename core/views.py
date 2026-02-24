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
            <h2 style="color:#004D7A;">Nova mensagem recebida pelo site</h2>

            <p><strong>Nome:</strong> {nome}</p>
            <p><strong>Email:</strong> {email_usuario}</p>
            <p><strong>Empresa:</strong> {empresa}</p>
            <p><strong>Telefone:</strong> {telefone}</p>

            <h3 style="color:#004D7A; margin-top:20px;">Mensagem:</h3>
            <p style="white-space: pre-line; color:#333;">{mensagem}</p>

            <p style="margin-top:30px; font-size:12px; color:#777;">
                Este e-mail foi enviado automaticamente pelo formulário do site FCF Químicos.
            </p>
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
# FORMULÁRIO DE ENVIO DE FDS
# =====================================

@require_POST
def enviar_fds_form(request):
    try:
        nome = request.POST.get("nome")
        email_usuario = request.POST.get("email")
        empresa = request.POST.get("empresa")
        telefone = request.POST.get("telefone")
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

        anexos = []

        for url in produtos_selecionados:
            nome_arquivo = os.path.basename(url)

            # ✅ SOLUÇÃO: Tentar STATIC_ROOT primeiro (produção), depois fonte (dev)
            caminho_producao = settings.STATIC_ROOT / "core" / "fds" / nome_arquivo
            caminho_dev = settings.BASE_DIR / "core" / "static" / "core" / "fds" / nome_arquivo

            if caminho_producao.exists():
                anexos.append(str(caminho_producao))
            elif caminho_dev.exists():
                anexos.append(str(caminho_dev))
            # Se não existir em nenhum, ignora silenciosamente

        if not anexos:
            return JsonResponse(
                {"status": "erro", "mensagem": "Nenhum arquivo PDF encontrado"},
                status=404
            )

        # ================= EMAIL PARA CLIENTE =================
        html_user = f"""
        <div style="font-family: Arial;">
            <h2>Fichas de Segurança (FDS)</h2>
            <p>Olá {nome},</p>
            <p>Segue em anexo as FDS solicitadas.</p>
            <p>Equipe FCF Químicos</p>
        </div>
        """

        email_usuario_envio = EmailMessage(
            subject="Fichas de Segurança (FDS) - FCF Químicos",
            body=html_user,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_usuario],
        )
        email_usuario_envio.content_subtype = "html"

        for pdf in anexos:
            email_usuario_envio.attach_file(pdf)

        email_usuario_envio.send(fail_silently=False)

        # ================= EMAIL PARA EMPRESA =================
        html_empresa = f"""
        <div style="font-family: Arial;">
            <h2>Nova Solicitação de FDS</h2>
            <p><strong>Nome:</strong> {nome}</p>
            <p><strong>Email:</strong> {email_usuario}</p>
            <p><strong>Empresa:</strong> {empresa}</p>
            <p><strong>Telefone:</strong> {telefone}</p>
            <p><strong>Produtos:</strong> {len(anexos)} arquivo(s)</p>
        </div>
        """

        email_empresa = EmailMessage(
            subject="Nova Solicitação de FDS - FCF Químicos",
            body=html_empresa,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=["contato@r1k2quimicos.com.br"],
            reply_to=[email_usuario],
        )
        email_empresa.content_subtype = "html"
        email_empresa.send(fail_silently=False)

        return JsonResponse({"status": "ok"})

    except Exception as e:
        import traceback
        print(f"ERRO FDS: {traceback.format_exc()}")  # Log para debug no Render
        return JsonResponse(
            {"status": "erro", "mensagem": str(e)},
            status=500
        )
