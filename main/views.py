from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.conf import settings
from django.core import serializers
from django.db.models import Avg, Count

from django.contrib.auth.models import User,auth

from .models import *

import json
import datetime
import os


# Problem Types
Prob_TYPES = (
    (0, 'None'),
    (1, 'Scam'),
    (2, 'Problems with withdrawals'),
    (3, 'Problems with deposits'),
    (4, 'Problems with KYC'),
    (5, 'Problems with Trade'),
    (6, 'Problems with Coins/Tokens'),
    (7, 'Problems with Customer Service'),
    (8, 'Problems with wallets'),
    (9, 'Other Problems'),
)


def sw(request):
    path = os.path.join(settings.BASE_DIR, 'static', 'pwabuilder-sw.js')
    with open(path , 'r') as myfile:
        data=myfile.read()
    response = HttpResponse(content=data)
    response['Content-Type'] = 'text/javascript'
    return response

def offline(request):
    path = os.path.join(settings.BASE_DIR, 'templates', 'offline.html')
    with open(path , 'r') as myfile:
        data=myfile.read()
    response = HttpResponse(content=data)
    response['Content-Type'] = 'text/html'
    return response

def assetlinks(request):
    path = os.path.join(settings.BASE_DIR, '.well-known', 'assetlinks.json')
    with open(path , 'r') as myfile:
        data=myfile.read()
    response = HttpResponse(content=data)
    response['Content-Type'] = 'application/json'
    return response


# Dynamic Views
def index(request):
    return render(request, 'main/index.html')


# Get Static filtered platforms
def platforms_filter(request, filter):
    return render(request, 'main/filter.html', {
        'filter' : filter,
    })

# Get Addresses
def addresses(request):
    return render(request, 'main/address.html')



# Platform Page
def platform(request, name):
    plt = get_object_or_404(platforms, name=name)

    # reviews
    revs = review.objects.filter(platform=plt).order_by('-createdon')

    # avg user rating
    count_revs = plt.review_set.count()
    avg = 0
    if (count_revs > 0):
        avg = list(plt.review_set.filter(is_comment=False).aggregate(Avg('rating')).values())[0]
        avg = round(avg, 2)
    else:
        avg = 5

    api_name = plt.api_name
    if not api_name:
        api_name = plt.name.lower()

    # Count Reports
    count_repos = review.objects.filter(
        platform=plt,
        is_problem=True,
        is_problem_resolved=False).values('problem_type').annotate(rcount=Count('problem_type'))

    prob_types = []
    for ptype in Prob_TYPES:
        prob_types.append([ptype[0], ptype[1], 0])

    for ptype in count_repos:
        prob_types[ptype['problem_type']][2] = ptype['rcount']


    return render(request, 'main/platform.html', {
        'platform' : plt,
        'count_revs' : count_revs,
        'users_avg' : avg,
        'api_name' : api_name,
        'Prob_TYPES' : prob_types,
    })


# Static Views
def support(request):
    return render(request, 'main/index.html')



# Register Requests
def register_requests(request):
    if not request.user.is_authenticated:
        return JsonResponse({
                'type' : 'error',
                'message' : 'Anonymous request!',
                'data' : {}
            })


    post_val = None
    if request.method == 'POST':
        post_val = json.loads(request.body.decode("utf-8"))

        req = requests()

        req.request = post_val['request_text']
        req.name = request.user.username
        req.email = request.user.email

        if (len(req.request.strip()) == 0):
            return JsonResponse({
                'type' : 'error',
                'message' : 'Please provide a review',
                'data' : {}
            })

        try:
            req.save()
            return JsonResponse({
                'type' : 'success',
                'message' : ''
            })
        except:
            return JsonResponse({
                'type' : 'error',
                'message' : 'Unable to send request. Please validate all fields',
                'data' : {}
            })
    else:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Invalid Request',
            'data' : {}
        })


# Register Reviews
def register_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({
                'type' : 'error',
                'message' : 'Anonymous request!',
                'data' : {}
            })


    post_val = None
    if request.method == 'POST':
        post_val = request.POST

        req = review()

        req.review = post_val['review_text']
        req.image = request.FILES.get('review_img', False)
        req.name = request.user.username
        req.email = request.user.email

        req.platform = get_object_or_404(platforms, name=post_val['platform_name'])

        if (post_val['rating'].isnumeric() and
            int(post_val['rating']) > 0 and
            int(post_val['rating']) <= 5 ):
            req.rating = int(post_val['rating'])
        else:
            return JsonResponse({
                'type' : 'error',
                'message' : 'Please provide a rating',
                'data' : {}
            })

        if (len(req.review.strip()) == 0):
            return JsonResponse({
                'type' : 'error',
                'message' : 'Please provide a review',
                'data' : {}
            })

        req.is_comment = False
        req.parent = 0

        req.is_problem = post_val['review_is_problem'] == 'true'
        req.problem_type = post_val['review_problem_type']
        req.is_problem_resolved = False

        try:
            req.save()
            return JsonResponse({
                'type' : 'success',
                'message' : ''
            })
        except:
            return JsonResponse({
                'type' : 'error',
                'message' : 'Unable to post review. Please validate all fields',
                'data' : {}
            })
    else:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Invalid Request',
            'data' : {}
        })


# Register Comment
def register_comment(request):
    if not request.user.is_authenticated:
        return JsonResponse({
                'type' : 'error',
                'message' : 'Anonymous request!',
                'data' : {}
            })


    post_val = None
    if request.method == 'POST':
        post_val = json.loads(request.body.decode("utf-8"))

        req = review()

        req.review = post_val['review_text']
        req.name = request.user.username
        req.email = request.user.email
        req.platform = get_object_or_404(platforms, name=post_val['platform_name'])
        req.rating = 0

        if (len(req.review.strip()) == 0):
            return JsonResponse({
                'type' : 'error',
                'message' : 'Please provide a review',
                'data' : {}
            })

        req.is_comment = True
        req.parent = post_val['review_parent']
        req.is_problem = False
        req.problem_type = 0
        req.is_problem_resolved = False

        try:
            req.save()
            return JsonResponse({
                'type' : 'success',
                'message' : ''
            })
        except:
            return JsonResponse({
                'type' : 'error',
                'message' : 'Unable to post review. Please validate all fields',
                'data' : {}
            })
    else:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Invalid Request',
            'data' : {}
        })


# Register Address
def register_address(request):
    if not request.user.is_authenticated:
        return JsonResponse({
                'type' : 'error',
                'message' : 'Anonymous request!',
                'data' : {}
            })


    post_val = None
    if request.method == 'POST':
        post_val = json.loads(request.body.decode("utf-8"))

        req = address()

        req.name = request.user.username

        req.coin = post_val['coin']
        req.exchange = post_val['exchange']
        req.network_type = post_val['network_type']
        req.address = post_val['address']

        try:
            req.save()
            return JsonResponse({
                'type' : 'success',
                'message' : ''
            })
        except:
            return JsonResponse({
                'type' : 'error',
                'message' : 'Unable to save address. Please validate all fields',
                'data' : {}
            })
    else:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Invalid Request',
            'data' : {}
        })




# Get Searchs
def get_search(request):
    post_val = None
    if request.method == 'POST':
        post_val = json.loads(request.body.decode("utf-8"))
        inp = post_val['inp']

        if (len(inp) < 2):
            return JsonResponse({
                'type' : 'error',
                'message' : 'Enter atlest 2 characters to search',
                'data' : {}
            })

        try:
            plts = platforms.objects.filter(name__icontains=inp).order_by('-rating')[:6]
            data = []
            for plt in plts:
                data.append({
                    'name' : plt.name,
                    'image_url' : plt.image_url,
                })

            return JsonResponse({
                'type' : 'success',
                'message' : '',
                'data' : json.dumps(data),
            })
        except:
            return JsonResponse({
                'type' : 'error',
                'message' : 'Unable to find searches',
                'data' : {}
            })
    else:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Invalid Request',
            'data' : {}
        })


# Get Recently reeviewed
def get_recent(request):
    try:
        plt = platforms.objects.all().order_by('-createdon')[:10]

        return JsonResponse({
            'type' : 'success',
            'message' : '',
            'data' : serializers.serialize('json', plt),
        })
    except:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Unable to get recent. Please try again!',
            'data' : {}
        })



# Get Top Exchanges
def get_top_exchanges(request):
    try:
        plt = platforms.objects.filter(
                platform_type='exchange'
            ).order_by('-rating')[:10]

        return JsonResponse({
            'type' : 'success',
            'message' : '',
            'data' : serializers.serialize('json', plt),
        })
    except:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Unable to get top exchanges. Please try again!',
            'data' : {}
        })


# Get Top Coins
def get_top_coins(request):
    try:
        plt = platforms.objects.filter(
                platform_type='coin'
            ).order_by('-rating')[:10]

        return JsonResponse({
            'type' : 'success',
            'message' : '',
            'data' : serializers.serialize('json', plt),
        })
    except:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Unable to get top coins. Please try again!',
            'data' : {}
        })


# Get Top Giveaways
def get_top_ga(request):
    try:
        plt = platforms.objects.filter(
                platform_type='give_away'
            ).order_by('-rating')[:10]

        return JsonResponse({
            'type' : 'success',
            'message' : '',
            'data' : serializers.serialize('json', plt),
        })
    except:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Unable to get top giveaways. Please try again!',
            'data' : {}
        })


# Get Filter reviewed
def get_filter(request, filter, page):
    is_valid = True
    is_valid &= int(page) >= 0
    is_valid &= (filter == 'all' or filter == 'exchange' or filter == 'coin' or filter == 'give_away')

    if not is_valid:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Invalid Request',
            'data' : {}
        })

    try:
        page = int(page)

        if filter == 'all':
            plt = platforms.objects.all().order_by('-createdon')[page*20 : (page+1)*20]
            count = platforms.objects.all().count()
        else:
            plt = platforms.objects.filter(
                    platform_type = filter
                ).order_by('-createdon')[page*20 : (page+1)*20]

            count = platforms.objects.filter(
                        platform_type = filter
                    ).count()

        return JsonResponse({
            'type' : 'success',
            'message' : '',
            'data' : serializers.serialize('json', plt),
            'page_count' : int(count/20) + 1,
        })
    except:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Unable to get recent. Please try again!',
            'data' : {}
        })



def dtserialize(o):
    if isinstance(o, datetime.datetime):
        return "{}-{}-{}".format(o.year, o.month, o.day)

# Get Reviews
def get_reviews(request, plt, filter, page):
    is_valid = True
    is_valid &= int(page) >= 0

    if not is_valid:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Invalid Request',
            'data' : {}
        })

    try:
        page = int(page)
        plt = get_object_or_404(platforms, name=plt)

        # reviews
        if (filter != 0):
            revs_qs = review.objects.filter(platform=plt, problem_type=filter, is_comment=False).order_by('-createdon')[page*3 : (page+1)*3]
            count = review.objects.filter(platform=plt, problem_type=filter, is_comment=False).count()

        else:
            revs_qs = review.objects.filter(platform=plt, is_comment=False).order_by('-createdon')[page*3 : (page+1)*3]
            count = review.objects.filter(platform=plt, is_comment=False).count()

        revs = []
        for rev in revs_qs:
            revs.append({
                'id' : rev.id,
                'name' : rev.name,
                'review' : rev.review,
                'rating' : rev.rating,
                'image_url' : rev.image.url if rev.image else None,
                'createdon' : str(rev.createdon),
                'is_problem' : rev.is_problem,
                'problem_type' : rev.problem_type,
                'is_problem_resolved' : rev.is_problem_resolved,
                'comments_count' : review.objects.filter(platform=plt, is_comment=True, parent=rev.id).count()
            })

        return JsonResponse({
            'type' : 'success',
            'message' : '',
            'data' : json.dumps(revs),
            'page_count' : int(count/3) + 1,
        })
    except:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Unable to get reviews. Please try again!',
            'data' : {}
        })


# Get Comments
def get_comments(request, parent):
    is_valid = True
    is_valid &= int(parent) >= 0

    if not is_valid:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Invalid Request',
            'data' : {}
        })

    try:
        # reviews
        parent = int(parent)
        revs_qs = review.objects.filter(is_comment=True, parent=parent).order_by('-createdon')
        count = review.objects.filter(is_comment=True, parent=parent).count()

        revs = []
        for rev in revs_qs:
            revs.append({
                'id' : rev.id,
                'name' : rev.name,
                'review' : rev.review,
                'createdon' : str(rev.createdon),
            })

        return JsonResponse({
            'type' : 'success',
            'message' : '',
            'data' : json.dumps(revs),
        })
    except:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Unable to get reviews. Please try again!',
            'data' : {}
        })



# Get Last Saved
def get_last_saved(request):
    if not request.user.is_authenticated:
        return JsonResponse({
                'type' : 'success',
                'message' : '',
                'data' : '[]'
            })

    try:
        saves = address.objects.filter(
                name=request.user.username
            ).order_by('-createdon')[:10]

        return JsonResponse({
            'type' : 'success',
            'message' : '',
            'data' : serializers.serialize('json', saves),
        })
    except:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Unable to get last saves. Please try again!',
            'data' : {}
        })


# Get All saved coins
def get_all_saved_coins(request):
    if not request.user.is_authenticated:
        return JsonResponse({
                'type' : 'success',
                'message' : '',
                'data' : '[]'
            })

    try:
        saves = address.objects.all().filter(
                name=request.user.username
            ).annotate(coin_count=Count('coin')).order_by('-createdon')

        return JsonResponse({
            'type' : 'success',
            'message' : '',
            'data' : serializers.serialize('json', saves, fields=('coin', 'coin_count',)),
        })
    except:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Unable to get last saves. Please try again!',
            'data' : {}
        })


# Get saved address for a coin
def get_coin_saved(request):
    if not request.user.is_authenticated:
        return JsonResponse({
                'type' : 'success',
                'message' : '',
                'data' : '[]'
            })

    post_val = json.loads(request.body.decode("utf-8"))
    coin = post_val.get('coin', False)

    try:
        saves = address.objects.all().filter(
                name=request.user.username,
                coin=coin
            ).order_by('-createdon')

        return JsonResponse({
            'type' : 'success',
            'message' : '',
            'data' : serializers.serialize('json', saves),
        })
    except:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Unable to get last saves. Please try again!',
            'data' : {}
        })


# Delete Address
def del_address(request):
    if not request.user.is_authenticated:
        return JsonResponse({
                'type' : 'error',
                'message' : 'Anonymous request!',
                'data' : {}
            })


    post_val = None
    if request.method == 'POST':
        post_val = json.loads(request.body.decode("utf-8"))
        name = request.user.username
        address_text = post_val.get('address', False)
        pk = post_val.get('pk', False)

        req = address.objects.filter(
                name=name,
                address=address_text,
                pk=pk,
            )

        try:
            if (req.exists()):
                req.delete()
                return JsonResponse({
                    'type' : 'success',
                    'message' : ''
                })
            else:
                return JsonResponse({
                    'type' : 'error',
                    'message' : 'Address not found',
                    'data' : {}
                })
        except:
            return JsonResponse({
                'type' : 'error',
                'message' : 'Unable to delete address. Please validate all fields',
                'data' : {}
            })
    else:
        return JsonResponse({
            'type' : 'error',
            'message' : 'Invalid Request',
            'data' : {}
        })