import requests
from time import sleep
import instagrapi
import pytesseract
import cv2

from bot.utils.classes import UserInformation, UserStatusDTO

cv2.setUseOptimized(True)


instagram = instagrapi.Client()
instagram.login_by_sessionid("8577390667%3AR1HLRfctyOrgBe%3A22%3AAYeGAzqQv7JVp9iaJfxFrsRhr9SZvKhxv2JknSIaSA")

def extract_text(link:str):
  open("image.png", "wb").write(requests.get(link).content)

  image = cv2.imread("image.png")
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  text = pytesseract.image_to_string(gray_image, lang="eng")
  persian_text = pytesseract.image_to_string(gray_image, lang="fas")

  return text, persian_text


def hashtag_search(hashtag:str, text:str):
  new_text = hashtag.replace('#','').split("_")
  for t in new_text:
    if (t in text): return True

  return False


def check_user_status(username:str, hashtag:str) -> UserInformation:
  status = []
  user = instagram.user_info_by_username(username)
  sleep(1)
  stories = instagram.user_stories(user_id=user.pk)
  sleep(1)
  posts = instagram.user_medias_paginated(user_id=user.pk,amount=12)
  sleep(1)

  for item in stories:
    en_text, fa_text = extract_text(item.thumbnail_url)
    en_include, fa_include = hashtag_search(hashtag, en_text), hashtag_search(hashtag, fa_text)

    if (en_include or fa_include):
      status.append(UserStatusDTO(**{
          "type": item.media_type,
          "username": username,
          "hashtag": item.hashtags + [hashtag],
          "media": item.thumbnail_url,
          "caption":"Story post: "+hashtag,
          "links": item.links
      }))

  for item in posts[0]:
    if (item.caption_text.find(hashtag) > -1):
      status.append(UserStatusDTO(**{
          "type": item.media_type,
          "username": username,
          "hashtag": [hashtag],
          "media": item.thumbnail_url,
          "caption": item.caption_text,
          "like_count": item.like_count,
          "comment_count": item.comment_count,
          "view_count": item.view_count,
          "links": [f"https://www.instagram.com/p/{item.code}"]
      }))

  return UserInformation(**{
      "username": username,
      "profile_pic_url": user.profile_pic_url,
      "media_count": user.media_count,
      "bio": user.biography,
      "follower_count": user.follower_count,
      "following_count": user.following_count,
      "status": status
  })


def user_follow(username:str):
    pk = instagram.user_info_by_username(username).pk
    sleep(1)
    instagram.user_follow(pk)
    sleep(1)

    return True
