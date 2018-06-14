"""
Sonic (as part of Sonic Waves)

started 11.06.18
by Bushuev Ilya

updated 25.06.18

function: hz => sound
"""

from math import pi, sin, asin, tan, atan, cos, ceil, floor
import pyaudio as pa
import array as ar

def sgn(x):
    res = None
    if x > 0:
        res = 1
    elif x < 0:
        res = -1
    else:
        res = 0
    return res
        
"""
2*pi*f*t   2*pi*t   1     f         sr
-------- = ------; --- = ----; w = ----;
   sr        w      w     sr        f

saw
(2*20/pi)*atan(tan(2*pi*x*440/(2*44100)))

sine
20 * sin(2*pi*440*x/44100)

trinagle
2*20/pi*asin(sin(2*pi*440*x/44100))

square
20* sign(sin(2*pi*440*x/44100))
"""
        
class Sonic:
    def wave(self, frequencies, time, amplitude, wave):
        mix = 0
        if type(frequencies) != list:
            frequencies = [frequencies]
        for frequency in frequencies:
            mix += wave(frequency, time, amplitude)
        return mix
    
    def wavelength(self, frequency):
        return round(self.sample_rate/frequency)
    
    def sine(self, frequency, time, amplitude):
        wavelength = self.wavelength(frequency)
        res = amplitude*sin(2*pi*time/wavelength)
        return res
    
    def saw(self, frequency, time, amplitude):
        wavelength = self.wavelength(frequency)
        res = (2*amplitude/pi)*atan(tan(2*pi*time/(2*wavelength)))
        return res
    
    def square(self, frequency, time, amplitude):
        wavelength = self.wavelength(frequency)
        #res = amplitude if time % wavelength < (wavelength//2) else -amplitude
        res = amplitude*sgn(sin(2*pi*time/wavelength))
        return res
    
    def trinagle(self, frequency, time, amplitude):
        wavelength = self.wavelength(frequency)
        res = 2*amplitude/pi*asin(sin(2*pi*time/wavelength))
        return res
    
    def __init__(self, bit=8, channels=2, rate=44100, echo=False):
        if bit == 8:
            pa_format = pa.paInt8
            self.array_format = 'h' 
        elif bit == 16:
            pa_format = pa.paInt16
            self.array_format = 'i'
        else:
            if bit != 32:
                print('Sonic: unsupported bit depth {} '.format(bit)+ 
                      'replaced by 32 bit')
                bit = 32
            pa_format = pa.paInt32
            self.array_format = 'l'
        self.pyaudio = pa.PyAudio()
        self.stream = self.pyaudio.open(format=pa_format, channels=channels,
                                        rate=rate, output=True)
        self.sample_rate = rate
        self.bit_volume = 2 ** bit
        self.echo = echo
        self.wave_functions = [self.sine, self.saw, 
                               self.square, self.trinagle]
        self.wave_functions = {'sine':self.sine, 
                               'saw':self.saw, 
                               'square':self.square, 
                               'trinagle':self.trinagle}
        if self.echo: print('Sonic: opened')
    
    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()
        if self.echo: print('Sonic: closed')
    
    def make_samples(self, frequencies, duration, volume, wave):
        try:
            wave = self.wave_functions[wave]
        except (KeyError, ValueError, IndexError):
            print('Sonic: unknown wave function {} '.format(wave)+
                  'replaced by sine')
            wave = self.sine
        amplitude = self.bit_volume * volume
        length = round(self.sample_rate * duration)
        samples = [round(self.wave(frequencies, time, amplitude, wave))
                   for time in range(length)]
        #print([i//10 for i in samples[0:100:10]])
        return samples
    
    def sound(self, frequencies, duration=1, volume=.1, wave='sine'):
        samples = self.make_samples(frequencies, duration, volume, wave)
        data = ar.array(self.array_format, samples).tobytes()
        self.stream.write(data)

def _test():
    sg = Sonic(echo=True)
    music = [440]
    sg.sound(music, duration=1, wave='sine')
    sg.sound(music, duration=1, wave='trinagle')
    sg.sound(music, duration=1, wave='saw')
    sg.sound(music, duration=1, wave='square')

if __name__ == '__main__':
    _test()