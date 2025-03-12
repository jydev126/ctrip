import re
from bs4 import BeautifulSoup

def extract_hotel_info(html_content):
    # 创建BeautifulSoup对象
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 找到hotellistContainer
    hotel_list_container = soup.find(id='hotellistContainer')
    if not hotel_list_container:
        print("没有找到hotellistContainer")
        return []
    
    # 找到所有的hotel-card
    hotel_cards = hotel_list_container.find_all(class_=lambda c: c and 'hotel-card' in c)
    
    hotels_info = []
    for card in hotel_cards:
        # 找到hotel_hotelInfoWrap
        info_wrap = card.find(class_=lambda c: c and 'hotel-card_hotelInfoWrap' in c)
        if not info_wrap:
            continue
        
        # 提取酒店名称
        hotel_name_elem = info_wrap.find(class_=lambda c: c and 'card_hotelName' in c)
        if hotel_name_elem:
            # 找到所有包含xt-text的元素
            text_elems = hotel_name_elem.find_all(class_=lambda c: c and 'xt-text' in c)
            if text_elems:
                hotel_name = text_elems[-1].get_text()
            else:
                hotel_name = "未找到酒店名称"
        else:
            hotel_name = "未找到酒店名称"
        
        # 提取酒店价格
        price_info = info_wrap.find(class_=lambda c: c and 'card_priceInfo' in c)
        price = "未找到价格"
        if price_info:
            price_layout = price_info.find(class_=lambda c: c and 'card_priceLayout' in c)
            if price_layout:
                price_cell = price_layout.find(class_=lambda c: c and 'card_price2' in c)
                if price_cell:
                    # 找到包含价格的元素
                    strong_price = price_cell.find(class_=lambda c: c and 'card_strong' in c)
                    if strong_price:
                        price = strong_price.get_text()
        
        hotels_info.append({
            "酒店名称": hotel_name,
            "价格": price
        })
    
    return hotels_info

def main():
    # 读取HTML文件
    try:
        with open("重庆酒店预订,价格查询-重庆宾馆住宿信息-【携程旅行手机版】.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print("找不到HTML文件，请确保文件路径正确")
        return
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return
    
    hotels_info = extract_hotel_info(html_content)
    
    if hotels_info:
        print(f"共找到 {len(hotels_info)} 家酒店:")
        for i, hotel in enumerate(hotels_info, 1):
            print(f"{i}. {hotel['酒店名称']} - ¥{hotel['价格']}")
    else:
        print("未找到任何酒店信息")

if __name__ == "__main__":
    main()