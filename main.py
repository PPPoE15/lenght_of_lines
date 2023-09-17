import re
import PySimpleGUI as sg



buf = [[], [], []]

cut_lenght = 0
is_cut = False


def rnd(num):
    return int(num + (0.5 if num > 0 else -0.5))







layout = [
    [sg.Text('Выберете файл, содержащий g-code:')],
    [sg.Text('Путь:'), sg.InputText(key='-PATH-'), sg.FileBrowse('Выбрать')],
    [sg.Submit('Загрузить параметры')],
    [sg.Text(' ')],
    [sg.Button('Просмотреть G-code'), sg.Button('Старт') , sg.Cancel('Выход')],
    [sg.Output(size=(100, 20))]
]


window = sg.Window('ЧПУ станок для нанесения герметика', layout)

while True:                             # The Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Выход':
        break
    #print(event, values) #debug
    path = values['-PATH-']

    if event == 'Загрузить параметры':
        print('Загружено')

    if event == 'Просмотреть G-code':
        print('G-code:\n')
        with open(path) as gcode:
            for line in gcode:
                line = line.strip()
                command = re.findall(r'[MG].?\d+.?\d+', line)
                command = str(command).strip("'[]'")
                buf[0].append(command)

                x_coord = re.findall(r'X+(\d*\.\d+|\d+)?', line)
                x_coord = str(x_coord).strip("'[GMXY]'")
                if x_coord == '':
                    x_coord = '0'
                x_coord = float(x_coord)
                buf[1].append(x_coord)

                y_coord = re.findall(r'Y+(\d*\.\d+|\d+)?', line)
                y_coord = str(y_coord).strip("'[GMXY]'")
                if y_coord == '':
                    y_coord = '0'
                y_coord = float(y_coord)
                buf[2].append(y_coord)

                print(command + '\t' + str(x_coord) + '\t' + str(y_coord))
                # print(line)

        print('Обработка завершена\n')

    if event == 'Старт':
        for i in range(len(buf[0])):
            match buf[0][i]:
                case "G21":
                    print(str(i) + ' Режим работы в метрической системе')

                    # print('done')


                case "G90":
                    print(str(i) + ' Задание абсолютных координат')



                case "G00":  # send 1
                    print(str(i) + ' Холостой ход')
                    #ser.write(b'1' + buf[1][i] + buf[2][i])  # send command + x-coord + y-coord
                    x_coord = buf[1][i]
                    y_coord = buf[2][i]


                case "M09":  # send 2
                    is_cut = True
                    print(str(i) + ' Подача воздуха')





                case "G01":  # send 3
                    print(str(i) + ' Рабочее перемещение')
                    cut_lenght += ((abs(x_coord - buf[1][i]))**2 + (abs(y_coord - buf[2][i]))**2)**0.5
                    #ser.write(b'3' + buf[1][i] + buf[2][i])  # send command + x-coord + y-coord
                    x_coord = buf[1][i]
                    y_coord = buf[2][i]


                case "M10":  # send 4
                    is_cut = False
                    print(str(i) + ' Прекращение подачи воздуха')


                case "M02":  # send 5
                     print(str(i) + ' Конец программы')


                case _:
                    print(str(i) + ' Ошибка! Неизвестная команда')
    print(cut_lenght)

window.close()
