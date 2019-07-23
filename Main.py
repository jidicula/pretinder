# Copyright 2019 Johanan Idicula

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import requests
import skimage as sk
import numpy as np
import time
import sys
from random import random, randint
# import matplotlib.pyplot as plt  # For img debugging purposes


def unblur_image(headers):
    # get all blurred images! https://api.gotinder.com/v2/fast-match/teasers
    response = requests.request(
        "GET",
        'https://api.gotinder.com/v2/fast-match/preview',
        headers=headers)
    print(response.status_code)
    assert response.status_code == 200, "GET failed, check auth_token"
    response.raise_for_status()
    with open('unblur.jpg', 'wb') as fd:
        for chunk in response.iter_content(chunk_size=1000):
            fd.write(chunk)
    img = sk.io.imread('unblur.jpg')
    return img


def left(headers, id):
    url = str('https://api.gotinder.com/pass/' + id)
    r = requests.request("GET", url, headers=headers)
    assert r.status_code == 200, "GET failed, check auth_token"
    print("Swipe left")
    return


def right(headers, id):
    url = str('https://api.gotinder.com/like/' + id)
    r = requests.request("GET", url, headers=headers)
    assert r.status_code == 200, "GET failed, check auth_token"
    print("Swipe right")
    r_data = r.json()

    if r_data['match'] == 'true':
        print("It's a match!")
    else:
        print("match:", r_data['match'])
    return


def rec_deck(headers):
    # Fetch recommendations deck and parse as JSON
    url = "https://api.gotinder.com/user/recs"
    recs = requests.request("GET", url, headers=headers)
    recs_data = recs.json()
    return recs_data


# Getting auth token from CLI argument
auth_token = str(sys.argv[1])
print(auth_token)

# Getting random right swipe proportion, defaulting to 0.2 if none given
try:
    random_right = 1 - float(sys.argv[2])
except Exception:
    random_right = 0.8

# Setting headers for JSON requests
headers = {
    'app_version': '6.9.4',
    'platform': 'ios',
    'Content-Type': 'application/json',
    'User-Agent': 'Tinder/7.5.3 (iPhone; iOs 10.3.2; Scale/2.00)',
    'Accept': 'application/json',
    'X-Auth-Token': auth_token
}

# Fetch unblurred image at top of "Who liked you" stack
unblurred_img = unblur_image(headers)

deck = True
k = 0
right_swipe_limit = randint(20, 30)  # Set random right swipe limit in range
print("Set right swipe limit:", right_swipe_limit)
while deck:
    recs_json = rec_deck(headers)
    print(len(recs_json['results']), "profiles in deck")

    for i in range(len(recs_json['results'])):
        time.sleep(random() * 5)  # random delay between profiles
        num_pics = len(recs_json['results'][i]['photos'])
        print(num_pics, "pics in this profile")
        id = recs_json['results'][i]['_id']
        if random() > random_right:  # Proportion of random likes
            right(headers, id)
            k += 1
            print(k, "of", right_swipe_limit, "right swipes so far")
            unblurred_img = unblur_image(headers)
            break
        for j in range(num_pics):
            time.sleep(random() * 2)  # random delay between pics
            print("profile", i + 1, ': pic', j + 1)
            img_url = recs_json['results'][i]['photos'][j]['processedFiles'][
                -1]['url']
            print(img_url)
            img = sk.io.imread(img_url)
            if np.array_equal(img, unblurred_img):
                # Uncomment below for img match debugging
                # fig, (ax_img, ax_unblurred) = plt.subplots(ncols=2)
                # ax_img.imshow(img)
                # ax_img.set_title("Current pic")
                # ax_unblurred.imshow(unblurred_img)
                # ax_unblurred.set_title("Unblurred pic")
                # plt.show()
                right(headers, id)
                unblurred_img = unblur_image(headers)
                k += 1
                print(k,  "of", right_swipe_limit, "right swipes so far")
                break
            elif j == num_pics - 1:
                left(headers, id)

    if k == right_swipe_limit:
        print("Swipe limit", right_swipe_limit, "has been reached.")
        deck = False
