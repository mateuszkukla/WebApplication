from django.http import HttpResponse, HttpResponseRedirect
from .models import Food, Meal, User, ToDoList, Item
from django.shortcuts import render, get_object_or_404
# from django.urls import reverse
from .forms import CrateNewList
from django.contrib.auth.models import User as Us


def home(response):
    return render(response, "web/home.html", {"name": "test"})


def index(response, id):
    ls = ToDoList.objects.get(id=id)
    if ls in response.user.todolist.all():
        if response.method == "POST":
            print(response.POST)
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c"+str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()

            elif response.POST.get("newItem"):
                txt = response.POST.get("new")
                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("Invalid")
        return render(response, "web/list.html", {"ls":ls})
    return  render(response, "web/view.html", {})




def create(response):
    if response.method == "POST":
        form = CrateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)

            return HttpResponseRedirect(f"/{t.id}")
    else:
        form = CrateNewList()
    return render(response, "web/create.html", {"form":form})

def view(response):
    return render(response, 'web/view.html', {})
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'web/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('results', args=(question.id,)))
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'web/results.html', {'question': question})