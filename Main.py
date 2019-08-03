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

import os
import shutil
import sys
import time
from random import randint, random

import numpy as np
import requests

import skimage as sk
import cv2


# import matplotlib.pyplot as plt  # For img debugging purposes


def unblur_image(headers):
    response = requests.request(
        "GET",
        'https://api.gotinder.com/v2/fast-match/preview',
        headers=headers)
    assert response.status_code == 200, "GET failed, check auth_token"
    response.raise_for_status()
    with open('unblur.jpg', 'wb') as fd:
        for chunk in response.iter_content(chunk_size=1000):
            fd.write(chunk)
    img = sk.io.imread('unblur.jpg')
    return img


def teaser_reveal(headers):
    response = requests.request(
        "GET",
        'https://api.gotinder.com/v2/fast-match/teasers',
        headers=headers)
    assert response.status_code == 200, "GET failed, check auth token"
    response.raise_for_status()
    teasers_json = response.json()
    teasers = []  # instantiate list of teaser images
    # iterate through each profile
    for i in range(len(teasers_json['data']['results'])):
        # iterate through each pic in the profile
        for j in range(
                len(teasers_json['data']['results'][i]['user']['photos'])):
            url = teasers_json['data']['results'][i]['user']['photos'][j][
                'processedFiles'][-1]['url']
            img = sk.io.imread(url)
            # add pic to teaser list and write out to ./teasers directory
            teasers.append(img)
            sk.io.imsave(
                "teasers/profile" + str(i + 1) + "pic" + str(j + 1) + ".tif",
                img)
    return (teasers)


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


def image_comparison(img1, img2):
    # If images have same dimensions, no need for
    # cross-correlation template matching
    if img1.shape == img2.shape:
        if np.array_equal(img1, img2):
            return
    # cross-correlation template matching
    img1_h = img1.shape[0]  # height of img1
    img1_w = img1.shape[1]  # height of img2
    img2_h = img2.shape[0]
    img2_w = img2.shape[1]
    if img1_h > img2_h or img1_w > img2_w:
        result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
    else:  # sometimes the img is bigger than the teaser
        result = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
    # match gives correlation coefficient 1 when rounded to 3rd decimal places
    if np.round(result.max(), 3) == 1:
        return


# Clean up old image and make new teasers directory
try:
    shutil.rmtree("teasers")
except Exception:
    os.makedirs("teasers")

# Getting auth token from CLI argument
auth_token = str(sys.argv[1])
print(auth_token)

# Getting random right swipe proportion, defaulting to 0.2 if none given
try:
    random_right_threshold = 1 - float(sys.argv[2])
except Exception:
    random_right_threshold = 0.8

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

# Fetch list of teaser images from the entire "Who liked you" stack
teasers = teaser_reveal(headers)

deck = True
right_count = 0
right_swipe_limit = randint(20, 30)  # Set random right swipe limit in range
print("Set right swipe limit:", right_swipe_limit)
while deck:
    recs_json = rec_deck(headers)
    print(len(recs_json['results']), "profiles in deck.")

    for i in range(len(recs_json['results'])):
        time.sleep(random() * 5)  # random delay between profiles
        num_pics = len(recs_json['results'][i]['photos'])
        print(num_pics, "pics in this profile.")
        id = recs_json['results'][i]['_id']
        if random() > random_right_threshold:  # Random right swipes
            right(headers, id)
            right_count += 1
            print(right_count, "of", right_swipe_limit, "right swipes so far.")
            unblurred_img = unblur_image(headers)
            break
        for j in range(num_pics):
            time.sleep(random() * 2)  # random delay between fetching pics
            print("profile", i + 1, ': pic', j + 1)
            img_url = recs_json['results'][i]['photos'][j]['processedFiles'][
                -1]['url']
            print(img_url)
            img = sk.io.imread(img_url)
            for k in range(len(teasers)):  # iterate through each teaser
                teaser = teasers[k]
                if image_comparison(img, teaser):
                    right(headers, id)
                    teasers = teaser_reveal(headers)
                    right_count += 1
                    print(right_count, "of", right_swipe_limit,
                          "right swipes so far.")
                    break
            if j == num_pics - 1:
                left(headers, id)
        break

    if right_count == right_swipe_limit:
        print("Swipe limit", right_swipe_limit, "has been reached.")
        deck = False
