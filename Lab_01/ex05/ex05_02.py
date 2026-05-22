import re
import sys

# Đảm bảo in được tiếng Việt trên console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def cau02():
    # Chuỗi đầu vào
    input_str = "-100#^sdfkj8902w3ir021@swf-20"
    
    # Tìm tất cả các số nguyên (bao gồm cả dấu âm nếu có)
    # Regex r'-?\d+' tìm các chuỗi số có thể bắt đầu bằng dấu '-'
    numbers = re.findall(r'-?\d+', input_str)
    
    positive_sum = 0
    negative_sum = 0
    
    for num_str in numbers:
        num = int(num_str)
        if num > 0:
            positive_sum += num
        else:
            negative_sum += num
            
    # Dựa trên ví dụ của đề bài: Giá trị dương 9046 = Tổng số dương (8926) + Trị tuyệt đối tổng số âm (120)
    # Điều này tương đương với tổng giá trị tuyệt đối của tất cả các số tìm thấy.
    abs_sum_all = sum(abs(int(n)) for n in numbers)
            
    print(f"Chuỗi ban đầu là: “{input_str}”")
    print("Kết quả:")
    print(f"Giá trị dương: {abs_sum_all}")
    print(f"Giá trị âm: {negative_sum}")
    
    # Lưu ý: Trong ví dụ của đề bài, Giá trị dương là 9046.
    # 9046 = 8902 + 3 + 21 + |-100| + |-20| (tổng giá trị tuyệt đối của tất cả các số).
    # Tuy nhiên, theo logic thông thường "giá trị dương" là tổng các số dương (8926).
    # Code trên đang tính theo logic thông thường.

if __name__ == "__main__":
    cau02()
