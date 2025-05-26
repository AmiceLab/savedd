
import pytesseract
from PIL import Image
import re
import cv2
import numpy as np
import os
from datetime import datetime

from django.shortcuts import render
from .forms import ImageUploadForm


#pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


# try with chatgpt -- another new upload page 9 Mar 2025

from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        
        # Save uploaded image
        image_name = "uploaded_images2/" + image.name
        file_path = default_storage.save(image_name, ContentFile(image.read()))
        
        #form = ImageUploadForm()

        return JsonResponse({"message": "Image uploaded successfully!", "image_url": file_path})
    
    #form = ImageUploadForm()

    return render(request, "upload_image.html")  # Handle GET request



def ocr_view(request):
    extracted_text = ''
    items = []  # 預設為空列表，防止未初始化的錯誤
    lightness = ''
    
    if request.method == 'POST' and request.FILES['image']:
        print("here")
        # 讀取圖片
        uploaded_image = request.FILES['image']
        img_pil = Image.open(uploaded_image)
        
        if img_pil.format == 'MPO':
            img_pil.save('converted_jpeg.jpg', 'JPEG')
            img = cv2.imread('converted_jpeg.jpg', cv2.IMREAD_UNCHANGED)
        else:
            img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            #img = cv2.imread(uploaded_image, cv2.IMREAD_UNCHANGED) <--- has problem if png
        
            
        print('Original Dimensions : ',img.shape)
    
        # Pre-process image BEFORE Tesseract
        #--------------------------------------
        
        processed_img, lightness = image_preprocess(img)
        print("imaged_processed ! ")
        # ----- ↑↑↑ GOT the process image
        
        

        # 使用 Tesseract 進行 OCR
        # (A) --- 傳送 Original
        # extracted_text = pytesseract.image_to_string(img)
        # (B) --- 傳送 processed image
        extracted_text = pytesseract.image_to_string(processed_img)
        
        all_lines = extracted_text.split('\n')
        print("all_lines =", all_lines)
        
        # Pro-process All lines AFTER Tesseract
        items = filter(all_lines)
        
        
        print("Valid items from list 1:")
        for item in items:
            print(f"Name: {item[0]}, Price: {item[1]}")
            
        return JsonResponse({
            "extracted_text": items,
            "lightness": lightness
        })

        
        
    form = ImageUploadForm()  # 確保表單初始化
    
    return render(request, "read_analysis/input.html")

    # return render(request, 'read_analysis/input.html', {'extracted_text': items, 'lightness': lightness })

def image_preprocess(img):
    
    print("side 0 =", img.shape[0])
    print("side 1 =", img.shape[1])
    light = ''

    
    if img.shape[0]+img.shape[1] > 6000 :
        scale_percent = 100
    else :
        scale_percent = 150
    
     # percent of original size  #100
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # (1)--- resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    print('Resized Dimensions : ',resized.shape)

    # 使用 Pillow 保存圖像，並設置DPI
    resized_pil = Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))  # OpenCV圖像轉換為Pillow格式

    # 設定DPI
    dpi = (300, 300)  # 設定為300 DPI
    resized_pil.save('a_resized_300dpi.png', dpi=dpi)

    # 將 Pillow 圖像轉換回 NumPy 格式（OpenCV 格式）
    resized_cv = np.array(resized_pil)
    
      
    # (1.5) ---- 灰度處理
    grayImage = cv2.cvtColor(resized_cv, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("a_resized_gray.png", grayImage)
    
    # (1.8) ------ rotate if required
    
    grayImage = rotate(grayImage)
    

    
    # (2) -- Calculate the lightess of fonts (original + resize image)
    #--------------
    font_lightness = detect_text_thinkness(grayImage)
    #=----------------
    # ---> Light fonts : higher number 
    

    # 127 between black and white, 255 white (>100 is white(190), <100 is black)
    
    # (3) -- 圖像黑白兩極化

    if font_lightness > 0.095 :  # Lightest
        light = "Lighest" 
        print("----Lightest")
        (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 150, 190, cv2.THRESH_BINARY)
    elif font_lightness > 0.085 : 
        light = "Lighter"
        print("----Lighter")
        (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 120, 190, cv2.THRESH_BINARY)
    else : #Darkness
        light = "Darkest"
        print("----Darkest")
         # (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 110, 190, cv2.THRESH_BINARY) # Walmart
        (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 115, 190, cv2.THRESH_BINARY)  #200

    #(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 85, 255, cv2.THRESH_BINARY)

    #prepare name:
    current_datetime = datetime.now().strftime("%m-%d %H-%M-%S")
    str_current_datetime = str(current_datetime)
    file_name = "a_" + str_current_datetime+".png"
    
    # (4) ---- only keep b4 sending
    cv2.imwrite(file_name, blackAndWhiteImage)
    
    # Done --> 兩極化-ed 圖像返回
    
    
    return blackAndWhiteImage, light

def rotate(img):
    
    #img --> resize + gray already
    # 使用 pytesseract 的方向偵測
    osd = pytesseract.image_to_osd(img)
    print("osd =", osd)

    # 從 OSD 結果中解析方向角度
    rotation_angle = int(osd.split('Rotate: ')[1].split('\n')[0])

    # 根據旋轉角度自動調整
    if rotation_angle == 90:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif rotation_angle == 180:
        img = cv2.rotate(img, cv2.ROTATE_180)
    elif rotation_angle == 270:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # 保存修正後的圖像
    cv2.imwrite('a_rotated.png', img)
    
    return img

def detect_text_thinkness(img):
    
    #img --> resize + gray + rotate already

    # 邊緣檢測 (Canny)
    edges = cv2.Canny(img, 50, 150)

    # 膨脹操作讓邊緣更明顯
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(edges, kernel, iterations=1)

    # 計算邊緣線條的密度 (白色像素數量)
    edge_density = np.sum(dilated == 255) / (img.shape[0] * img.shape[1])

    print(f"Edge Density: {edge_density}")
    
    return edge_density

       

# def is_purchase_item(line):
#     # Match for number with two decimal places (e.g., 10.50)
    
#     if re.search(r'\d+\.\d{2}', line) or re.search(r'\$\d',line) :
#         return True
#     return False

def filter(lines):
    
    # (1) - filter useful "lines" first        
    # filtered item line (with item and dollar)
    
    # purchase_items = [line for line in lines if is_purchase_item(line)]
    # print(purchase_items)
    # print("purchase_items =", purchase_items)
            
    # 定義要過濾的關鍵字
    exclude_keywords = ["subtotal", "tax", "total", "visa", "amount", "hst", "change due"]

    # 過濾非食物項目
    filtered_items = []
    #for item in purchase_items:
    for item in lines:
        # 轉換為小寫，檢查是否包含關鍵字
        if not any(keyword in item.lower() for keyword in exclude_keywords):
            filtered_items.append(item)

    # 結果
    print("filtered_items =", filtered_items)
    
    # (2) - extract items and price from useful lines

    promo_pattern = re.compile(r'1\s*of\s*\d+\s*\$\d{3,}', re.IGNORECASE)

    # 用來識別物品名稱和價格的模式
    # item_price_pattern = re.compile(r'([A-Za-z\s\.\-]+)\s*\d+[\s\S]*\s?(\$?[\d,]+\.\d{2})[\s\S]*')
    #item_price_pattern = re.compile(r'([A-Za-z\s\.\-]+)\s*\d+[\s\S]*\s?(\$?[\d,]+(?:\s?\.\s?\d{2}))[\s\S]*')
    item_price_pattern = re.compile(r'([A-Za-z0-9\s\.\-"\(\)]*[A-Za-z]+[A-Za-z0-9\s\.\-"\(\)]*)\s*\d+[\s\S]*\s?(\$?[\d,]+(?:\s?\.\s?\d{2}))[\s\S]*')


    # # 正則表達式
    # item_price_pattern = re.compile(
    #     r'([A-Za-z0-9\s\.\-"\(\)]*[A-Za-z]+[A-Za-z0-9\s\.\-"\(\)]*)'  # 捕獲名稱部分 (需要包括至少一個字母)
    #     r'\s*\d+[\s\S]*\s?(\$?[\d,]+(?:\.\d{1,2})?)'  # 捕獲價格部分
    #     r'\s*[=|]?\s*'  # 分隔符 | 或 =
    #     r'(\$?\d+(?:\.\d{1,2}))'  # 捕獲第二個價格
    # )

    # item_price_pattern = re.compile(
    #     # r'([A-Za-z0-9\s\.\-"\(\)]+)'          # 捕獲名稱部分 (允許特殊字符) (沒有需要包括英文字)
    #     r'([A-Za-z0-9\s\.\-"\(\)\]]*[A-Za-z]+[A-Za-z0-9\s\.\-"\(\)]*)' # 捕獲名稱部分 (允許特殊字符)(需要包括最少一個英文字)
    #     #r'(?:\s+\d+(?:\.\d{1,2})?)?'          # 忽略第一個價格
    #     r'\s*(\d[\d,]*)[\s\S]*\s?(\$?[\d,]+(?:\.\d{1,2})?)'  # 忽略產品代碼，並捕獲第二個價格
    #     r'\s*[=|]?\s*'                        # 分隔符 | 或 =
    #     r'(\$?\d+(?:\.\d{1,2}))'              # 捕獲第二個價格
    # )


    # 處理名稱與價格分開兩行的情況
    valid_items = []
    current_name = None
    
    for item in filtered_items:
    # 先匹配名稱與價格在同一行的情況
        match = item_price_pattern.search(item)

        if match:
            print("enter match =", item) # <-------- enter match = 6.00 1 6.00
            name, price = match.groups()
            valid_items.append((name, price))
            current_name = None  # 重置名稱
            
        else:
            print("enter else =", item)
            # 若未找到價格，可能是名稱行
            if not re.search(r'\d+(?:\.\d{1,2})', item):  # 檢查行內無價格
                current_name = item.strip()  # 保存名稱
                print("current_name : ", current_name)
            else:
                # 若發現價格行且有名稱儲存，將名稱與價格組合
                if current_name:
                    # 改寫價格匹配邏輯，從最後一個數字取值
                    # price_match = re.findall(r'(\$?\d+(?:\.\d{1,2}))', line)
                    price_match = re.findall(r'(\d+\.\d{2})', item)
                    
                    if price_match:  # 若有多個價格
                        price = price_match[-1]  # 取最後一個價格
                        print("price_match : ", price)
                        valid_items.append((current_name, price))
                        
                    current_name = None  # 重置名稱
                    
    # 結果輸出
    # print("valid items =")
    # for item in valid_items:
    #     print(item)

    return valid_items

        