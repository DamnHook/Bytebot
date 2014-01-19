#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from ircerror       import IrcErrorLevel, IrcException
from socket         import socket, AF_INET, SOCK_STREAM

class BytebotIrc:
    def __init__(self, server, port=6667, ssl=False, nick='Bytebot',
                 password='', description='', channel='',
                 debug=IrcErrorLevel.WARN):
        self.server      = server
        self.port        = port
        self.ssl         = ssl 
        self.nick        = nick
        self.description = description
        self.password    = password
        self.channel     = channel

        self.debug       = debug
        self.warm_up     = True
        self.socket      = socket(AF_INET, SOCK_STREAM)

        self.register_hook('ping', self.ping)

    def __del__(self):
        self.socket.shutdown()
        self.socket.close()

    def log(self, message, debug_level=IrcErrorLevel.WARN):
        if self.debug & debug_level == self.debug:
            print(message)



    def connect(self):
        try:
            self.socket.connect(self.server, self.port)
        catch Exception, e:
            self.log(e, IrcErrorLevel.EMERG)
            raise IrcException
        else:
            self.log('Successfully connected to ' + self.server + ':' + self.port, IrcErrorLevel.DEBUG)

    def login(self):
        self.socket.send("USER "+ self.nick +" "+ self.nick +" "+ self.nick +" :" + self.description + "\r\n")
        self.socket.send("NICK "+ self.nick +"\n")
        if self.password:
            self.socket.send("PRIVMSG NICKSERV :IDENTIFY " + self.password+ "\r\n")

        if self.channel:
            self.socket.send("JOIN "+ self.channel +"\n")
    
    def send_message(self, message, destination=self.channel):
        max_len = (500 - destination.__len__())
        if message.__len() > max_len):
            for part in message.split("", num=max_len):
                self.send_message(message=message, destination=destination)
        self.log('send_message to ' + destination + ': ' + message, IrcErrorLevel.DEBUG)
        self.socket.send("PRIVMSG " + destination + " :" + message + "\r\n")



    def run_commands(self, message):
        for cmd in self.hooks:
            cmd(message)



    def register_hook(self, name, function):
        if not self.hooks[name]:
            self.log('Registering hook ' + name, IrcErrorLevel.INFO)
            self.hooks[name] = function
        else:
            self.log('Hook ' + name + ' already registered', IrcErrorLevel.WARN)

    def unregister_hook(self, name):
        self.log('Unregistering hook ' + name, IrcErrorLevel.INFO)
        del self.hooks[name]

    def register_timed_hook(self, name, function):
        if not self.timed_hooks[name]:
            self.log('Registering timed hook ' + name, IrcErrorLevel.INFO)
            self.timed_hooks[name] = function
        else:
            self.log('Timed Hook ' + name + ' already registered', IrcErrorLevel.WARN)

    def unregister_timed_hook(self, name):
        self.log('Unregistering hook ' + name, IrcErrorLevel.INFO)
        del self.timed_hooks[name]



    def ping(self, message):
        if message.find('PING') != -1:
            self.log("PING REQUEST:\r\n", IrcErrorLevel.DEBUG)
            self.log(text, IrcErrorLevel.DEBUG)
            self.log('Reply will be: "PONG ' + text.split() [1] + '"\r\n', IrcErrorLevel.DEBUG)

            self.socket.send('PONG ' + text.split() [1] + '\r\n')
