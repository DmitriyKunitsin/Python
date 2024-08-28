## Словари упорядочены, изменяемы и не допускают дублирования
## Элементы хранятся в словаре inkey:valuepairs и на них можно ссылаться по имени ключа

test_dict = { "fruit": "mango", "colors": ["red", "green", "yellow"]}
print(test_dict["fruit"])
print(test_dict["colors"])

print('\n')
## Можно получить ключ и значение след образом
print(test_dict.keys())
print(test_dict.values())

## Можно обновить значения след образом
test_dict.update({"fruit": "grapes"})
print(test_dict)
## Можно добавить в словарь 
test_dict["test"] = ["sweet", "home"]
print(test_dict)
print(test_dict["test"])

## Можно выталкивать элементы
print("Выталкиваем элементы ",test_dict.pop("colors"))
print(test_dict)

## Можно вытащить последний выставленный элемент
print("Выталкиваем последний вставленный элемент ",test_dict.popitem())
print(test_dict)

## Удаление элемента 
del test_dict["fruit"]
print(test_dict)

## Удаление словаря
del test_dict

print('\n')
while_dict = { "fruit": "mango", "colors": ["red", "green", "yellow"]}

for items in while_dict.keys():
    print(items)

print('\n')

for items in while_dict.values():
    print(items)

print('\n')
# Выводим ключи и соответствующие значения
for keys, value in while_dict.items():
    print(f"{keys}: {value}")

## Если отдельное каждое значение
for key, value in while_dict.items():
    print(f"{key}")
    if isinstance(value, list): ## Если значение список
        for item in value:
            print(f" - {item}")
    else:
        print(f" - {value}")