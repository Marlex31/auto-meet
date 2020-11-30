import PySimpleGUI as sg
from audio_controller import AudioController

audio_controller = AudioController('firefox.exe')
audio_controller.set_volume(1)


sg.theme('Reddit')

toggle_vol = sg.Button('Unmuted', size=(7, 2), key='btn', enable_events=True)
layout = [[sg.Slider(range=(0, 10),
                     default_value=10,
                     size=(20, 15),
                     orientation='horizontal',
                     font=('Helvetica', 12),
                     enable_events=True,
                     key='vol'
                     ), toggle_vol]]

window = sg.Window('Meeting automation', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'vol':
        audio_controller.set_volume(values['vol']/10)
    if event == 'btn':
        if toggle_vol.get_text() == 'Unmuted':
            audio_controller.mute()
            toggle_vol.Update(text='Muted')
        else:
            audio_controller.unmute()
            toggle_vol.Update(text='Unmuted')

window.close()
