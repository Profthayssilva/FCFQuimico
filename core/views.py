from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'core/index.html')

def sobre(request):
    return render(request, 'core/sobre.html')

def produtos(request):
    return render(request, 'core/produtos.html')

def contato(request):
    return render(request, 'core/contato.html')


@csrf_exempt
def enviar_fds_form(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        empresa = request.POST.get("empresa")
        telefone = request.POST.get("telefone")

        mensagem = f"""
        Novo pedido de FDS:
        Nome: {nome}
        Email: {email}
        Empresa: {empresa}
        Telefone: {telefone}
        """

        send_mail(
            subject="Pedido de FDS - FCF Químicos",
            message=mensagem,
            from_email="contato@fcfquimicos.com",
            recipient_list=["contato@fcfquimicos.com", email],
            fail_silently=False,
        )

        return JsonResponse({"status": "ok"})
