from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Category(models.Model):
	name = models.CharField(max_length=120, unique=True)

	def __str__(self):
		return self.name


class MenuItem(models.Model):
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="items")
	name = models.CharField(max_length=150)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	stock = models.PositiveIntegerField(default=0)
	is_available = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.name} ({self.category.name})"


class Order(models.Model):
	STATUS_CHOICES = [
		("NEW", "New"),
		("PREP", "Preparing"),
		("DONE", "Done"),
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
	status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="NEW")
	total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	notes = models.CharField(max_length=255, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def recalculate_total(self):
		aggregate = self.items.aggregate(total=Sum(models.F("quantity") * models.F("unit_price")))
		self.total_amount = aggregate["total"] or 0
		self.save(update_fields=["total_amount"])

	def __str__(self):
		return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
	menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True, blank=True)
	quantity = models.PositiveIntegerField(default=1)
	unit_price = models.DecimalField(max_digits=8, decimal_places=2)

	def __str__(self):
		return f"{self.quantity} x {self.menu_item}"


class FeedbackDocument(models.Model):
	# JSONField is used as a NoSQL-like document bucket for flexible feedback schemas.
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	payload = models.JSONField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Feedback #{self.id}"

