"""
Sonic (part of Sonic Waves)

started 11.06.18
by Bushuev Ilya

updated 17.07.18

function: hz => sound
"""

from math import pi, sin, asin, tan, atan, cos, ceil, floor
import pyaudio as pa
import array as ar

# Math signum function
def sgn(x):
    res = None
    if x > 0:
        res = 1
    elif x < 0:
        res = -1
    else:
        res = 0
    return res


class Sonic:
    # e - sinE
    def make_sine(self, wavelength, time, amplitude):
        return amplitude*sin(2*pi*time/wavelength)
    
    # q - sQuare
    def make_square(self, wavelength, time, amplitude):
        return amplitude*sgn(sin(2*pi*time/wavelength))
    
    # r - tRingale
    def make_trinagle(self, wavelength, time, amplitude):
        return 2*amplitude/pi*asin(sin(2*pi*time/wavelength))
    
    # w - saWtooth
    def make_sawtooth(self, wavelength, time, amplitude):
        return (2*amplitude/pi)*atan(tan(2*pi*time/(2*wavelength)))
        
    def make_coefs(self, waves):
        coefs = dict.fromkeys(self.wave_functions, 0)
        try:
            waves = set(waves)
            value = 1/len(waves)
            for name in waves:
                if name in set(coefs.keys()):
                    coefs[name] = value
                else:
                    raise KeyError
        except (KeyError, ValueError, IndexError):
            print('Sonic: error in counting coefficients, replaced by sine')
            coefs = dict.fromkeys(coefs, 0)
            coefs['e'] = 1            
        if self.echo: print('Sonic: wave coefficients',coefs)
        return coefs
    
    def make_wavelength(self, frequency):
        return round(self.sample_rate/frequency)
    
    def make_mix(self, frequencies, amplitude, waves_coefs, time):
        mix = 0
        if type(frequencies) != list:
            frequencies = [frequencies]
        for frequency in frequencies:
            wavelength = self.make_wavelength(frequency)
            for name, function in self.wave_functions.items():
                mix += function(wavelength, time, amplitude*waves_coefs[name])
        return mix
    
    def __init__(self, bit=8, channels=2, rate=44100, echo=False):
        self.echo = echo
        if self.echo: print('Sonic: loading...')
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
        self.wave_functions = {'e':self.make_sine, 'q':self.make_square, 
                               'r':self.make_trinagle, 'w':self.make_sawtooth}
        self.data = []
        if self.echo: print('Sonic: ready to read!')
    
    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()
        if self.echo: print('Sonic: terminated.')
    
    def get_samples(self, frequencies, duration, volume, waves):
        amplitude = self.bit_volume * volume
        waves_coefs = self.make_coefs(waves)
        length = round(self.sample_rate * duration)
        samples = [round(self.make_mix(frequencies, amplitude, waves_coefs, time))
                   for time in range(length)]
        #print([i//10 for i in samples[0:100:10]])
        return samples
    
    def waves(self, frequencies, duration, volume=.1, waves='e', now=False):
        samples = self.get_samples(frequencies, duration, volume, waves)
        data = ar.array(self.array_format, samples).tobytes()
        if now:
            if self.echo: print('Sonic: live play!')
            self.stream.write(data)
        else:
            if self.echo: print('Sonic: writing data.')
            self.data.append(data)
    
    def play(self):
        if self.echo: print('Sonic: playing.')
        for data in self.data:
            self.stream.write(data)
        if self.echo: print('Sonic: finished.')
        
    def __show(self):
        print(dir(self))

def __test():
    sonic = Sonic(echo=True)
    sonic.waves(frequencies=[440,220,880],waves='qwer',duration=3)
    sonic.play()

if __name__ == '__main__':
    __test()
    
"""
Notice:
understanding wavelength
2*pi*f*t   2*pi*t   1     f         sr  
-------- = ------; --- = ----; w = ----;
   sr        w      w     sr        f   
when: 
    f -- frequency
    t -- time
    sr -- sample rate
    w -- wavelength

Drawing graphs with f = y(x)
saw
(2*20/pi)*atan(tan(2*pi*x*440/(2*44100)))
sine
20*sin(2*pi*440*x/44100)
trinagle
2*20/pi*asin(sin(2*pi*440*x/44100))
square
20*sign(sin(2*pi*440*x/44100))
"""