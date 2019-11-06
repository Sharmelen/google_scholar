import wx
import hashlib
import os
import sys
import pymysql

class Mywin(wx.Frame):
    def __init__(self,parent,title):
        super(Mywin, self).__init__(parent,title = title,size = (350,400))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.SetBackgroundColour('WHITE')
        self.png = wx.StaticBitmap(panel, -1, wx.Bitmap("upnm.png", wx.BITMAP_TYPE_ANY))
        vbox.Add(self.png, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        l1 = wx.StaticText(panel,-1,"Username :")

        hbox1.Add(l1, 1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        self.t1 = wx.TextCtrl(panel)

        hbox1.Add(self.t1,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        vbox.Add(hbox1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        l2 = wx.StaticText(panel, -1, "Password :")

        hbox2.Add(l2,1,wx.ALIGN_LEFT|wx.ALL,5)
        self.t2 = wx.TextCtrl(panel,style = wx.TE_PASSWORD)

        hbox2.Add(self.t2,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        vbox.Add(hbox2)

        self.btn = wx.Button(panel, -1, "Login")
        vbox.Add(self.btn, 0, wx.ALIGN_CENTER)
        self.btn.Bind(wx.EVT_BUTTON, self.OnClicked)

        self.btn = wx.Button(panel, -1, "Exit")
        vbox.Add(self.btn, 0, wx.ALIGN_CENTER)
        self.btn.Bind(wx.EVT_BUTTON, self.OnExit)

        panel.SetSizer(vbox)

        self.Centre()
        self.Show()
        self.Fit()

    def OnClicked(self,event):
        name = self.t1.GetValue()     #name is sharmelen
        password = self.t2.GetValue() #password is sharmelen

        m = hashlib.md5()
        m.update((password.encode('utf-8')))
        newpass = m.hexdigest()
       #print(m.hexdigest())

        connection = pymysql.connect(host='localhost', user='root', port=3306, password='sharmelen', db='li_trial',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sqlQuery = "SELECT name , password FROM admin_cred WHERE name = %s AND password = %s "
                cursor.execute(sqlQuery, (name, newpass))
                auth = cursor.fetchall()
                auth_new = auth[0]
                auth_name = auth_new['name']
                auth_pass = auth_new['password']
                connection.commit()
        except:
            print()

        if name == auth_name :
            if newpass == auth_pass:
                os.system('python admin_view.py')
            else:
                wx.MessageBox("Please Try Again", "Message", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Please Try Again", "Message", wx.OK | wx.ICON_ERROR)

    def OnExit(self, event):
        wx.MessageBox("Thank You", "Message", wx.OK | wx.ICON_INFORMATION)
        sys.exit(0)
app = wx.App()
Mywin(None,'Login Page')
app.MainLoop()
