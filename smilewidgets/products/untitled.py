# from django.shortcuts import render
# import requests
# from django.http import HttpResponse
# from .serializers import ProductSerializer, GiftCardSerializer, ProductPriceSerializer
# from .models import Product, GiftCard, ProductPrice

# def get_price(request):

#     product_prices = Product.objects.all()

#     serializer = ProductPriceSerializer(,many=True)
#     return HttpResponse()

# from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError






    # must be a GET request
    if request.method != 'GET':
        return HttpResponseBadRequest('% not supported' % request.method)

    # check if productCode and date were included in the request parameters

    product_code_requested = request.GET.get('productCode', None)
    date_requested = request.GET.get('date', None)

    if not product_code_requested or not date_requested:
        return HttpResponseBadRequest("Error: Required input not included in request.")

    else:
        #convert date query 'YYYY-mm-dd' string into python object
        try:
            date = models.DateField().to_python(date_requested)
        except ValidationError as e:
            return HttpResponseBadRequest(e)

        # find product object with this product_code
        product = get_object_or_404(Product,code=product_code_requested)

        # returns multiple objects
        product_price = get_object_or_404(ProductPrice, product=product.pk)
        # product_price = ProductPrice.objects.all(Product, product=product.pk)```


        """
        this method assumes when there are two+ overlapping prices for one product
        on the same date, then that indicates a sale, and to chose the lowest price
        e.g. Black Friday price schedule overlapping with 2018 price schedule
        """

        lowest_price = None
        # get results list of product's price at date
        lowest_price =  product_price.prices.filter(
                           start_date=date,
                           end_date=date
                       ).order_by('price').first()



        # check for optional request parameter giftCardCode
        if gift_card_code:
            gift_card = get_object_or_404(GiftCard, code=gift_card_code)

        #     response_payload['price'] = '${0:.2f}'.format(adjusted_price / 100)
        #     response_payload['message'] = 'Gift card applied at that date'

        # if not valid:
        #     response_payload['message'] = 'Gift card not applicable at that date'
