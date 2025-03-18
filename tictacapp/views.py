from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
import uuid
from .models import Game , Player
# Create your views here.

@login_required(login_url='/account/login-page/')
def home(request):
    # print(request.user.email)
    if request.method == "POST":
        user = request.user
        option = request.POST["option"]
        print(user)

        if option == "create":
            game = Game.objects.create()
            room_code = game.room_code
            player = Player.objects.create(game=game , user=user , symbol="X")
        
            return HttpResponse(f"wait for player two to join room with code : {room_code}")  

        elif option == "join":
            room_code = request.POST["room_code"]
            print(room_code)
            try:
                game = Game.objects.get(room_code=room_code)
                print(game)
                player_count = Player.objects.filter(game=game).count()
                print(player_count)
                if player_count>=2:
                    return HttpResponse("room is full")
                else:

                    player = Player.objects.create(game=game, user=user, symbol="O")

                    return HttpResponse(f"wait for room owner to start game : {room_code}")
            except:
                return HttpResponse("no room with that room code")

            
    return render(request , 'tictacapp/home.html')


            
    


   