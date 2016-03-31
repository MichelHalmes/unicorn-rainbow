import random

from _base_classes import Animation

PIX_PER_CHAR = 8

class TextBanner(Animation):
    RESET_RGB = None
    NB_CYCLES_PER_ANIMATION = 10
    

    def __init__(self, rainbow):
        super(self.__class__, self).__init__(rainbow)
        self._cnst_angular_speed = False
        
        message = random.choice(MESSAGES)

        for part in self.get_parts():
            self.get_data(part)['string'] = '-'*self.MAX_PART_LEN

        for char in message.upper():
            pixels = CHARACTERS[char].split('\n')[1:]
            
            for part in self.get_parts():
                string = pixels[part._id]
                assert len(string)==PIX_PER_CHAR or char in ' !?-'
                self.get_data(part)['string']+= string + '----'

        # for part in self.get_parts():
        #     self.get_data(part)['string'] += '-'*self.MAX_PART_LEN

    def run_period(self, part, period_cnt):
        part.set_uniform_color((0,0,0))

        idx = period_cnt
        string = self.get_data(part)['string'][idx: idx+self.MAX_PART_LEN-1]
        if len(string)==1:
            raise StopIteration

        for string_idx, char in enumerate(string):
            if char != '#':
                continue

            led_idx = int(round(1.*string_idx*part._length/self.MAX_PART_LEN))
            part.set_led_color(led_idx,  (255,255,255))



MESSAGES = [
"@EMELINE@!",
"AWEEE!!",
"Play!",
"AB 2017!",
"AFRIKABURN",
"RADICAL INCLUSION!",
"GIFTING!",
"DECOMMODIFICATION!",
"RADICAL SELF-RELIANCE!",
"RADICAL SELF-EXPRESSION!",
"COMMUNAL EFFORT!",
"CIVIC RESPONSIBILITY!",
"LEAVE NO TRACE!",
"PARTICIPATION!",
"IMMEDIACY!",
"EACH 1 TEACH 1!",
"GRATITUDE!",
"NO MOOP!"
]

CHARACTERS = {
'A': """
---##---
--#--#--
-#----#-
########
#------#
#------#
""",
'B': """
#######-
#------#
#-----#-
#######-
#------#
#######-
""",
'C': """
-#######
#-------
#-------
#-------
#-------
-######-
""",
'D': """
#####---
#-----#-
#------#
#------#
#-----#-
#####---
""",
'E': """
########
#-------
#-------
######--
#-------
########
""",
'F': """
-#######
#-------
#-------
######--
#-------
#-------
""",
'G': """
-#######
#-------
#-------
#---####
#------#
-######-
""",
'H': """
#------#
#------#
#------#
########
#------#
#------#
""",
'I': """
-######-
---#----
---#----
---#----
---#----
-######-
""",
'J': """
#######-
-------#
-------#
-------#
-#-----#
--#####-
""",
'K': """
#------#
#----#--
#--#----
##------
#--#----
#----#--
""",
'L': """
#-------
#-------
#-------
#-------
#-------
########
""",
'M': """
#------#
#-#--#-#
#--##--#
#------#
#------#
#------#
""",
'N': """
##-----#
#-#----#
#--#---#
#---#--#
#----#-#
#-----##
""",
'O': """
-######-
#------#
#------#
#------#
#------#
-######-
""",
'P': """
#######-
#------#
#------#
#######-
#-------
#-------
""",
'Q': """
-######-
#------#
#------#
#---#--#
#----##-
-####--#
""",
'R': """
#######-
#------#
#------#
######--
#--#----
#----#--
""",
'S': """
-#######
#-------
#-------
-######-
-------#
#######-
""",
'T': """
########
---#----
---#----
---#----
---#----
---#----
""",
'U': """
#------#
#------#
#------#
#------#
#------#
-######-
""",
'V': """
#------#
-#----#-
-#----#-
--#--#--
--#--#--
---##---
""",
'W': """
#------#
#------#
#------#
#--##--#
#-#--#-#
#------#
""",
'X': """
#------#
--#--#--
---##---
---##---
--#--#--
#------#
""",
'Y': """
#------#
--#--#--
---##---
---#----
---#----
---#----
""",
'Z': """
########
-----#--
----#---
---#----
--#-----
########
""",
'0': """
-######-
#----#-#
#---#--#
#--#---#
#-#----#
-######-
""",
'1': """
---##---
--#-#---
-#--#---
----#---
----#---
--#####-
""",
'2': """
-######-
#------#
------#-
-----#--
----#---
--######
""",
'3': """
-######-
-------#
-------#
---####-
-------#
-######-
""",
'4': """
---#---#
--#----#
-#-----#
########
-------#
-------#
""",
'5':"""
########
#-------
#-------
#######-
-------#
-######-
""",
'6':"""
----##--
---#----
--#-----
-######-
#------#
-######-
""",
'7': """
########
-------#
------#-
----###-
----#---
---#----
""",
'8':"""
-######-
#------#
-#----#-
--####--
#------#
-######-
""",
'9': """
-######-
#------#
-######-
-----#--
----#---
--##----
""",
'@': """
-##--##-
###--###
########
-######-
--####--
---#----
""",
' ': """
----
----
----
----
----
----
""",
'!': """
--#--
--#--
--#--
--#--
-----
--#--
""",
'?': """
--###--
-#---#-
----#--
---#---
-------
---#---
""",
'-': """
------
------
------
-####-
------
------
""",


}