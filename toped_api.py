import requests
import json

def get_user_input():
    keyword = input("Masukkan keyword pencarian: ")
    rows = input("Masukkan jumlah produk yang ingin ditampilkan: ")
    return keyword, rows

def create_payload(keyword, rows):
    return [{
        "operationName": "SearchProductV5Query",
        "variables": {
            "params": f"device=desktop&ob=23&page=1&q={keyword}&rows={rows}&safe_search=false&scheme=https&shipping=&show_adult=false&source=search&st=product&start=0"
        },
        "query": "query SearchProductV5Query($params: String!) {\n  searchProductV5(params: $params) {\n    data {\n      products {\n        id\n        name\n        url\n        shop {\n          name\n          city\n          __typename\n        }\n        price {\n          text\n          __typename\n        }\n        labelGroups {\n          position\n          title\n          __typename\n        }\n        rating\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }]

def display_products(data):
    products = data[0]['data']['searchProductV5']['data']['products']
    print(f"\nTotal produk ditemukan: {len(products)}")
    print("\n" + "="*50 + "\n")

    for index, product in enumerate(products, 1):
        print(f"Produk #{index}")
        print(f"Nama: {product['name']}")
        print(f"Harga: {product['price']['text']}")
        print(f"Toko: {product['shop']['name']} ({product['shop']['city']})")
        print(f"Rating: {product['rating']}")
        
        labels = [label['title'] for label in product['labelGroups'] if label['position'] == 'ri_product_credibility']
        if labels:
            print(f"Label: {', '.join(labels)}")
        
        print(f"URL: {product['url']}")
        print("\n" + "-"*50 + "\n")

def main():
    keyword, rows = get_user_input()
    
    url = 'https://gql.tokopedia.com/graphql/SearchProductV5Query'
    payload = create_payload(keyword, rows)
    
    headers = {
    'accept': '*/*',
    'accept-language': 'en,id;q=0.9',
    'content-type': 'application/json',
    'cookie': 'hfv_banner=true; DID=4b9f47cf916fe0c34fc6cb6e41e8223a01e2346449c01901514c8c7087a96c22f30d18956fa1d56fd51654a58fdfbbbe; _fbp=fb.1.1714892655569.2067736717; bm_mi=BAE9204FC71F894A5F1F9F39EEE206C9~YAAQ1MMmFxh9LjKRAQAAqn7jMhjRqw7LggzrEg6Kk03ErjuA5A9Pq+7SaIBCfbgfcBnudBPn7uM6XbPYJDVhSYsdrFkcU9/JtWDzKKqx9+4mSV7iLjPClMQP26GlnhM0gSI1CpALgUYWyXhme9g+HJgj1SxAAYuNHo8owsEm8cgaSSOjzc0ZqBcK/5KxQJOP3ynAboJd02bP8Wdk/i8LtsZ/6FL3o/s+Wd2rNFU/XXv8hie3biByMAXIG1hI2w4lwDlcl7oOwURT5cg4aumfBeTNpCY4qsgTD+meVtVp+ykGKVFglBmEfwgarJUeCvpGIUrLxZwnN57y/cmDiVr2FZkJRd95Mg==~1; _gid=GA1.2.1250847310.1723135657; _gcl_au=1.1.1936159706.1723135657; _UUID_NONLOGIN_=7285ae48f7031777cb1411999f83e2ed; _SID_Tokopedia_=OHQl6DnbBUYvMPwRmANSqOVGtIYDmmqNGR2sjmC-juU7GteID9ju27UjS3HjEOqbuR1ZCcUaBRbxIFKSuUuUu8ZlD8-3V-IgnuK9YCBCaymfrGaoAE2tkfDTkzfEA6Zq; DID_JS=NGI5ZjQ3Y2Y5MTZmZTBjMzRmYzZjYjZlNDFlODIyM2EwMWUyMzQ2NDQ5YzAxOTAxNTE0YzhjNzA4N2E5NmMyMmYzMGQxODk1NmZhMWQ1NmZkNTE2NTRhNThmZGZiYmJl47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; AMP_TOKEN=%24NOT_FOUND; ak_bmsc=2B8360102BFA27BD8C479279D86DCEB9~000000000000000000000000000000~YAAQ1MMmFyR9LjKRAQAA9YfjMhgXzkbZzU4ofMsMHsIdWKIGe8S68qDIAClwsbMvqq8b/tkwHQwOOhPcEN0Y1G+/czyZkeAOlTbb4hvUjT2X20eqQAULMjv6liVCH+dRievUrBk5bAtfHLNJ1doLZjLSA2wTvm/M8pahAdcHo8jPugaJnZo//YCcre2Pp/ApaCzZ3CWt15PVUbW0ouS7asmfQddc5rF2+u5vhdIER+Q2Co0RfPDPIPyhlJ4gAJjqAO3umlYOcNX9T6jca/JMA8VBodsa8nPpQXuyifG9dSecmCybkPu3a3pahoTxTuf61eJp0ACPqW4BpOJMF+KG5sb2d8KihdauvQaRsKfxh/fYQIeT9AatJqRl7PuOrW09EheSBv3gB6CtL23FrItGaq733RCLfXlQtghlsvkkaLR5kC0irQBmsvpVHpi7qCERff35o0NOP3o6jOF2DszdauIni2l1R3PcBGvmJBkvaiSZCXI1WwDxlGvghQht+zsOdLp5beyjpAc=; _tt_enable_cookie=1; _ttp=Yr7ZpWnmoIwJVfiQwuQZ6ytbixM; TOPATK=6byc-vplS0eezr4VkZ0MTA; l=1; tuid=68092726; gec_id=292456031265504960; uidh=OiRAV0umAqyacImg4WNBNlTmumzsWmr4HMsE47pzf08=; FPF=1; uide=bFHZ2rSr7EkiSVwX8q6TN2eO2Wn581IXfM0wSU3XtrEVQzLi; _gcl_gs=2.1.k1$i1723135794; aus=1; ISID=%7B%22www.tokopedia.com%22%3A%22d3d3LnRva29wZWRpYS5jb20%3D.89e954fb63b664389aba4fb8a6ab68d3.1714892650495.1714892650495.1723135795004.9%22%2C%22developer.tokopedia.com%22%3A%22ZGV2ZWxvcGVyLnRva29wZWRpYS5jb20%3D.8325c9e8d162649deab9f13ae28f4ea6.1723132423458.1723132423458.1723132424463.1%22%7D; _ga=GA1.2.433841451.1723135657; _abck=D13FC1157479689FC07D327129E1E942~0~YAAQ78MmF/uwnwORAQAAMaDlMgw6HoqdFMWFxhThxmH25qGHs6SfwijkYwCpvvNpYretnVll1qNm2V3L+Yn+0gZyQBtSAh4mq84DtIrFVxulGZ+Ky/z7isZFecVyRsxUPNGzkx4dlBUJpytjCSmyZryzaDJtVGFqgA7/gWBeby94kZohvvI63ljTt32uHLHhUNH3996/WUbwg52wNMl5avIU/Rq5O8erZl7EuR6jmRGBBQHJBe6bHuKJPB6g3ZIt60sJOjruk65walRBVokqMPNiggJ2FH9f+OQl2LNAFy+VhjIRD8cTbyHAxuJf70kuat9K0pH70eEOpWeRUsqBKVlpQThp3DrP0BBpEo7Ys3vBhMKnrwNbrIYSxkI6o8lZ0sQh2b2Mqj3fXD95QyvtTzXX4MVtNaaaCLAe0gs7ojjtV8aw9XD68wk7J6h6TkqAdljzDDA4Co9k5K80sjmACh5reCQsPkE=~-1~||0||~-1; bm_sz=1FA9B24C2CA87419CDF7DE2C78D043FB~YAAQ78MmF/ywnwORAQAAMaDlMhiZi/ptUkVfxVKAYk+2+nbDpHGNl7R6/lKU3xYMAFX34HPztDiy+S0Q5pnggN0FxhBLVoIv0MNnJbFFYTl9jKtA58FllpCUq/5PvLdn0LAMobeZXylZHgcSE+dzCM6+ncbQXtiRcRjjvsvJ/zId4IdBgUt9tgG0yhNTm8ve5HAfIWt1IuqEfZFgheBZoGYaOSd5o9v7JObJoOeNvaNPjrJ86e0oYrZ6RghzaD+jzFKrsrnewyuuW0Gye0jLhOvSO1H4/vGSvP7I0I4o6z5KlPvdGbxOlvUUxVJo3/zLB1qTa+82pyfgrZXxraIu7U9rz0pya3qv2XKczAtWaNDnI8ozpkIO8hxZG1flBENdGwFjG4SUuN4JET7YhCayDf9A/dVKpYAehola5Wz3/7OtL2PwnRzlfPm2X0smmKSW0J8GfB12Dk7q~4539192~3683123; _CASE_=732a69416c2a3239383f3f3f393b393c242a6b416c2a32393c3e242a6c416c2a32393e3b3a242a645d786c2a322a3a383a3c2538302538305c3a3b323c31323d3d23383f3238382a242a64697c2a322a253e2639313e3a3d3f392a242a646a642a322a5a7d65696028456964616328416a7a69606165284269716d666c7a61692a242a6467666f2a322a39383e263f383130303d2a242a784b672a322a393d393c3f2a242a7b416c2a3239393d3b383d3f3b242a7b5c71786d2a322a67676b2a242a7f416c2a3238242a7f607b2a322a53552a242a7f607b7b2a322a53552a75; _UUID_CAS_=55596e8c-8081-459e-94e1-906d2bb892d7; webauthn-session=a9272523-55c4-4562-9c50-508cccfd007a; _ga_70947XW48P=GS1.1.1723135657.5.1.1723135843.3.0.0',
    'origin': 'https://www.tokopedia.com',
    'priority': 'u=1, i',
    'referer': 'https://www.tokopedia.com/search?st=&q=handphone&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource=',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'tkpd-userid': '125639938',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'x-dark-mode': 'false',
    'x-device': 'desktop-0.0',
    'x-source': 'tokopedia-lite',
    'x-tkpd-lite-service': 'zeus',
    'x-version': 'cd2da3f'
}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        display_products(data)
    else:
        print(f"Request gagal dengan kode status: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()