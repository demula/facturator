#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import os
import facturator

try:
    import wx
except ImportError, inst:
    print >>sys.stderr, 'wxPython is not available'
    sys.exit(1)

REQUIRED_WX_VERSION = (3, 0)
CURRENT_WX_VERSION = wx.VERSION[:2]
if CURRENT_WX_VERSION != REQUIRED_WX_VERSION:
    print >> sys.stderr, ('wxPython version incorrect; is %d.%d, must be %d.%d' % (CURRENT_WX_VERSION + REQUIRED_WX_VERSION))
    sys.exit(2)


# Generado por wxglade
class RootFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: RootFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.label_1 = wx.StaticText(self, -1, "Nombre pdf global:")
        self.pdf_general = wx.TextCtrl(self, -1, "facturas.pdf", style=wx.TE_RIGHT)
        self.label_2 = wx.StaticText(self, -1, "Plantilla de email:")
        self.plantilla_email = wx.TextCtrl(self, -1, "mail_factura.html", style=wx.TE_RIGHT)
        self.label_3 = wx.StaticText(self, -1, "Email remite:")
        self.email_sender = wx.TextCtrl(self, -1, "facturacion@tarjetalia.es", style=wx.TE_RIGHT)
        self.label_4 = wx.StaticText(self, -1, "Asunto email:")
        self.email_subject = wx.TextCtrl(self, -1, "Facturacion del mes", style=wx.TE_RIGHT)
        self.label_5 = wx.StaticText(self, -1, "Servidor SMTP:")
        self.smtp_server = wx.TextCtrl(self, -1, "mail.tarjetalia.es", style=wx.TE_RIGHT)
        self.label_6 = wx.StaticText(self, -1, "Usuario:")
        self.smtp_user = wx.TextCtrl(self, -1, "facturacion@tarjetalia.es", style=wx.TE_RIGHT)
        self.label_7 = wx.StaticText(self, -1, u"Contraseña:")
        self.smtp_pass = wx.TextCtrl(self, -1, "neptuno123", style=wx.TE_PASSWORD | wx.TE_RIGHT)
        self.button_1 = wx.Button(self, -1, "Enviar")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnEnviar, self.button_1)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: RootFrame.__set_properties
        self.SetTitle("Facturator")
        self.SetSize((420, 356))
        self.SetFocus()
        self.label_1.SetMinSize((200, 21))
        self.pdf_general.SetMinSize((200, 35))
        self.pdf_general.SetFocus()
        self.label_2.SetMinSize((200, 21))
        self.plantilla_email.SetMinSize((200, 35))
        self.label_3.SetMinSize((200, 21))
        self.email_sender.SetMinSize((200, 35))
        self.label_4.SetMinSize((200, 21))
        self.email_subject.SetMinSize((200, 35))
        self.label_5.SetMinSize((200, 21))
        self.smtp_server.SetMinSize((200, 35))
        self.label_6.SetMinSize((200, 21))
        self.smtp_user.SetMinSize((200, 35))
        self.label_7.SetMinSize((200, 21))
        self.smtp_pass.SetMinSize((200, 35))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: RootFrame.__do_layout
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(self.label_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_3.Add(self.pdf_general, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.Add(sizer_3, 1, wx.ALIGN_RIGHT, 0)
        sizer_4.Add(self.label_2, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_4.Add(self.plantilla_email, 0, 0, 0)
        sizer_2.Add(sizer_4, 1, wx.ALIGN_RIGHT, 0)
        sizer_5.Add(self.label_3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_5.Add(self.email_sender, 0, 0, 0)
        sizer_2.Add(sizer_5, 1, wx.ALIGN_RIGHT, 0)
        sizer_6.Add(self.label_4, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_6.Add(self.email_subject, 0, 0, 0)
        sizer_2.Add(sizer_6, 1, wx.ALIGN_RIGHT, 0)
        sizer_7.Add(self.label_5, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_7.Add(self.smtp_server, 0, 0, 0)
        sizer_2.Add(sizer_7, 1, wx.ALIGN_RIGHT, 0)
        sizer_8.Add(self.label_6, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_8.Add(self.smtp_user, 0, 0, 0)
        sizer_2.Add(sizer_8, 1, wx.ALIGN_RIGHT, 0)
        sizer_9.Add(self.label_7, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_9.Add(self.smtp_pass, 0, 0, 0)
        sizer_2.Add(sizer_9, 1, wx.ALIGN_RIGHT, 0)
        sizer_10.Add(self.button_1, 0, 0, 0)
        sizer_2.Add(sizer_10, 0, wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizer_2)
        self.Layout()
        self.Centre()
        # end wxGlade

    def OnEnviar(self, event):  # wxGlade: RootFrame.<event_handler>
        pdf_general = str(self.pdf_general.GetValue())
        plantilla_email = str(self.plantilla_email.GetValue())
        email_sender = str(self.email_sender.GetValue())
        email_subject = str(self.email_subject.GetValue())
        smtp_server = str(self.smtp_server.GetValue())
        smtp_user = str(self.smtp_user.GetValue())
        smtp_pass = str(self.smtp_pass.GetValue())
        try:
            facturator.enviar_emails(
                    pdf_general,
                    plantilla_email,
                    email_sender,
                    email_subject,
                    smtp_server,
                    smtp_user,
                    smtp_pass)
            wx.MessageBox('Todos los emails enviados correctamente.', 'Terminado', style=wx.OK | wx.ICON_INFORMATION)
        except:
            wx.MessageBox('Hubo un problema al procesar el pdf. '
                    'Para mas informacion ejecutalo el programa desde la consola.', 'Fallo en el proceso', style=wx.OK | wx.ICON_ERROR)
            print "problemo!"
        event.Skip()

# end of class RootFrame


class App(wx.App):
    def OnInit(self):
        self._project_frame = RootFrame(None)
        self._project_frame.Show()
        self.SetTopWindow(self._project_frame)
        return True
# end of class App

if __name__ == '__main__':
    app = App()
    app.MainLoop()
