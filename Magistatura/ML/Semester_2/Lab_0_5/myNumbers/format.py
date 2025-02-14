from PIL import Image
import os

def main():
    resize_image(28)

def resize_image(size):
    for i in range(0,10):
        try:
            img = Image.open(f"C:\\Users\\d.kunicin\\Python\\Python\\Magistatura\\ML\\Semester_2\\Lab_0_5\\myNumbers\\{i}.png")
                        # Получаем размеры изображения
            img_res = img.resize((size,size))
            print(img_res.size)
            img_res.save(f"C:\\Users\\d.kunicin\\Python\\Python\\Magistatura\\ML\\Semester_2\\Lab_0_5\\myNumbers\\resize_{i}.png")
        except IOError:
            print(f'Не удалось изменить размер{i}')
if __name__ == "__main__":
    main()