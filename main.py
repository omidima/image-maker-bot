import json
import re
import openai
import g4f

openai.api_key = "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"  # Replace with your actual token
openai.api_base = "http://127.0.0.1:1337/v1"


def export_link(text = "علی احمدی ابراز خوشحالی از کشتار در فلسطین،همراه با انتشار عکس کیان پیر فلک https://instagram.com/ali_ahmadi.e230?igshid=NjIwNzIyMDk2Mg=="):
    r_instagram = r"https:\/\/instagram.com\/*.*=="
    r_twitter = r"(https://twitter.com/.*)\?"

    if (re.findall(r_instagram,text)):
        return 0, re.findall(r_instagram,text)
    elif (re.findall(r_twitter,text)):
        return 1, re.findall(r_twitter,text)


def export_instagram_username(text = "علی احمدی ابراز خوشحالی از کشتار در فلسطین،همراه با انتشار عکس کیان پیر فلک https://instagram.com/ali_ahmadi.e230?igshid=NjIwNzIyMDk2Mg=="):
    if (text.find("https://instagram.com/stories/") > -1):
        r = r"https:\/\/instagram.com\/stories\/(.*)\/"
        return re.findall(r, text)
    elif(text.find("https://instagram.com/")):
        r = r"https:\/\/instagram.com\/(.*)\?"
        return re.findall(r, text)
    

def export_twitter_username(link = "https://twitter.com/omiddana19/234123423?"):
    return link.split("/")[3]
    

def export_details(text = "علی احمدی ابراز خوشحالی از کشتار در فلسطین،همراه با انتشار عکس کیان پیر فلک https://instagram.com/ali_ahmadi.e230?igshid=NjIwNzIyMDk2Mg=="):
    
    propmt = """
به عنوان یک انسان و متخصص تحلیل محتوا این متن را بررسی کن و به این شکل در قالب json برگردان:
'''json
{
    subject: string,
    subject_emotion: string,
    location: string | null,
    user_name: string | null,
    links: [string],
    keyword: [string]
}'''
""" + f""" متن: {text}"""

    return openai.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo_16k.name,
        messages=[{"role": "user", "content": propmt}],
        stream=False,
    )['choices'][0]["message"]['content']


# print(export_details(text="سید رضا شاهورانی ساکن مهدیشهر ، خیابان المهدی استوری وقتی ۶۹ پادشاه مقابل شاه ایران زانو زدند(مقایسه با طرفداران رونالدو) https://instagram.com/stories/_reza_sh.v.nii/3195725490814557314?utm_source=ig_story_item_share&igshid=NjZiM2M3MzIxNA=="))

def main():
    data = json.loads(open("db.json","r").read())
    index = 0

    for item in data:
        j = []
        while len(j) == 0:
            result = export_details(text=item['content'])
            j = re.findall(r"```json(.*)```",result.replace("\n",""))

        data[index]['details'] = result
        data[index]['json'] = json.loads(j[0])

        index +=1 
        open("db.json","w").write(json.dumps(data, ensure_ascii=False))
        print(f"Review: {index}",end="\r", flush=True)

    print("Review complete.")


if __name__ == "__main__":
    main()
    # print(json.loads(re.findall(r"```json(.*)```",text.replace("\n",""))[0]))