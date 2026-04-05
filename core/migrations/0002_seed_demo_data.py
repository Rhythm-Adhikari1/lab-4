from django.db import migrations


def seed_demo_menu(apps, schema_editor):
	Category = apps.get_model("core", "Category")
	MenuItem = apps.get_model("core", "MenuItem")

	if MenuItem.objects.exists():
		return

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


def unseed_demo_menu(apps, schema_editor):
	MenuItem = apps.get_model("core", "MenuItem")
	Category = apps.get_model("core", "Category")
	MenuItem.objects.all().delete()
	Category.objects.all().delete()


class Migration(migrations.Migration):

	dependencies = [
		("core", "0001_initial"),
	]

	operations = [
		migrations.RunPython(seed_demo_menu, unseed_demo_menu),
	]