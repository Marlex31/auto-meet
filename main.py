import threading

from login import LogIn

import PySimpleGUI as sg
from audio_controller import AudioController


audio_controller = AudioController('Zoom.exe')
audio_controller.unmute()
audio_controller.set_volume(1)


sg.theme('Reddit')
sg.set_options(font=20)

toggle_job = sg.Button('Start', size=(5, 1), key='job', enable_events=True)
toggle_vol = sg.Button('Mute', size=(7, 1), key='btn', enable_events=True)
layout = [
    [sg.Output(size=(30, 5), key='out'), sg.Text('Join delay value:'),
     sg.Spin(values=list(range(15)), initial_value=0, size=(2, 2),
             key='d', enable_events=True),
     sg.Text('mins')],
    [sg.Slider(range=(0, 10),
               default_value=10,
               size=(20, 15),
               orientation='horizontal',
               font=('Helvetica', 12),
               enable_events=True,
               key='vol'
               ),
     toggle_job,
     toggle_vol,
     sg.Button('Add credentials',
               enable_events=True,
               key='creds'),
     sg.Button('Clear', enable_events=True, key='cls')]]

window = sg.Window('Meeting automation', layout, finalize=True)
try:
    open('cookies.txt', 'rb')
    window['out'].Update('Connection successful with Adservio.')
except FileNotFoundError:
    window['out'].Update('Connection to Adservio failed, please enter your credentials.\n')

ex = LogIn()


def long_function():
    global t
    t = threading.Timer(interval=ex.join(), function=ex.join)
    t.start()


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == 'vol':
        audio_controller.set_volume(values['vol']/10)

    if event == 'job':
        if toggle_job.get_text() == 'Start':
            toggle_job.Update(text='Stop')
            toggle_job.Update(button_color=('white', 'red'))
            long_function()
        else:
            toggle_job.Update(text='Start')
            toggle_job.Update(button_color=('white', 'DodgerBlue3'))
            t.cancel()
            print('Canceled job.')

    if event == 'btn':
        if toggle_vol.get_text() == 'Mute':
            audio_controller.mute()
            toggle_vol.Update(text='Unmute')
            toggle_vol.Update(button_color=('white', 'red'))

        else:
            audio_controller.unmute()
            toggle_vol.Update(text='Mute')
            toggle_vol.Update(button_color=('white', 'DodgerBlue3'))

    if event == 'creds':
        mail = sg.popup_get_text('Mail')
        pwd = sg.popup_get_text('Password', password_char='*')
        if mail is not None and pwd is not None and mail != '' and pwd != '':
            print('New credentials added!')
            ex = LogIn(mail=mail, pwd=pwd)
        else:
            print("Failed to add credentials.")

    if event == 'cls':
        window['out'].Update('')

    if event == 'd':
        print(f'Delay set to {values["d"]}.')

window.close()
