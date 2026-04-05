from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET

from .forms import FeedbackForm, MenuItemForm, OrderCreateForm, RegistrationForm
from .models import FeedbackDocument, MenuItem, Order, OrderItem


def _is_staff(user):
	return user.is_staff


def _seed_demo_menu():
	if MenuItem.objects.exists():
		return

	from .models import Category

	meal = Category.objects.create(name="Meals")
	snack = Category.objects.create(name="Snacks")
	drink = Category.objects.create(name="Drinks")

	MenuItem.objects.bulk_create(
		[
			MenuItem(category=meal, name="Campus Rice Bowl", price=4.99, stock=24, is_available=True),
			MenuItem(category=meal, name="Noodle Fiesta", price=5.49, stock=18, is_available=True),
			MenuItem(category=snack, name="Crunchy Wrap", price=2.75, stock=30, is_available=True),
			MenuItem(category=drink, name="Iced Lemon Tea", price=1.50, stock=40, is_available=True),
		]
	)


def dashboard(request):
	_seed_demo_menu()
	visit_count = request.session.get("visit_count", 0) + 1
	request.session["visit_count"] = visit_count
	selected_theme = request.session.get("theme", "classic")

	menu_count = MenuItem.objects.filter(is_available=True).count()
	order_count = Order.objects.count()
	ratings = []
	for payload in FeedbackDocument.objects.values_list("payload", flat=True):
		if isinstance(payload, dict):
			rating = payload.get("rating")
			if isinstance(rating, (int, float)):
				ratings.append(float(rating))
	avg_feedback = round(sum(ratings) / len(ratings), 2) if ratings else "N/A"

	return render(
		request,
		"core/dashboard.html",
		{
			"visit_count": visit_count,
			"selected_theme": selected_theme,
			"menu_count": menu_count,
			"order_count": order_count,
			"avg_feedback": round(avg_feedback, 2) if avg_feedback else "N/A",
		},
	)


def about_response_demo(request):
	return HttpResponse("SmartCanteen: Example of direct HttpResponse handling.")


@require_GET
def api_health(request):
	return JsonResponse(
		{
			"status": "ok",
			"active_menu_items": MenuItem.objects.filter(is_available=True).count(),
			"orders": Order.objects.count(),
		}
	)


def register_view(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Account created and logged in.")
			return redirect("dashboard")
	else:
		form = RegistrationForm()
	return render(request, "registration/register.html", {"form": form})


def menu_list(request):
	_seed_demo_menu()
	items = MenuItem.objects.select_related("category").order_by("category__name", "name")
	return render(request, "core/menu_list.html", {"items": items})


@login_required
@user_passes_test(_is_staff)
def menu_create(request):
	if request.method == "POST":
		form = MenuItemForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Menu item created.")
			return redirect("menu-list")
	else:
		form = MenuItemForm()
	return render(request, "core/menu_form.html", {"form": form, "title": "Create Menu Item"})


@login_required
@user_passes_test(_is_staff)
def menu_update(request, pk):
	item = get_object_or_404(MenuItem, pk=pk)
	if request.method == "POST":
		form = MenuItemForm(request.POST, instance=item)
		if form.is_valid():
			form.save()
			messages.success(request, "Menu item updated.")
			return redirect("menu-list")
	else:
		form = MenuItemForm(instance=item)
	return render(request, "core/menu_form.html", {"form": form, "title": "Update Menu Item"})


@login_required
@user_passes_test(_is_staff)
def menu_delete(request, pk):
	item = get_object_or_404(MenuItem, pk=pk)
	if request.method == "POST":
		item.delete()
		messages.success(request, "Menu item deleted.")
		return redirect("menu-list")
	return render(request, "core/menu_delete.html", {"item": item})


@login_required
def place_order(request):
	if request.method == "POST":
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			menu_item = form.cleaned_data["menu_item"]
			quantity = form.cleaned_data["quantity"]
			order = Order.objects.create(user=request.user, notes=form.cleaned_data["notes"])
			OrderItem.objects.create(
				order=order,
				menu_item=menu_item,
				quantity=quantity,
				unit_price=menu_item.price,
			)
			order.recalculate_total()
			messages.success(request, f"Order #{order.id} created.")
			return redirect("my-orders")
	else:
		form = OrderCreateForm()

	return render(request, "core/place_order.html", {"form": form})


@login_required
def my_orders(request):
	orders = (
		Order.objects.filter(user=request.user)
		.prefetch_related("items", "items__menu_item")
		.order_by("-created_at")
	)
	return render(request, "core/my_orders.html", {"orders": orders})


@login_required
def feedback_create(request):
	if request.method == "POST":
		form = FeedbackForm(request.POST)
		if form.is_valid():
			payload = {
				"rating": form.cleaned_data["rating"],
				"topic": form.cleaned_data["topic"],
				"comment": form.cleaned_data["comment"],
				"would_recommend": form.cleaned_data["would_recommend"],
				"submitted_by": request.user.username,
			}
			FeedbackDocument.objects.create(user=request.user, payload=payload)
			request.session["last_feedback_topic"] = payload["topic"]
			messages.success(request, "Feedback saved in document format.")
			return redirect("dashboard")
	else:
		form = FeedbackForm()

	return render(request, "core/feedback_form.html", {"form": form})


def set_theme(request, theme):
	request.session["theme"] = theme
	return redirect(request.META.get("HTTP_REFERER", "dashboard"))

