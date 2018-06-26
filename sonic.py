"""
Sonic (part of Sonic Waves)

started 11.06.18
by Bushuev Ilya

updated 03.07.18

function: hz => sound

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
            waves = set(waves.split())
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
        if self.echo: print(coefs)
        return coefs
    
    def make_wavelength(self, frequency):
        return round(self.sample_rate/frequency)
    
    def make_mix(self, frequencies, time):
        mix = 0
        if type(frequencies) != list:
            frequencies = [frequencies]
        for frequency in frequencies:
            wavelength = self.make_wavelength(frequency)
            for name, function in self.wave_functions.items():
                mix += function(wavelength, time, self._amplitude*self._coefs[name])
        return mix
    
    def __init__(self, bit=8, channels=2, rate=44100, echo=False):
        """
        array_format, pyaudio, stream, sample_rate, bit_volume, echo, wave_functions, 
        
        """
        self.echo = echo
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
        self.settings(volume=.1, waves='s')
        if self.echo: print('Sonic: opened')
    
    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()
        if self.echo: print('Sonic: closed')
    
    def get_samples(self, frequencies, duration):
        length = round(self.sample_rate * duration)
        samples = [round(self.make_mix(frequencies, time))
                   for time in range(length)]
        #print([i//10 for i in samples[0:100:10]])
        return samples
    
    def settings(self, volume, waves):
        self._amplitude = self.bit_volume * volume
        self._coefs = self.make_coefs(waves)
    
    def get_sound(self, frequencies, duration):
        samples = self.get_samples(frequencies, duration)
        data = ar.array(self.array_format, samples).tobytes()
        self.stream.write(data)
    
    def get_sound_full(self, frequencies, duration, volume, waves):
        self.settings(volume, waves)
        self.get_sound(frequencies, duration)
    
    def show(self):
        print(dir(self))

def _test():
    sn = Sonic(echo=True)
    #sn.show()
    music = [440]
    print('gs')
    sn.settings(.1,'q w e r')
    sn.get_sound(music,3)
    """
    print('gsf')
    sn.get_sound_full(music, duration=1, volume = .1, waves='q')
    sn.get_sound_full(music, duration=1, volume = .1, waves='w')
    sn.get_sound_full(music, duration=1, volume = .1, waves='e')
    sn.get_sound_full(music, duration=1, volume = .1, waves='r')
    """

if __name__ == '__main__':
    _test()