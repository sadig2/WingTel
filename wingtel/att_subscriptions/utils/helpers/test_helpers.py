from att_subscriptions.models import ATTSubscription
from faker import Faker

fake = Faker()


def generate_att_subscription(user=None, plane=None,N=1) -> ATTSubscription:
    att_subs = ATTSubscription.objects.create(
    user=user
    plan=plan,
    status = "xren",

    )

    status = models.CharField(max_length=10,
                              choices=STATUS,
                              default=STATUS.new)

    device_id = models.CharField(max_length=20, blank=True, default='')
    phone_number = models.CharField(max_length=20, blank=True, default='')
    phone_model = models.CharField(max_length=128, blank=True, default='')
    network_type = models.CharField(max_length=5, blank=True, default='')

    effective_date = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted = models.BooleanField(default=False)