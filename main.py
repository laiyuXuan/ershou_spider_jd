# coding:utf-8
import codecs
import datetime

import requests
from bs4 import BeautifulSoup

from product import Product

colors = ["黑", "白", "灰", "红", "黄", "蓝", "绿", "粉", "金", "银", "紫", "青", "色"]
networks = ["全网通", "移动", "联通", "电信"]
mems = {"8G", "16G", "32G", "64G", "128G", "256G"}

get_brand_url = "https://search.jd.com/search?keyword=%E4%BA%8C%E6%89%8B%E8%87%AA%E8%90%A5&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&cid3=13768#J_searchWrap"
url_prefix = "https://search.jd.com/"

user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"

cookie = "__jdu=15222049534561639914302; xtest=4502.cf6b6759; qrsc=3; pinId=yGUjj96MvGA; pin=xaychow; unick=xaychow; _tp=5Za85Tqdfi%2F%2F%2FLkv2WtWlw%3D%3D; _pst=xaychow; user-key=bf0048ad-1d0d-4c5e-9e35-7edb694aa5d3; ceshi3.com=103; ipLoc-djd=1-2800-4134-0.569671042; ipLocation=%u5317%u4EAC; PCSYCityID=1; mt_xid=V2_52007VwMWUV5bU18XTRtZAWADFVBVUFJfHUgabAc0V0EHVAtVRhgeSQkZYlRAUUFQAFkXVUlZBW4AEFNVDwJZFnkaXQVuHxNXQVtQSx9IEl0DbAATYl9oUmofShtVBGcFG1dtWFdcGA%3D%3D; _jrda=3; wlfstk_smdl=3ljnhkvlq7jovd9jbgtkhf4al3dhqy8t; cn=1; rkv=V0200; TrackID=1w0-4NoiHBz-u-nCzyG7Q7zWGViLtP89YBwQNcyBz98zCiZTijmXrTq8p_JjG6enHuPX6drodE8EsfPduqm9iSSHQ_oVbH7bgVh0TTWrRZOs; 3AB9D23F7A4B3C9B=IHIIW5P3AVN7MEERK5JLFWCZ55BHNXX3QDZNF4TRCZAWL7HHDMKMOX2CJ2WNAOLVLDXIAEBJ7V5QGKTUDT7D74OLMU; assist=LGXT4ZUUMHZXTNWWB7OME2MRZSQCVPSORLZ3X27KMWNHY3MDTTRYPHCNE6K3GGLEVWE736CGKA3E6AOI7PJF2SEUPK3DKRHELIKOYWWZX5MBHD2KFSAPNWLXF3H7THUWJSDZV4D6JDTBZAXJ3CTPY5D5RLJMZJYMMU7TQU4XP4OOX7GFNZCIXQ26TIZ4MY6V; isvName=xaychow; businessCollege_id=a558758a64da5be38e1c4fe5a7643968&&1524743404772&&xaychow; businessCollege_shopName=xaychow; __jdv=122270672|baidu|-|organic|not set|1524743405082; mobilev=html5; sid=8c439f17063516f2c8e8b941214eae9b; shshshfp=a763167144cb6b0404643406bf0f72f6; shshshfpa=b661d988-bba6-89ce-bcfb-432d23e895d1-1524809025; mba_muid=15222049534561639914302; shshshfpb=095dfb6d9663141b31ff542413d9f257cbde8113ab2de7fb35ae2bd41f; __jdc=122270672; __jda=122270672.15222049534561639914302.1522204953.1524810843.1524813611.25; thor=081D3796C9F326BDF30A24A53356D925C39F038F15A2CB9379BD34F964800E3FA03A9D962D956DD399DC384DCB578CB9446327D1451DFBBAE15A22E2357A854BEE46AB28AEECC9EFEC0708DB556FF4C9C529B3A34D93455B26FD4B4A987D313ABC4B83A6C6E87A957843F6A8A22B94A45AD98BFBA5A01ABE0ED6DAFBBCF431387A071B94E6B9F36668227A363E3A20AA; __jdb=122270672.26.15222049534561639914302|25.1524813611"

proxyDict = {
    # "http": 'http://47.90.87.225:88'
    "https": 'https://46.191.190.44:53281'
    # "ftp"   : ''
}

headers = {
    'User-Agent': user_agent,
}


def get():
    r = requests.get(get_brand_url, headers=headers, proxies=proxyDict)
    if r.status_code != 200:
        print("获取品牌失败")
        return
    soup = BeautifulSoup(str(r.content, 'utf-8'), 'lxml')
    brands = soup.select_one(".J_selectorLine.s-brand").select_one('.J_valueList').select("li")
    products = []
    for brand in brands:
        if brand.text.strip() != 'Apple':
            products.append(get_one_brand(brand.select_one("a")["href"], brand.select_one("a").text))
        else:
            get_apple(brand.select_one("a")["href"], products)
    write_excel(products)


def get_apple(url: str, products):
    r = requests.get(url_prefix + url, headers=headers, proxies=proxyDict)
    if r.status_code != 200:
        return
    decoded = str(r.content, 'utf-8')
    soup = BeautifulSoup(decoded, "lxml")
    lis = soup.select('div.J_selectorLine.s-line')[2].select_one('.J_valueList').select('li')
    for li in lis:
        products.append(get_one_brand(li.select_one('a')['href'], 'Apple'))


def get_one_brand(url: str, brand: str):
    r = requests.get(url_prefix + url, headers=headers, proxies=proxyDict)
    if r.status_code != 200:
        return
    decoded = str(r.content, 'utf-8')
    soup = BeautifulSoup(decoded, "lxml")
    goods = soup.select("#J_goodsList .gl-item")
    products = []
    for good in goods:
        p = Product()
        p.price = good.select_one(".p-price").select_one("i").text
        p.title = good.select_one(".p-name.p-name-type-2").select_one("em").text.replace("【分期用】", "")
        p.condition = p.title.split("【")[1].split("】")[0]
        p.mem = get_mem(p.title)
        p.network = get_network(p.title)
        p.color = get_color(p.title)
        p.brand = get_brand(brand)
        p.model = get_model(p)
        products.append(p)
    return products


def get_mem(title: str):
    for split in title.split(" "):
        for mem in mems:
            if split.__contains__(mem):
                return split
    return "NULL"


def get_network(title: str):
    for split in title.split(" "):
        for network in networks:
            if split.__contains__(network):
                return split
    return "NULL"


def get_color(title: str):
    for split in title.split(" "):
        for color in colors:
            if split.__contains__(color) and not split.__contains__('青春') and not split.__contains__('红米'):
                return split
    return "NULL"


def intercept(str0: str, str1: str):
    res = []
    for x in str0:
        if x in str1:
            res.append(x)
    return res


def get_brand(brand: str):
    return brand.replace('\t', '').replace('\n', '').replace('（', ' ').replace('）', ' ').strip()


def get_model(p: Product):
    model = p.title.split("】")[1] \
        .replace(p.condition, '') \
        .replace(p.mem, '') \
        .replace(p.network, '') \
        .replace(p.color, '') \
        .replace(p.brand, '') \
        .replace('手机', '') \
        .replace('双卡双待', '') \
        .replace('[精品]', '') \
        .replace('精品', '') \
        .replace('[优品]', '') \
        .replace('优品', '') \
        .replace(p.brand.split(' ')[0], '')
    if p.brand.split(' ').__len__() > 1:
        model = model.replace(p.brand.split(' ')[1], '')
    return model


def write_file(*products):
    text = ' 价格 \t 品牌 \t 型号 \t 容量 \t 网络 \t 成色 \t 颜色 \t 标题 \t \n'
    for brand in products[0]:
        for product in brand:
            text = text + product.price + ' \t '
            text = text + product.brand + ' \t '
            text = text + product.model + ' \t '
            text = text + product.mem + ' \t '
            text = text + product.network + ' \t '
            text = text + product.condition + ' \t '
            text = text + product.color + ' \t '
            text = text + product.title + ' \t '
            text = text + '\n'
    file = codecs.open('price', 'w', encoding='utf-8')
    file.write(text)
    file.close()


def write_excel(products):
    import xlwt
    wb = xlwt.Workbook(encoding='utf-8')  # 创建实例，并且规定编码
    ws = wb.add_sheet('price', cell_overwrite_ok=True)  # 设置工作表名称
    ws.write(0, 0, '售卖形式（自营、店铺名）')
    ws.write(0, 1, '品牌')
    ws.write(0, 2, '型号')
    ws.write(0, 3, '容量')
    ws.write(0, 4, '颜色')
    ws.write(0, 5, '制式')
    ws.write(0, 6, '成色')
    ws.write(0, 7, '价格')
    ws.write(0, 8, '是否有货')
    ws.write(0, 9, '原标题')
    i = 1
    for brand in products:
        for product in brand:
            ws.write(i, 0, '自营')
            ws.write(i, 1, product.brand)
            ws.write(i, 2, product.model.replace('二手苹果', '').replace('二手', ''))
            ws.write(i, 3, product.mem)
            ws.write(i, 4, product.color)
            ws.write(i, 5, product.network.replace('二手手机', '').replace('手机', ''))
            ws.write(i, 6, product.condition)
            ws.write(i, 7, product.price)
            ws.write(i, 8, '')
            ws.write(i, 9, product.title)
            i = i + 1

    wb.save(datetime.date.today().__str__() + '.xls')


if __name__ == '__main__':
    get()
    # test()

