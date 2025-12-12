from django.shortcuts import render
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os


# ===========================
# PÁGINAS
# ===========================

def index(request):
    return render(request, 'core/index.html')

def sobre(request):
    return render(request, 'core/sobre.html')

def produtos(request):
    return render(request, 'core/produtos.html')

def contato(request):
    return render(request, 'core/contato.html')


# ===========================
# FORMULÁRIO DE CONTATO
# ===========================

@csrf_exempt
def enviar_contato(request):
    print("FORMULÁRIO DE CONTATO RECEBIDO")

    if request.method == "POST":
        nome = request.POST.get("nome")
        email_usuario = request.POST.get("email")
        empresa = request.POST.get("empresa")
        telefone = request.POST.get("telefone")
        mensagem = request.POST.get("mensagem")

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
                Este e-mail foi enviado automaticamente pelo formulário de contato do site FCF Químicos.
            </p>
        </div>
        """

        email_empresa = EmailMessage(
    subject="📬 Nova mensagem no site - FCF Químicos",
    body=html_empresa,
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=["contatofcfquimicos@gmail.com"],
    reply_to=[email_usuario]
)


        email_empresa.content_subtype = "html"
        email_empresa.send()

        return render(request, "core/contato.html", {"sucesso": True})

    return render(request, "core/contato.html")


# ===========================
# FORMULÁRIO DE ENVIO DE FDS
# ===========================

@csrf_exempt
def enviar_fds_form(request):
    if request.method == "POST":

        nome = request.POST.get("nome")
        email_usuario = request.POST.get("email")
        empresa = request.POST.get("empresa")
        telefone = request.POST.get("telefone")

        produtos_selecionados = request.POST.getlist("produtos")

        print("PRODUTOS RECEBIDOS:", produtos_selecionados)

        # ===============================
        # LOCALIZAR PDFs
        # ===============================
        anexos = []

        for url in produtos_selecionados:
            nome_arquivo = os.path.basename(url)

            caminho_pdf = (
                settings.BASE_DIR /
                "core" /
                "static" /
                "core" /
                "fds" /
                nome_arquivo
            )

            if caminho_pdf.exists():
                anexos.append(str(caminho_pdf))

        print("ANEXOS ENCONTRADOS:", anexos)

        # ===============================
        # E-MAIL PARA O CLIENTE
        # ===============================
        html_user = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color:#004D7A;">Fichas de Segurança (FDS)</h2>

            <p>Olá <strong>{nome}</strong>,</p>
            <p>Segue em anexo as FDS solicitadas.</p>

            <p style="font-size: 13px; color:#777;">
                Atenciosamente,<br>
                Equipe FCF Químicos
            </p>
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

        email_usuario_envio.send()

        # ===============================
        # E-MAIL PARA A EMPRESA
        # ===============================
        html_empresa = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color:#004D7A;">Nova Solicitação de FDS</h2>

            <p><strong>Nome:</strong> {nome}</p>
            <p><strong>Email:</strong> {email_usuario}</p>
            <p><strong>Empresa:</strong> {empresa}</p>
            <p><strong>Telefone:</strong> {telefone}</p>

            <h3>Produtos solicitados:</h3>
            <ul>
                {''.join(f"<li>{os.path.basename(p)}</li>" for p in produtos_selecionados)}
            </ul>
        </div>
        """

        email_empresa = EmailMessage(
            subject="Nova Solicitação de FDS - FCF Químicos",
            body=html_empresa,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=["contatofcfquimicos@gmail.com"],
            reply_to=[email_usuario]
        )
        email_empresa.content_subtype = "html"
        email_empresa.send()

        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "erro"}, status=400)
