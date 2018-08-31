from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import status
from rest_framework.response import Response

from .models import GiftCard, Product, ProductPrice
from .serializers import ProductSerializer, ProductPriceSerializer, GiftCardSerializer
from django.db import models
from datetime import datetime


def get_price(request):
    product_code_param = request.GET.get('productCode', None)
    date_param = request.GET.get('date', None)

    # check if productCode and date were included in the request parameters
    if product_code_param is None and date_param is None:
        return HttpResponseBadRequest("the required parameters to process this request are missing: productCode & date")
    elif product_code_param is None or date_param is None:
        return HttpResponseBadRequest("At least one of the required parameters to process this request are missing: productCode, date")
    else:

        # convert date query 'YYYY-mm-dd' string into python object
        try:
            date = models.DateField().to_python(date_param)
        except ValidationError as e:
            return HttpResponseBadRequest(e)

        # find product object with this product_code
        product_obj = get_object_or_404(Product,code=product_code_param)

        # returns list of ProductPrice objects matching product's id
        matching_product_prices = get_list_or_404(ProductPrice, product=product_obj.id)

        """
        this method assumes when there are two or more overlapping product price results
        for one product & on the same date, this indicates a sale, and to chose the lowest price
        e.g. Black Friday price schedule overlapping with 2018 price schedule
        """

        lowest_price_for_product = None
        subtotal_product_price = None
        # get results list of product's price per date requested

        matching_product_prices_matching_date = []

        for x in matching_product_prices:
            if x.date_start < date and x.date_end > date:
                matching_product_prices_matching_date.append(x)

        if len(matching_product_prices_matching_date) > 1:
            lowest_productprice = matching_product_prices_matching_date.sort(key=price).first()
        else:
            lowest_productprice = matching_product_prices_matching_date[0]

        if lowest_productprice:
            subtotal_product_price = lowest_productprice.price
        else:
            return HttpResponseNotFound()



        # check for optional request parameter giftCardCode
        gift_card_param = request.GET.get('giftCardCode', None)


        gift_card_code_valid = None
        if gift_card_param is None:
            pass
        else:
            gift_card_code_valid =  GiftCard.objects.get(code=gift_card_param)

            if gift_card_code_valid:
                if gift_card_code_valid.amount < subtotal_product_price:
                    subtotal_product_price -= gift_card_code_valid.amount
                else:
                    subtotal_product_price = 0

            else:
                return HttpResponseBadRequest("giftCard code was invalid. Please try again")

        #build response
        formatted_price_total = '${0:.2f}'.format(subtotal_product_price/ 100)
        response = {'price': formatted_price_total}
        print(response)

        return JsonResponse(status=200, data={'price': formatted_price_total})

