# Tinderizer

This is a little script that automates Tinder swiping to match with profiles that liked you. It follows details laid out in Sanskar Jethi's [Medium post](# https://medium.com/@sansyrox/hacking-tinders-premium-model-43f9f699d44) about a Tinder API vulnerability.

# Requirements

This has been tested only in Python 3.7.3. It might work with previous or later version of Python, but I haven't tested them.

# What Tinderizer does

Tinderizer finds the original profile pic at the top of your "Likes" deck that appears blurred to non-Premium users. It then cycles through your recommendations deck, comparing each picture to the picture from the profile that liked you. If there's an image match, Tinderizer swipes right. If none of the pictures in the profile matches, Tinderizer swipes left. Tinderizer also accepts an argument to set the proportion of random right swipes on profiles. Finally, a `right_swipe_limit` is randomly set ranging between 30 to 40 to prevent you from maxing out your right swipes.

# Installation

1. Clone this repo.
2. Install Python 3.7.3.
3. Create a virtual environment in the directory with `virtualenv name_of_your_venv`.
3. Activate the virtualenv with `source name_of_your_venv/bin/activate`.
4. Install dependencies with `pip install -r req.txt`.
5. Find your Tinder X-Auth-Token using the instructions in Sanskar Jethi's [Medium post](# https://medium.com/@sansyrox/hacking-tinders-premium-model-43f9f699d44).
6. Run the software with `python Main.py "X-Auth-Token_here" "random_right"`, where `random_right` is the proportion of random right swipes you want. If no argument is given to `random_right`, it defaults to 0.2, or 20%.

# Troubleshooting

You might come across an error looking something like:

```Traceback (most recent call last):
  File "Main.py", line 82, in <module>
    unblurred_img = unblur_image(headers)
  File "Main.py", line 31, in unblur_image
    response.raise_for_status()
  File "/path/to/tinderizer/venv/lib/python3.7/site-packages/requests/models.py", line 940, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 401 Client Error: Unauthorized for url: https://api.gotinder.com/v2/fast-match/preview```

This means your X-Auth-Token has expired and you'll need to fetch a new one (see Step 5 of Installation above).
