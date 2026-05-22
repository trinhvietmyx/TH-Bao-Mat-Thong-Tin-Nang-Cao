import itertools
import sys

# Đảm bảo in được tiếng Việt trên console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def cau01():
    # Danh sách ban đầu
    lst = [1, 2, 3]
    
    # Sử dụng itertools.permutations để liệt kê tất cả các hoán vị
    # permutations() trả về một iterator chứa các tuple hoán vị
    perms = list(itertools.permutations(lst))
    
    print(f"Danh sách ban đầu: {lst}")
    print("Tất cả các hoán vị của danh sách:")
    for p in perms:
        # Chuyển tuple thành list để hiển thị đẹp hơn nếu cần, hoặc in trực tiếp tuple
        print(list(p))

if __name__ == "__main__":
    cau01()
