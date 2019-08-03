# Tinderizer

This is a little script that automates Tinder swiping to match with profiles that liked you. It follows details laid out in Sanskar Jethi's [Medium post](https://medium.com/@sansyrox/hacking-tinders-premium-model-43f9f699d44) about a Tinder API vulnerability.

# Requirements

This has been tested only in Python 3.7.3. It might work with previous or later version of Python, but I haven't tested them.

# What Tinderizer does

Tinderizer finds all the pics from the profiles in your "Likes" deck that appears blurred to non-Premium users. It then cycles through your recommendations deck, comparing each picture via the cross-correlation template match function from OpenCV to each "Who liked you" picture. If there's an image match, Tinderizer swipes right. If none of the pictures in the profile matches, Tinderizer swipes left. Tinderizer also accepts an argument to set the proportion of random right swipes on profiles. Finally, a `right_swipe_limit` is randomly set ranging between 20 to 30 to prevent you from maxing out your right swipes.

# Installation

1. Clone this repo.
2. Install Python 3.7.3.
3. Create a virtual environment in the directory with `virtualenv name_of_your_venv`.
3. Activate the virtualenv with `source name_of_your_venv/bin/activate`.
4. Install dependencies with `pip install -r req.txt`.
5. Find your Tinder X-Auth-Token using the instructions in Sanskar Jethi's [Medium post](https://medium.com/@sansyrox/hacking-tinders-premium-model-43f9f699d44). Generally, you'll have to:
   1. Open Tinder in a browser.
   2. Open the Web Console.
   3. Swipe right on the first profile.
   4. Check the Web Console for an XHR GET request to a URL beginning with `https://api.gotinder.com/like/` followed by a string of random characters.
   5. Expand the request in the window and look for the request header titled "X-Auth-Token". Copy this to your clipboard.
6. Run the software with `python Main.py "X-Auth-Token_here" "random_right"`, where `random_right` is the proportion of random right swipes you want. If no argument is given to `random_right`, it defaults to 0.2, or 20%. Alternatively, edit and run `demo_run.sh` following the instructions inside.

# Troubleshooting

You might come across an error looking something like:

```Traceback (most recent call last):
  File "Main.py", line 145, in <module>
    unblurred_img = unblur_image(headers)
  File "Main.py", line 36, in unblur_image
    assert response.status_code == 200, "GET failed, check auth_token"
AssertionError: GET failed, check auth_token
```

This means your X-Auth-Token has expired and you'll need to fetch a new one (see Step 5 of Installation above).
