def saldo_global(request):
    if request.user.is_authenticated:
        saldo = request.user.userperfil.saldo
    else:
        saldo = None
    return {'saldo_global': saldo}