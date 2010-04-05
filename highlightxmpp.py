# HighlightXMPP for IRC. Requires WeeChat >= 0.3.0.
# 
# Copyright (c) 2009 Jacob Peddicord <jpeddicord@ubuntu.com>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#######
#
# You must configure this plugin before using:
#   JID messages are sent from:
#     /set plugins.var.python.highlightxmpp.jid someid@jabber.org
#   Password for the above JID:
#     /set plugins.var.python.highlightxmpp.password abcdef
#   JID messages are sent *to* (if not set, defaults to the same jid):
#     /set plugins.var.python.highlightxmpp.jid myid@jabber.org

import weechat as w
import xmpp

info = (
    'highlightxmpp',
    'Jacob Peddicord <jpeddicord@ubuntu.com>',
    '0.1',
    'GPL3',
    "Relay highlighted & private IRC messages over XMPP (Jabber)",
    '',
    ''
)

settings = {
    'jid': '',
    'password': '',
    'to': '',
}

client = None

def connect_xmpp():
    global client
    # connected if not connected
    # & if we were disconnected, try to connect again
    if client and client.isConnected():
        return True
    w.prnt('', "XMPP: Connecting")
    jid_name = w.config_get_plugin('jid')
    password = w.config_get_plugin('password')
    try:
        jid = xmpp.protocol.JID(jid_name)
        client = xmpp.Client(jid.getDomain(), debug=[])
        client.connect()
        client.auth(jid.getNode(), password)
    except:
        w.prnt('', "Could not connect or authenticate to XMPP server.")
        client = None
        return False
    return True

def send_xmpp(data, signal, msg):
    global client
    # connect to xmpp if we need to
    if not connect_xmpp():
        return w.WEECHAT_RC_OK
    jid_to = w.config_get_plugin('to')
    # send to self if no target set
    if not jid_to:
        jid_to = w.config_get_plugin('jid')
    # send the message
    msg = xmpp.protocol.Message(jid_to, msg)
    client.send(msg)
    return w.WEECHAT_RC_OK

# register with weechat
if w.register(*info):
    # add our settings
    for setting in settings:
        if not w.config_is_set_plugin(setting):
            w.config_set_plugin(setting, settings[setting])
    # and finally our hooks
    w.hook_signal('weechat_highlight', 'send_xmpp', '')
    w.hook_signal('weechat_pv', 'send_xmpp', '')
