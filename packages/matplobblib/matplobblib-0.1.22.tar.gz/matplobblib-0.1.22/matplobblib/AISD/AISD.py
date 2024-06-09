from .data_structures import *
from  .search_algorythms import *
from .additional_funcs import *

data1 = text1.split('abracadabrabibidi')
data_structures_dict = dict([(x.split('\n')[1].replace("# ",''),x) for x in data1])
data2 = text2.split('abracadabrabibidi')
search_algorythms_dict = dict([(x.split('\n')[1].replace("# ",''),x) for x in data2])
data3 = text3.split('abracadabrabibidi')
additional_funcs_dict = dict([(x.split('\n')[1].replace("# ",''),x) for x in data3])

themes = {
        'Структуры данных': list(data_structures_dict.keys()),
        'Алгоритмы сортировки': list(search_algorythms_dict.keys()),
        'Вывести функцию буфера обмена': ['enable_ppc'],
        'Дополнительные функции' : list(additional_funcs_dict.keys()),
              }

def description(dict_to_show = themes, show_only_keys:bool = True):
    if dict_to_show == themes:
        show_only_keys = False
    text = ""
    length1=1+max([len(x) for x in list(dict_to_show.keys())])
    for key in dict_to_show.keys():
        text += f'{key:^{length1}}'
        if not show_only_keys:
            text +=': '
            for f in dict_to_show[key]:
                text += f'{f};\n'+' '*(length1+2)
        text += '\n'
    if dict_to_show == themes:
        print(text)
    else:
        return text

def enable_ppc():
    return '''    import pyperclip

    #Делаем функцию которая принимает переменную text
    def write(name):
        pyperclip.copy(name) #Копирует в буфер обмена информацию
        pyperclip.paste()'''

def data_structures(key=None):
    if key == None:
        print(description(data_structures_dict))
    else:
        try:
            return data_structures_dict[key]
        except:
            print('Ошибка поиска. Структура данных должна быть среди этих:\n')
            print(description(data_structures_dict))
            
def search_algorythms(key=None):
    if key == None:
        print(description(search_algorythms_dict))
    else:
        try:
            return search_algorythms_dict[key]
        except:
            print('Ошибка поиска. Алгоритм поиска должен быть среди этих:\n')
            print(description(search_algorythms_dict))