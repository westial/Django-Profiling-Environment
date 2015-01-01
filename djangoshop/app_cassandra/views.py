import json

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.contrib import messages

from app_cassandra.models import Product, User, Sale
from form_purchase import PurchaseForm
from djangoshop import payment
from vendor.BasicBenchmarker import BasicBenchmarker


# functions


def index(request):
    """
    Homepage
    :param request:
    :return: HttpResponse
    """
    products_list = Product.objects\
        .filter(date__gte=timezone.now())\
        .allow_filtering()

    template = loader.get_template('index.html')

    context = RequestContext(request, {
        'products_list': products_list,
    })

    return HttpResponse(template.render(context))


def details(request, product_id):
    """
    Displays product
    :param request: HttpRequest
    :param product_id: uuid
    :return: HttpResponse
    """

    product = get_object_or_404(Product, pk=product_id)

    purchase_form = PurchaseForm()

    return render(request, 'details.html',
                  {
                      'product': product,
                      'purchase_form': purchase_form,
                  })


def purchase(request, product_id, profiling=False):
    """
    Purchase form execution. Saves user and sale.
    :param request:
    :param product_id: int
    :param profiling: boolean. Returns json response if enabled.
    :return: HttpResponse
    """

    profiler = BasicBenchmarker(usage=True)
    profiler.start()

    if request.method != 'POST':

        error_msg = "Form method is not allowed."

        if profiling:

            profiler_results = profiler.report()
            profiler_results['error_msg'] = error_msg
            profiler_results['result'] = False

            return HttpResponse(
                json.dumps(profiler_results, sort_keys=True))

        else:

            messages.error(request, message=error_msg)

            return render(request, 'details.html', {
                'product_id': product_id,
            })

    try:
        product = Product.objects.get(pk=product_id)

    except Product.DoesNotExist:

        error_msg = "Product ID {product_id} not exists."\
            .format(product_id=product_id)

        if profiling:

            profiler_results = profiler.report()
            profiler_results['error_msg'] = error_msg
            profiler_results['result'] = False

            return HttpResponse(
                json.dumps(profiler_results, sort_keys=True))

        else:

            messages.error(request, message=error_msg)

            return render(request, 'index.html')

    purchase_form = PurchaseForm(request.POST)

    if not purchase_form.is_valid():

        error_msg = "Error sending form, data has not been validated"

        if profiling:

            profiler_results = profiler.report()
            profiler_results['error_msg'] = error_msg
            profiler_results['result'] = False

            return HttpResponse(
                json.dumps(profiler_results, sort_keys=True))

        else:

            messages.error(request, message=error_msg)

            return render(request, 'details.html',
                          {
                              'product': product,
                              'purchase_form': purchase_form,
                          })

    form_email = purchase_form.cleaned_data['email']
    form_repeat_email = purchase_form.cleaned_data['repeat_email']
    form_quantity = purchase_form.cleaned_data['quantity']

    if form_email != form_repeat_email:

        error_msg = "Email not matches repeat email."

        if profiling:

            profiler_results = profiler.report()
            profiler_results['error_msg'] = error_msg
            profiler_results['result'] = False

            return HttpResponse(
                json.dumps(profiler_results, sort_keys=True))

        else:

            messages.error(request, message=error_msg)

            return render(request, 'details.html', {
                'product_id': product_id,
            })

    if form_quantity > product.inventory:

        error_msg = "There aren't enough quantity in inventory to satisfy" \
                    " your query."

        if profiling:

            profiler_results = profiler.report()
            profiler_results['error_msg'] = error_msg
            profiler_results['result'] = False

            return HttpResponse(
                json.dumps(profiler_results, sort_keys=True))

        else:

            messages.error(request, message=error_msg)

            return render(request, 'details.html', {'product_id': product_id})

    if profiling:
        payment_result = True   # Any payment while profiling is successful.

    else:
        payment_result = payment.local_payment()

    if payment_result:

        product.inventory -= form_quantity
        product.save()

        user = User(email=form_email)
        user.save()

        sale = Sale(user_id=user.id, product_id=product_id,
                    quantity=form_quantity)
        sale.save()

        saved = bool(sale.id)

        if not saved:

            product.inventory += form_quantity
            product.save()

            user.delete()

            error_msg = "Sale has not been saved for an unknown error."

            if profiling:

                profiler_results = profiler.report()

                profiler_results['error_msg'] = error_msg
                profiler_results['result'] = False

                return HttpResponse(
                    json.dumps(profiler_results, sort_keys=True))

            else:

                messages.error(request, message=error_msg)

                return render(request, 'details.html',
                              {'product_id': product_id})

        else:

            if profiling:

                profiler_results = profiler.report()

                profiler_results['error_msg'] = ""
                profiler_results['result'] = True

                return HttpResponse(
                    json.dumps(profiler_results, sort_keys=True))

            else:

                return render(request, 'result.html', {'result': payment_result,
                                                       'product': product,
                                                       'sale': sale,
                                                       'user': user})

    else:

        if profiling:

            profiler_results = profiler.report()
            profiler_results['error_msg'] = "Payment is not finished due to " \
                                            "an error."
            profiler_results['result'] = False

            return HttpResponse(
                json.dumps(profiler_results, sort_keys=True))

        else:

            return render(request, 'result.html', {'result': payment_result,
                                                   'product': product})
