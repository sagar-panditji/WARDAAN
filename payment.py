from django.shortcuts import render, HttpResponse
from WARDAAN import settings
from django.contrib import messages
from django.core.mail import EmailMessage
import razorpay


razorpay_client = razorpay.Client(
    auth=(settings.razorpay_id, settings.razorpay_account_id)
)

from doctor.models import BookAppointment, Doctor
from patient.models import Patient
from home.models import PaymentOrder


def payment(request,did,pid):
    doctor = Doctor.objects.get(id=did)
    patient=Patient.objects.get(id=pid)
    final_price = doctor.fees
    order = PaymentOrder.objects.create()
    order.patient_id=patient.id
    order.doctor_id=doctor.id
    order.amount=final_price
    order.save()
    order.save()

    order_currency = "INR"
    client=razorpay.Client(auth=('rzp_test_0H9C5X5pJXVSNM','KRopirHNVJZbmAZDSpYyl7W7'))
    payment=clinet.order.create({})
        callback_url = "http://" + str(get_current_site(request)) + "/handlerequest/"
        print(callback_url)
        notes = {"order-type": "basic order from the website", "key": "value"}
        razorpay_order = razorpay_client.order.create(
            dict(
                amount=final_price * 100,
                currency=order_currency,
                notes=notes,
                receipt=order.order_id,
                payment_capture="0",
            )
        )
        print(razorpay_order["id"])
        order.razorpay_order_id = razorpay_order["id"]
        order.save()

        return render(
            request,
            "firstapp/payment/paymentsummaryrazorpay.html",
            {
                "order": order,
                "order_id": razorpay_order["id"],
                "orderId": order.order_id,
                "final_price": final_price,
                "razorpay_merchant_id": settings.razorpay_id,
                "callback_url": callback_url,
            },
        )
    else:
        return HttpResponse("505 Not Found")
