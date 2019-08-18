"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""
"""

0                             CHUNK//2                        CHUNK
+-------+-------+-------+-------+-------+-------+-------+-------+
              CHUNK//4                  
           <--CHUNK//8
             CHUNK//8-->

"""
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy.signal import detrend, cheby1, cheby2, butter, sosfiltfilt, sosfilt, lfilter, filtfilt, find_peaks, flattop, tukey, triang, nuttall, general_gaussian, blackmanharris, hamming, hann
import time
import sys
import array
import threading

#
user_freq = [697.0, 770.0, 852.0, 941.0,
             1209.0, 1336.0, 1477.0, 1633.0]
user_tones = {
    '1': (user_freq[0], user_freq[4]),
    '2': (user_freq[0], user_freq[5]),
    '3': (user_freq[0], user_freq[6]),
    'A': (user_freq[0], user_freq[7]),
    '4': (user_freq[1], user_freq[4]),
    '5': (user_freq[1], user_freq[5]),
    '6': (user_freq[1], user_freq[6]),
    'B': (user_freq[1], user_freq[7]),
    '7': (user_freq[2], user_freq[4]),
    '8': (user_freq[2], user_freq[5]),
    '9': (user_freq[2], user_freq[6]),
    'C': (user_freq[2], user_freq[7]),
    '*': (user_freq[3], user_freq[4]),
    '0': (user_freq[3], user_freq[5]),
    '#': (user_freq[3], user_freq[6]),
    'D': (user_freq[3], user_freq[7]),
}
op_freq = [700.0, 900.0, 1100.0, 1300.0, 1300.0, 1500.0, 1700.0]

op_tones = {
    '1': (op_freq[0], op_freq[1]),
    '2': (op_freq[0], op_freq[2]),
    '3': (op_freq[1], op_freq[2]),
    '4': (op_freq[0], op_freq[3]),
    '5': (op_freq[1], op_freq[3]),
    '6': (op_freq[2], op_freq[3]),
    '7': (op_freq[0], op_freq[4]),
    '8': (op_freq[1], op_freq[4]),
    '9': (op_freq[2], op_freq[4]),
    '0': (op_freq[3], op_freq[4]),  # 0 or "10"
    'A': (op_freq[3], op_freq[4]),  # 0 or "10"
    'B': (op_freq[0], op_freq[5]),  # 11 or ST3
    'C': (op_freq[1], op_freq[5]),  # 12 or ST2
    'D': (op_freq[2], op_freq[5]),  # KP
    'E': (op_freq[3], op_freq[5]),  # KP2
    'F': (op_freq[4], op_freq[5]),  # ST
}

#
WIDTH = 2
CHANNELS = 2
RATE = 48000
CHUNK = 4096

WINDOW_HALF_WIDTH = CHUNK//12
LOW_FREQ_POINT = CHUNK//3-WINDOW_HALF_WIDTH
HIGH_FREQ_POINT = CHUNK//3+WINDOW_HALF_WIDTH

FFT_NEW_XAXIS = RATE//1000//2

x = np.arange(10000)
y = np.random.randn(10000)

# disable matplotlib key shortcut
plt.rcParams['keymap.xscale']=''
plt.rcParams['keymap.yscale']=''

fig = plt.figure()

ax1 = plt.subplot(311)
ax2 = plt.subplot(312)
ax3 = plt.subplot(325)
ax4 = plt.subplot(326)

plt.set_loglevel("info") 
#fig.subplots_adjust(hspace=0.5)

class Station_Cursor(object):
    def __init__(self, ax):
        global LOW_FREQ_POINT
        global HIGH_FREQ_POINT
        self.ax = ax
        self.v1 = ax.axvline(LOW_FREQ_POINT,color='red',ls='--')  # 
        self.v2 = ax.axvline(HIGH_FREQ_POINT,color='red',ls='--')  # 

        # text location in axes coords
        #self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)
        self.keyPressed = False
        #print('init')

    def onrelease(self, event):
        self.keyPressed = False
    def onpress(self, event):
        if event.inaxes is not new_axis_1_0:
            return
        self.keyPressed = True
        global LOW_FREQ_POINT
        global HIGH_FREQ_POINT
        if event.inaxes is not None:
            pointer_at_ratio = event.xdata/FFT_NEW_XAXIS
            new_middle_sample_point = (CHUNK//2) * pointer_at_ratio
            if new_middle_sample_point + WINDOW_HALF_WIDTH > (CHUNK//2):
                new_middle_sample_point = (CHUNK//2) - WINDOW_HALF_WIDTH
            elif new_middle_sample_point - WINDOW_HALF_WIDTH < 0:
                new_middle_sample_point = WINDOW_HALF_WIDTH
            #print(new_middle_sample_point)
            LOW_FREQ_POINT = int(new_middle_sample_point - WINDOW_HALF_WIDTH)
            HIGH_FREQ_POINT = int(new_middle_sample_point + WINDOW_HALF_WIDTH)
            self.v1.set_xdata(LOW_FREQ_POINT)
            self.v2.set_xdata(HIGH_FREQ_POINT)
            v3.set_xdata(LOW_FREQ_POINT)
            v4.set_xdata(HIGH_FREQ_POINT)
            #self.txt.set_text('center at = %1.2f kHz' % (pointer_at_ratio*(RATE//1000//2)))
            #print('event')
    def onmotion(self, event):
        global LOW_FREQ_POINT
        global HIGH_FREQ_POINT
        if self.keyPressed is False:
            return
        if event.inaxes is not None:
            pointer_at_ratio = event.xdata/FFT_NEW_XAXIS
            new_middle_sample_point = (CHUNK//2) * pointer_at_ratio
            if new_middle_sample_point + WINDOW_HALF_WIDTH > (CHUNK//2):
                new_middle_sample_point = (CHUNK//2) - WINDOW_HALF_WIDTH
            elif new_middle_sample_point - WINDOW_HALF_WIDTH < 0:
                new_middle_sample_point = WINDOW_HALF_WIDTH
            #print(new_middle_sample_point)
            LOW_FREQ_POINT = int(new_middle_sample_point - WINDOW_HALF_WIDTH)
            HIGH_FREQ_POINT = int(new_middle_sample_point + WINDOW_HALF_WIDTH)
            self.v1.set_xdata(LOW_FREQ_POINT)
            self.v2.set_xdata(HIGH_FREQ_POINT)
            v3.set_xdata(LOW_FREQ_POINT)
            v4.set_xdata(HIGH_FREQ_POINT)
            #self.txt.set_text('center at = %1.2f kHz' % (pointer_at_ratio*(RATE//1000//2)))
            #print('event')

command_is_sending=False
def stream_write(commands, stream2):
    global command_is_sending
    command_is_sending=True
    tone_set = user_tones
    sr = RATE
    length = 0.1
    volume = 0.3
    for char in commands:
        tone = tone_set[char]
        stream_output = array.array('f',
            ((volume * np.sin(2.0 * np.pi * i * tone[0] / float(sr)) + volume * np.sin(2.0 * np.pi * i * tone[1] / float(sr)))
                for i in range(int(sr*length)))).tobytes()
        stream2.write(stream_output)
        time.sleep(0.25)
    command_is_sending=False

# key event
stream2=0
cursor_middle_point_freq=0
commands=""
old_commands=""
old_freq=0
digits=""
old_digits=""
def keypress(event):
    global stream2
    global cursor_middle_point_freq
    global commands
    global old_commands
    global old_freq
    global digits
    global old_digits
    global command_is_sending
    global frame_process_finish
    sys.stdout.flush()
    
    if command_is_sending:
        return

    key_from_event = event.key
    
    print(key_from_event)
    if key_from_event == "enter":
        if digits == "":
            if old_digits == "":
                return
            digits = old_digits
        print(digits)
        old_digits=digits
        freq=int(digits)
        digits=""
        freq = freq - (cursor_middle_point_freq*1000)
        if freq < 0:
            freq = 0
        if freq > 0 and freq < 30000000:
            old_freq = freq
            commands = str(int(freq)) + "#"
    elif key_from_event.lower() == "k":
        if digits == "":
            if old_digits == "":
                return
            digits = old_digits
        else:
            digits += "000"
        print(digits)
        old_digits=digits
        freq=int(digits)
        digits=""
        freq = freq - (cursor_middle_point_freq*1000)
        if freq < 0:
            freq = 0
        if freq > 0 and freq < 30000000:
            old_freq = freq
            commands = str(int(freq)) + "#"
    elif key_from_event.lower() == "m":
        if digits == "":
            if old_digits == "":
                return
            digits = old_digits
        else:
            digits += "000000"
        print(digits)
        old_digits=digits
        freq=int(digits)
        digits=""
        freq = freq - (cursor_middle_point_freq*1000)
        if freq < 0:
            freq = 0
        if freq > 0 and freq < 30000000:
            old_freq = freq
            commands = str(int(freq)) + "#"
    elif key_from_event == "up":
        commands="2*"
    elif key_from_event == "left":
        commands="4*"
    elif key_from_event == "right":
        commands="6*"
    elif key_from_event == "down":
        commands="8*"
    else:
        if key_from_event.isdigit():
            digits = digits + key_from_event
            
    if commands != "":
        #
        #
        t = threading.Thread(target = stream_write(commands, stream2))
        t.start()
        commands=""
        
        #
        """
        command_is_sending=True
        stream_write(commands, stream2)
        commands=""
        command_is_sending=False
        """
        """
        tone_set = user_tones
        sr = RATE
        length = 0.1
        volume = 0.5         
        for char in commands:
            tone = tone_set[char]
            stream_output = array.array('f',
                ((volume * np.sin(2.0 * np.pi * i * tone[0] / float(sr)) + volume * np.sin(2.0 * np.pi * i * tone[1] / float(sr)))
                    for i in range(int(sr*length)))).tobytes()
            stream2.write(stream_output)
            time.sleep(0.25)
        command_is_sending=False
        
        commands=""
        """
#
#
li2, = ax1.plot(x, y)
ax1.set_xlim(0,(CHUNK//2))
ax1.xaxis.set_visible(False)
ax1.set_ylim(0,10)
ax1.set_title("Fast Fourier Transform")
new_axis_1_0 = inset_axes(ax1,height="100%",width="100%",loc='center')
new_axis_1_0.set_xlim([0,FFT_NEW_XAXIS])
new_axis_1_0.yaxis.set_visible(False)
new_axis_1_0.set_frame_on(False)
cursor = Station_Cursor(ax1)
fig.canvas.mpl_connect('key_press_event', keypress)
fig.canvas.mpl_connect('button_press_event', cursor.onpress)
fig.canvas.mpl_connect('button_release_event', cursor.onrelease)
fig.canvas.mpl_connect('motion_notify_event', cursor.onmotion)
peak_txt = ax1.text(0, 0, '')
peak_marker, = ax1.plot([0],[0],'r*')

#v1 = ax[0].axvline(LOW_FREQ_POINT,color='red',ls='--')
#v2 = ax[0].axvline(HIGH_FREQ_POINT,color='red',ls='--')

#
Z=np.zeros((32,CHUNK//2+1))
im = ax2.imshow(Z, aspect='auto', interpolation='bilinear', cmap='inferno')
ax2.set_xlim(0-10,(CHUNK//2)+10)
ax2.set_ylim(0,32)
ax2.set_title("Waterfall")
ax2.xaxis.set_visible(False)
ax2.yaxis.set_visible(False)
v3 = ax2.axvline(LOW_FREQ_POINT,color='white',ls='--')
v4 = ax2.axvline(HIGH_FREQ_POINT,color='white',ls='--')

#
li, = ax3.plot(x, y)
ax3.set_xlim(0-10,(CHUNK//4)+10)
ax3.set_ylim(0,10)
ax3.set_title("Windowed FFT")

#
li3, = ax4.plot(x,y)
ax4.set_xlim(0-50,CHUNK+50)
ax4.set_ylim(-35000,35000)
ax4.set_title("Output")


# try to findout the audio input
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))
    #print(p.get_device_info_by_index(i)['index'],p.get_device_info_by_index(i)['name'])
    if "USB" in p.get_device_info_by_index(i)['name'] and p.get_device_info_by_index(i)['maxInputChannels'] > 0:
        INPUT_DEVICE = p.get_device_info_by_index(i)['index']
        print(p.get_device_info_by_index(i))
        print("INPUT_DEVICE=",INPUT_DEVICE)
        break
for i in range(p.get_device_count()):
    #print(p.get_device_info_by_index(i))
    #print(p.get_device_info_by_index(i)['index'],p.get_device_info_by_index(i)['name'])
    if "USB" in p.get_device_info_by_index(i)['name'] and p.get_device_info_by_index(i)['maxOutputChannels'] > 0:
        OUTPUT_DEVICE = p.get_device_info_by_index(i)['index']
        print(p.get_device_info_by_index(i))
        print("OUTPUT_DEVICE=",OUTPUT_DEVICE)
        break
#OUTPUT_DEVICE = 2
try: INPUT_DEVICE
except NameError: sys.exit()
try: OUTPUT_DEVICE
except NameError: sys.exit()

# process i-q signal
frame_process_finish = False
def callback(in_data, frame_count, time_info, status):
    global frame_process_finish
    global dfft
    global ifft
    global fft_shift
    global fft_cut
    global peak_pos
    global peak_value
    global filtered
    global last_head
    global left_peak_pos
    global left_peak_value
    global right_peak_pos
    global right_peak_value
    global solid_dfft
    global solid_fft_cut
    global solid_filtered
    if status:
        print("Playback Error: %i" % status)
    # raw data fetch
    raw = np.frombuffer(in_data, np.int16)
    result = np.reshape(raw, (CHUNK, CHANNELS))
    result = result.astype(np.int32)
    # I-Q data fetch
    left_input = result[:,0]
    right_input = result[:,1]
    # I-Q demodulation directly
    buffer = np.sqrt(np.power(left_input, 2) + np.power(right_input, 2))
    
    # fft and normalize
    dfft_from_IQ_demod = np.fft.rfft(buffer ,norm = 'ortho')  # CHUNK
    #fft_shift = dfft
    left_dfft = np.fft.rfft(left_input ,norm = 'ortho')  # CHUNK
    right_dfft = np.fft.rfft(right_input ,norm = 'ortho')  # CHUNK
    # for display
    dfft = left_dfft + right_dfft
    
    # find the peak point(carrier)
    left_loged_shifted_fft = np.log10(left_dfft[LOW_FREQ_POINT:HIGH_FREQ_POINT]+0.001)
    left_peak_pos = np.argmax(left_loged_shifted_fft)
    left_peak_value = np.absolute(np.amax(left_loged_shifted_fft))
    right_loged_shifted_fft = np.log10(right_dfft[LOW_FREQ_POINT:HIGH_FREQ_POINT]+0.001)
    right_peak_pos = np.argmax(right_loged_shifted_fft)
    right_peak_value = np.absolute(np.amax(right_loged_shifted_fft))
    
    # spectrum segment and agc
    # ((10**2)/peak_value)
    left_fft_cut = ((10**2.1)/left_peak_value) * left_dfft[LOW_FREQ_POINT+left_peak_pos:HIGH_FREQ_POINT]
    right_fft_cut = ((10**2.1)/right_peak_value) * right_dfft[LOW_FREQ_POINT+right_peak_pos:HIGH_FREQ_POINT]
    #left_fft_cut = ((10**1)/left_peak_value) * left_dfft[LOW_FREQ_POINT+left_peak_pos:HIGH_FREQ_POINT]
    #right_fft_cut = ((10**1)/right_peak_value) * right_dfft[LOW_FREQ_POINT+right_peak_pos:HIGH_FREQ_POINT]
    
    # reshape freq domain data
    if len(left_fft_cut) > 0:
        left_fft_cut[:int(len(left_fft_cut)*0.1)] = left_fft_cut[:int(len(left_fft_cut)*0.1)] * np.linspace(0.00001,1,int(len(left_fft_cut)*0.1))
    if len(right_fft_cut) > 0:
        right_fft_cut[:int(len(right_fft_cut)*0.1)] = right_fft_cut[:int(len(right_fft_cut)*0.1)] * np.linspace(0.00001,1,int(len(right_fft_cut)*0.1))
    min_np_array_size = min(len(left_fft_cut),len(right_fft_cut))
    # for display
    fft_cut = left_fft_cut[:min_np_array_size] + right_fft_cut[:min_np_array_size]
    
    # inverse fft
    ifft = np.fft.irfft(a=fft_cut , n=CHUNK ,norm = 'ortho')
    # inverse fft from left only
    #ifft = np.fft.irfft(a=left_fft_cut , n=CHUNK ,norm = 'ortho')
    # inverse fft from IQ_demod directly
    #ifft = buffer
    
    
    # low frequency suppressing
    # nadpass filter
    #sos = cheby2(N=33, rs=55, Wn=[ 0.000125,0.5], btype='band', output='sos')
    #ifft = sosfilt(sos, ifft)
    
    # I Q signal demodulation
    #ifft_left = np.fft.irfft(a=left_fft_cut[:min_np_array_size] , n=CHUNK ,norm = 'ortho')
    #ifft_right = np.fft.irfft(a=right_fft_cut[:min_np_array_size] , n=CHUNK ,norm = 'ortho')
    #ifft = np.sqrt(np.power(ifft_left, 2) + np.power(ifft_right, 2))
    
    #ifft = ifft - np.average(ifft)
    
    #ifft = left_ifft
    
    # pops suppressing
    ifft[:150] =  ifft[:150] * np.linspace(0.00001,1,150)
    ifft[-150:] = ifft[-150:] * np.linspace(1,0.00001,150)
    
    filtered = np.empty(CHUNK*2)
    filtered[0::2]=ifft
    filtered[1::2]=ifft
    
    # solidify
    solid_dfft=np.log10(abs(dfft[:])+0.001)
    solid_fft_cut=np.log10(abs(fft_cut[:])+0.001)
    solid_filtered=filtered[:]
    # set flag
    frame_process_finish = True
    return (filtered.astype(np.int16).tostring(), pyaudio.paContinue)


# init input for i-q signal
stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK,
                input_device_index=INPUT_DEVICE,
                stream_callback=callback)

stream.start_stream()

# init output for DTMF
stream2 = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=True,
                output_device_index=OUTPUT_DEVICE)



time.sleep(0.1)
while stream.is_active():
    if frame_process_finish:
        try:
            # dfft,fft_cut,filtered are from frame process
            
            #
            #log_fft = np.log10(abs(solid_dfft)+0.001)
            log_fft = solid_dfft
            li2.set_xdata(np.arange(len(log_fft)))
            li2.set_ydata(log_fft)
            peak_pos = np.argmax(log_fft[LOW_FREQ_POINT:HIGH_FREQ_POINT])
            peak_value = np.absolute(np.amax(log_fft))
            peak_marker.set_data(LOW_FREQ_POINT+peak_pos,peak_value) #
            #if peak_value > 0:
                #peak_point_y_ratio = left_peak_value/(ax[0].get_ylim()[1]-ax[0].get_ylim()[0])
            #peak_marker.set_ydata(peak_value) #get_yticks()
            peak_txt.set_position((LOW_FREQ_POINT+peak_pos,peak_value))
            peak_point_x_ratio =(LOW_FREQ_POINT+peak_pos)/(ax1.get_xlim()[1]-ax1.get_xlim()[0])
            peak_offset_freq = (np.ceil((peak_point_x_ratio*(RATE//100//2)))/10)
            peak_txt.set_text(' {0:.1f} @{1:.1f} kHz'.format(peak_value,peak_offset_freq))
            cursor_middle_point_freq = (np.ceil(((LOW_FREQ_POINT+((HIGH_FREQ_POINT-LOW_FREQ_POINT)/2))/(ax1.get_xlim()[1]-ax1.get_xlim()[0])*(RATE//100//2)))/10)
            # waterfall
            Z = np.vstack((Z, log_fft))
            Z = np.delete(Z, 1, axis=0)
            im.set_data(Z)
            im.autoscale()
            
            #
            #log_fft_cut = np.log10(abs(solid_fft_cut)+0.001)
            log_fft_cut = solid_fft_cut
            li.set_xdata(np.arange(len(log_fft_cut)))
            li.set_ydata(log_fft_cut)
            #
            li3.set_xdata(np.arange(len(solid_filtered[0::2])))
            li3.set_ydata(solid_filtered[0::2])
            
            plt.pause(0.001)
            frame_process_finish = False
        except:
            pass
        else:
            pass
    #time.sleep(0.1)
    
stream.stop_stream()
stream.close()
stream2.stop_stream()
stream2.close()

p.terminate()
