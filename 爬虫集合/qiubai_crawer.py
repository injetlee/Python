import requests
from bs4 import BeautifulSoup


def download_page(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r = requests.get(url, headers=headers)
    return r.text


def get_content(html, page):
    output = """第{}页 作者：{} 性别：{} 年龄：{} 点赞：{} 评论：{}\n{}\n------------\n"""
    soup = BeautifulSoup(html, 'html.parser')
    con = soup.find(id='content-left')
    con_list = con.find_all('div', class_="article")
    for i in con_list:
        author = i.find('h2').string  # 获取作者名字
        content = i.find('div', class_='content').find('span').get_text()  # 获取内容
        stats = i.find('div', class_='stats')
        vote = stats.find('span', class_='stats-vote').find('i', class_='number').string
        comment = stats.find('span', class_='stats-comments').find('i', class_='number').string
        author_info = i.find('div', class_='articleGender')  # 获取作者 年龄，性别
        if author_info is not None:  # 非匿名用户
            class_list = author_info['class']
            if "womenIcon" in class_list:
                gender = '女'
            elif "manIcon" in class_list:
                gender = '男'
            else:
                gender = ''
            age = author_info.string   # 获取年龄
        else:  # 匿名用户
            gender = ''
            age = ''

        save_txt(output.format(page, author, gender, age, vote, comment, content))


def save_txt(*args):
    for i in args:
        with open('qiubai.txt', 'a', encoding='utf-8') as f:
            f.write(i)


def main():
    # 我们点击下面链接，在页面下方可以看到共有13页，可以构造如下 url，
    # 当然我们最好是用 Beautiful Soup找到页面底部有多少页。
    for i in range(1, 14):
        url = 'https://qiushibaike.com/text/page/{}'.format(i)
        html = download_page(url)
        get_content(html, i)

if __name__ == '__main__':
    main()
