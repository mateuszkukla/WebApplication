from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SelectFoodForm, AddFoodForm, CreateUserForm, ProfileForm
from .models import *
from datetime import timedelta
from django.utils import timezone
from datetime import date
from datetime import datetime
from .filters import FoodFilter
import dash_core_components as dcc
import dash_html_components as html
from plotly.offline import plot

from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.graph_objects as gos


@login_required(login_url='login')
def home_page_view(request):
    # Latest profile object
    calories = Profile.objects.filter(person_of=request.user).last()
    calorie_goal = calories.calorie_goal

    # creating one profile each day
    if date.today() > calories.date:
        profile = Profile.objects.create(person_of=request.user)
        profile.save()

    calories = Profile.objects.filter(person_of=request.user).last()

    # showing all food consumed present day

    all_food_today = PostFood.objects.filter(profile=calories)

    calorie_goal_status = calorie_goal - calories.total_calorie
    over_calorie = 0
    if calorie_goal_status < 0:
        over_calorie = abs(calorie_goal_status)

    context = {
        'total_calorie': calories.total_calorie,
        'calorie_goal': calorie_goal,
        'calorie_goal_status': calorie_goal_status,
        'over_calorie': over_calorie,
        'food_selected_today': all_food_today,
    }

    return render(request, 'home.html', context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')
        context = {}
        return render(request, 'login.html', context)


def log_out_page(request):
    logout(request)
    return redirect('login')


@login_required
def select_food(request):
    person = Profile.objects.filter(person_of=request.user).last()

    # for showing all food items available

    food_items = Food.objects.filter(person_of=request.user)
    form = SelectFoodForm(request.user, instance=person)

    if request.method == 'POST':
        form = SelectFoodForm(request.user, request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SelectFoodForm(request.user)

    context = {'form': form, 'food_items': food_items}
    return render(request, 'select_food.html', context)


def add_food(request):
    # for showing all food items available
    food_items = Food.objects.filter(person_of=request.user)
    form = AddFoodForm(request.POST)
    if request.method == 'POST':
        form = AddFoodForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.person_of = request.user
            profile.save()
            return redirect('add_food')
    else:
        form = AddFoodForm()
    # for filtering food
    myFilter = FoodFilter(request.GET, queryset=food_items)
    food_items = myFilter.qs
    context = {'form': form, 'food_items': food_items, 'myFilter': myFilter}
    return render(request, 'add_food.html', context)


@login_required
def update_food(request, pk):
    food_items = Food.objects.filter(person_of=request.user)

    food_item = Food.objects.get(id=pk)
    form = AddFoodForm(instance=food_item)
    if request.method == 'POST':
        form = AddFoodForm(request.POST, instance=food_item)
        if form.is_valid():
            form.save()
            return redirect('profile')
    myFilter = FoodFilter(request.GET, queryset=food_items)
    context = {'form': form, 'food_items': food_items, 'myFilter': myFilter}

    return render(request, 'add_food.html', context)


@login_required
def delete_food(request, pk):
    food_item = Food.objects.get(id=pk)
    if request.method == "POST":
        food_item.delete()
        return redirect('profile')
    context = {'food': food_item}
    return render(request, 'delete_food.html', context)


@login_required
def profile_page(request):
    # getting the lastest profile object for the user
    person = Profile.objects.filter(person_of=request.user).last()
    food_items = Food.objects.filter(person_of=request.user)

    form = ProfileForm(instance=person)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=person)

    # querying all records for the last seven days
    some_day_last_week = timezone.now().date() - timedelta(days=7)
    records = Profile.objects.filter(date__gte=some_day_last_week, date__lt=timezone.now().date(),
                                     person_of=request.user)

    def scatter_1():
        y_upper = []
        y_lower = []
        y = []
        for i in records:
            y.append(i.total_calorie)

        for idx, record in enumerate(records):
            if record.total_calorie > records[idx].calorie_goal:
                y_upper.append(record.total_calorie)
                y_lower.append(0)
            else:
                y_upper.append(0)
                y_lower.append(record.total_calorie)

        calorie_dates = [i.date for i in records]

        calorie_goal = [i.calorie_goal for i in records]

        fig = go.Figure()
        fig.add_scatter(x=calorie_dates, y=calorie_goal)
        fig.add_trace(go.Bar(x=calorie_dates, y=y,
                             base=0,
                             marker_color='crimson',
                             name='Upper Goal'))
        fig.add_trace(go.Bar(x=calorie_dates, y=y_lower,
                             base=0,
                             marker_color='blue',
                             name='Under Goal'))
        fig.add_trace(go.Bar(x=calorie_dates, y=calorie_goal,
                             base=0,
                             marker_color='lightslategrey',
                             name='Goal'
                             ))

        fig_html = fig.to_html()
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return fig_html

    context = {'form': form, 'food_items': food_items, 'records': records, 'plot11': scatter_1()}
    return render(request, 'profile.html', context)


external_stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheet)

app.layout = html.Div([
    html.H1("Square Root slider"),
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", "color": "ffffff"}),
    dcc.Slider(
        id='slider-updatemode',
        marks={i: '{}'.format(i) for i in range(20)},
        max=20,
        value=2,
        step=1,
        updatemode='drag',
    ),

])


@app.callback(
    Output('slider-graph', 'figure'),
    [Input('slider-updatemode', 'value')])
def display_value(value):
    x = []
    for i in range(value):
        x.append(i)

    y = []
    for i in range(value):
        y.append(i * i)

    graph = go.Scatter(
        x=x,
        y=y,
        name="Manipulate Graph"
    )

    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(range=[min(y), max(y)]),
        font=dict(color='white')
    )
    return {'data': [graph], 'layout': layout}
