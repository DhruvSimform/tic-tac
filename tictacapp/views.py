from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
import uuid
from .models import Game , Player
from django.contrib import messages
# Create your views here.
@login_required(login_url='/account/login-page/')
def home(request):
    if request.method == "POST":
        user = request.user
        option = request.POST.get("option")

        if option == "create":
            game = Game.objects.create()
            room_code = game.room_code
            Player.objects.create(game=game, user=user, symbol="X")
            return HttpResponseRedirect(f'/lobby/{room_code}')

        elif option == "join":
            room_code = request.POST.get("room_code")
            try:
                game = Game.objects.get(room_code=room_code)
                player_count = Player.objects.filter(game=game).count()
                if player_count >= 2:
                    messages.error(request, "Room is full.")
                    return redirect('home')
                else:
                    Player.objects.create(game=game, user=user, symbol="O")
                    return redirect('lobby', room_code=room_code)
            except Game.DoesNotExist:
                messages.error(request, "No room with that room code.")
                return redirect('home')

    return render(request, 'tictacapp/home.html')


def lobby(request,room_code):
    context = {}
    game = get_object_or_404(Game,room_code=room_code)
    players = Player.objects.filter(game=game)
    player1 = Player.objects.get(game=game,symbol="X").user.username if players.exists() else None
    player2 = Player.objects.get(game=game,symbol="O").user.username if players.count() > 1 else None
    is_owner = request.user.username == player1

    context['player1']=player1
    context['player2']=player2
    context['is_owner']=is_owner
    context['room_code']=room_code


    return render(request,'tictacapp/lobby.html',context)

            
def play(request,room_code):
    pass


   