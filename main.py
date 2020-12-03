import threading

from login import LogIn
from audio_controller import AudioController

import PySimpleGUI as sg


audio_controller = AudioController('Zoom.exe')
audio_controller.unmute()
audio_controller.set_volume(1)

sg.theme('Reddit')
sg.set_options(font=20)

# GUI definition
toggle_job = sg.Button('Start', size=(5, 1), key='job', enable_events=True)
toggle_vol = sg.Button('Mute', size=(7, 1), key='btn', enable_events=True)
layout = [
    [sg.Output(size=(31, 5), key='out'), sg.Text('Join delay value:'),
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

ex = LogIn()  # attempting loggin in
out_contents = []  # first messages to display on the Output elem
# finalize param causes startup slowness
window = sg.Window('Meeting automation', layout, finalize=True)
try:
    open('cookies.txt', 'rb')
    out_contents.append('> Successfully connected to Adservio.\n')
except FileNotFoundError:
    out_contents.append(
        '> Connection to Adservio failed,\n please enter your credentials.\n')
if audio_controller.process_volume() is None:
    out_contents.append('> No "Zoom.exe" process found, yet.\n')

out_contents = ''.join(out_contents)
window['out'].Update(out_contents)


def long_function():
    # separate to the GUI thread
    global t
    t = threading.Timer(interval=ex.join(), function=ex.join)
    t.start()


# main event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == 'vol':
        audio_controller.set_volume(values['vol']/10)

    if event == 'job':  # toggle job start/end + button text
        if toggle_job.get_text() == 'Start':
            toggle_job.Update(text='Stop')
            toggle_job.Update(button_color=('white', 'red'))
            long_function()
        else:
            toggle_job.Update(text='Start')
            toggle_job.Update(button_color=('white', 'DodgerBlue3'))
            t.cancel()
            print('> Canceled job.')

    if event == 'btn':  # toggle app mute/unmute
        if toggle_vol.get_text() == 'Mute':
            audio_controller.mute()
            toggle_vol.Update(text='Unmute')
            toggle_vol.Update(button_color=('white', 'red'))

        else:
            audio_controller.unmute()
            toggle_vol.Update(text='Mute')
            toggle_vol.Update(button_color=('white', 'DodgerBlue3'))

    if event == 'creds':  # promp for log in credentials
        mail = sg.popup_get_text('Mail')
        pwd = sg.popup_get_text('Password', password_char='*')
        if mail is not None and pwd is not None and mail != '' and pwd != '':
            print('> New credentials added!')
            ex = LogIn(mail=mail, pwd=pwd)
        else:
            print("> Failed to add credentials.")

    if event == 'cls':  # clear the Output elem of text
        window['out'].Update('')

    if event == 'd':  # delay value from Spinner elem
        print(f'> Delay set to {values["d"]}.')

window.close()
