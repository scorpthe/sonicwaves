"""
Split (part of Sonic Waves)

started 22.03.18
by Bushuev Ilya

updated 17.07.18

function: file => splitted
"""

import re

COMMENT = re.compile(r'(".*")') #'  "comment"  '
SPACE = re.compile(r'^\s*$') #' '
MARK = re.compile(r'^\s*@(\w*)\s*$') #'  @any_name  '
TEMPO = re.compile(r'^\s*tempo\s*=\s*(\d{2,3})\s*$') #' tempo = 120 '
VALUE = re.compile(r'^\s*value\s*=\s*(\d{1,2})\s*$') #' value = 16 '
VOLUME = re.compile(r'^\s*volume\s*=\s*(\d{1,3})\s*$') #' volume = 100 '
WAVES = re.compile(r'^\s*waves\s*=\s*([qwer]+)\s*$') #' wave = qwer '
FOR = re.compile(r'^\s*FOR\s*$') #' FOR '
REP = re.compile(r'^\s*REP\s*=\s*(\d{1,3})\s*$') #' REP = 16 '
VAL = r'[CDEFGAH][#b]?[0-9]'
DUR = r'|\*\d{1,2}|/\d{1,2}|:\d{1,2}' # *n /n :n
NOTE = re.compile(r'^\s*('+VAL+')('+DUR+')\s*$') #' A4/2 '
CHORD = re.compile(r'^\s*([(](?:(?:'+VAL+'))(?:[ ](?:'+VAL+'))*[)])('+
                   DUR+')\s*$') #' (A4E4)/2 '
PAUSE = re.compile(r'^\s*P('+DUR+')\s*$') #' P/2 '

class SplitError(Exception):
    pass

class RepeatError(Exception):
    pass
    
def split(text, echo=True):
    if echo: print('\nSplit: your text\n',text)
    text = COMMENT.sub('', text)
    if echo: print('\nSplit: text w/o comments\n',text)
    sep = re.split(r',*', text)
    if echo: print('\nSplit: separated text\n',sep)
    res = []
    repcount = 0
    try:
        for el in sep:
            add = None
            if SPACE.search(el):
                pass
            elif MARK.search(el):
                add = ('mark', MARK.search(el).group(1))
            elif TEMPO.search(el):
                add = ('tempo', int(TEMPO.search(el).group(1)))
            elif VALUE.search(el):
                add = ('value', int(VALUE.search(el).group(1)))
            elif VOLUME.search(el):
                add = ('volume', int(VOLUME.search(el).group(1)))
            elif WAVES.search(el):
                add = ('waves', WAVES.search(el).group(1))
            elif FOR.search(el):
                add = ('for',)
                repcount+=1
            elif REP.search(el):
                add = ('rep', int(REP.search(el).group(1)))
                repcount-=1
            elif NOTE.search(el):
                add = ('note', NOTE.search(el).group(1), 
                       NOTE.search(el).group(2))
            elif CHORD.search(el):
                add = ('chord', 
                       tuple(CHORD.search(el).group(1)[1:-1].split()),
                       CHORD.search(el).group(2))
            elif PAUSE.search(el):
                add = ('pause', PAUSE.search(el).group(1))
            else:
                raise SplitError(el)
            if add:
                res.append(add)
        if repcount != 0:
            raise RepeatError()
        if echo: print('\nSplit: command list\n',res)
    except SplitError as er:
        print('Split: error in expression <{0}>'.format(er.args[0]))
        res = 0
    except RepeatError:
        print('Split: unfinushed repeat section')
        res = 0
    return res

def _test():
    with open('music', 'r') as file:
        text = file.read()
    split(text)

if __name__ == '__main__':
    _test()