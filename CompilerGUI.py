from logging import disable
from kivy.config import Config
Config.set('kivy','window_icon','hacking.png')
from os import error
from typing import Text
import kivy
from kivy.app import App
from kivy.core import text
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
import pyperclip
from scanner import *
from tokentypes import *
from emiter import *
from myparser import *
import sys
from kivy.clock import Clock


def main(text):
    """ with open(sys.argv[1],'r') as inputfile:
        source = inputfile.read() """
    source = text
    lexer = Lexer(source)

    lexer2 = Lexer(source)
    emiter = Emiter()
    parser = Parser(lexer,emiter)
    token = lexer2.getToken()
    flag = False
    while True :
        if(token == None ):
            flag = True
            break
        if(token.tokenKind == Tokens.EOF):
            break

        token = lexer2.getToken()
    if (flag == False):
        #print("token list:")
        for i in lexer2.tokenList:
            pass
            #print(i.tokenText)
        #print("end")
        parser.program()
    
    if(lexer2.error is True):
        return 1
    elif(parser.error is True):
        return 2,lexer2.tokenList
    #print("EMITER GET CODE ARRIVED")
    return emiter.getCode(),lexer2.tokenList
    print(emiter.getCode())
    print("parser completed")


def showError_Popup(errorType):
    show = P() 
    popupWindow = Popup(title="Error", content=show, size_hint=(None,None),size=(400,400)) 
    app = App.get_running_app()
    if(errorType == 1 ):
        app.cError.text = "Scanner Error"
    elif(errorType == 2):
        app.goCButton.disabled = True
        app.cError.text = "Parser Error"
    popupWindow.open() 
class CompilerLayout(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def run(self,superRoot):
        #showError_Popup()
        count = 0
        response = main((self.ids.tinyCode.text))
        if(not isinstance(response,int)):
            response,tokenTableResponse = main(self.ids.tinyCode.text)
        app = App.get_running_app()
        app.goCButton.disabled = False
        if(response == 1):
            showError_Popup(response)
        else:
            app.c_code = response
            if(not isinstance(response,int)):
                app.cTextInput.text = str(response)
            else:
                showError_Popup(2)
            
            numberOfToken = Label(text="#")
            firstColName = Label(text="Token Name ")
            secondColName = Label(text="Token Value")
            app.table.clear_widgets()
            app.table.add_widget(numberOfToken)
            app.table.add_widget(firstColName)
            app.table.add_widget(secondColName)
            for i in tokenTableResponse:
                tokenNum = TextInput(text=str(count+1),disabled=True,size=(100,100),size_hint=(0.3,1))
                tname = TextInput(text=i.tokenText,disabled=True,size=(100,100),size_hint=(1,1))
                tval = TextInput(text=str(i.tokenKind),disabled=True,size=(100,100),size_hint=(0.3,1))
                app.table.add_widget(tokenNum)
                app.table.add_widget(tname)
                app.table.add_widget(tval)
                count = count +1 
                
            superRoot.root.current = "tableScreen"
            self.manager.transition.direction = "left"
        
class TokenTable(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.assign)
    
    def assign(self,dt):
        app = App.get_running_app()
        app.table = self.ids.tableLayout
        app.goCButton = self.ids.goToC
    
    


class P(BoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        #print("ASSIGNED")
        app = App.get_running_app()
        app.cError = self.ids.errorLabel
        #print(app.cError.text)
class Code(Screen):
    
    def __init__(self, **kw):
        super(Code,self).__init__(**kw)

        #app = App.get_running_app()
        #self.ids.cCodeLabel.text = "hello"
        Clock.schedule_once(self.assign)
    
    def assign(self,dt):
        app = App.get_running_app()
        app.cTextInput = self.ids.cTextInput
    def copy(self):
        app = App.get_running_app()
        pyperclip.copy(app.c_code)
class WindowManager(ScreenManager):
    pass
kv = Builder.load_file('compilerlayout.kv')


class MyApp(App): # <- Main Class
    code:str = ''

    def build(self):
        self.title = 'Tiny Compiler'
        return kv

if __name__ == "__main__":
    MyApp().run()