from django.db import models
from MClothing.models import Product
from django.conf import settings
import uuid
from django.utils.translation import gettext_lazy as _


class DeliveryOptions(models.Model):
    """
    The Delivery methods table contining all delivery
    """

    name = models.CharField(
        verbose_name=_("delivery_name"),
        help_text=_("Required"),
        max_length=255,
    )
    price = models.DecimalField(
        verbose_name=_("delivery price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999.99."),
            },
        },
        max_digits=5,
        decimal_places=2,
    )
    description = models.CharField(
        max_length=500, null=True
    )


    class Meta:
        verbose_name = _("Delivery Option")
        verbose_name_plural = _("Delivery Options")

    def __str__(self):
        return self.name



class BillingAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Customer"), on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name=_("Full Name"), max_length=150)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(_("Phone Number"), max_length=50)
    address = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "Address"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order_user")
    full_name = models.CharField(max_length=50, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_key = models.CharField(max_length=200)
    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
