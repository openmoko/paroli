#    Paroli
#
#    copyright 2008 OpenMoko
#
#    This file is part of Paroli.
#
#    Paroli is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Paroli is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Paroli.  If not, see <http://www.gnu.org/licenses/>.


import logging
logger = logging.getLogger('app.i-o')

import os
import tichy
from tichy import gui
import sys
from tichy.service import Service
import ecore

class I_O_App(tichy.Application):
    name = 'Paroli-I/O'
    icon = 'icon.png'
    category = 'main' # So that we see the app in the launcher
    
    def run(self, parent=None, text = ""):
        if isinstance(text, str):
            text = tichy.Text(text)
        #print dir(parent.etk_obj)
        #parent.etk_obj.title_set('parent')
        #parent.etk_obj.hide_all()
        self.main = parent
        self.main.etk_obj.title_set('Paroli I/O')
        self.history_items = []
        self.edje_file = os.path.join(os.path.dirname(__file__),'paroli-i-o.edj')
        #dir(main.etk_obj)
        #print dir(main)
        #self.window = gui.Window(parent, modal=True)
        #self.window.etk_obj.theme_file_set('../tichy/gui_p/edje/paroli-in-tichy.edj')
        #print self.window.etk_obj.theme_file_get()
        #self.window.etk_obj.theme_group_set('tele')
        #print self.window.etk_obj.theme_group_get()
        #self.window.etk_obj.title_set('paroli dialer')
        #self.window.etk_obj.show_all()
        #print dir(self.window.etk_obj)
        #self.window.show()
        #self.window.etk_obj.propagate_color_set(0)
        #print self.window.etk_obj.children_get()
        self.gsm_service = tichy.Service('GSM')
        #print dir(gsm_service.logs)
        #print "printing of dir done"
        #print str(gsm_service.logs)
        #for i in gsm_service.logs:
            #print dir(i)
            
        print "logs done"
        #self.history = [('Ali', '099872394'),('bachus', '098953214'),('julius', '059321894'),('zacharias', '04326953214'),('zuberio', '09922153214'),('oliver', '03322153214'),('Paula', '0225623614')]
        self.history = self.gsm_service.logs
        
        self.history_scroller = ['one','two','three','four','five','six','seven','i']
        #,'i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i','i'
        self.edje_obj = gui.edje_gui(self.main,'i-o',self.edje_file)
        self.edje_obj.edj.layer_set(2)
        self.edje_obj.edj.show()
        
        self.edje_obj.edj.signal_callback_add("edit_btn_clicked", "*", self.edit_mode)
        self.edje_obj.edj.signal_callback_add("top-bar", "*", self.top_bar)
        
        history_box = gui.edje_box(self,'V',1)
        self.lists = gui.lists()
        try:
          #self.lists.generate_list(self,self.main.etk_obj.evas,self.history_scroller,history_edje,self.edje_obj,'history_item')
          self.history_objects_list = gui.contact_list(self.history,history_box,self.main.etk_obj.evas,self.edje_file,'history_item',self,kind='history')
        except Exception,e:
          print e
        to_2_swallowed = history_box.scrolled_view

        try:
          self.edje_obj.add(to_2_swallowed,history_box,"history-items")
        except Exception,e:
          print e
        history_box.box.show()

     
        yield tichy.Wait(self.main, 'back')
        print dir(self.main.children)
        for i in self.main.children:
          i.remove()
        self.main.etk_obj.hide()   # Don't forget to close the window
        
    
    def edit_mode(self, emission, source, param):
        #for i in self.history_objects_list.item_list:
            #print i[0]
        if emission.part_state_get(param)[0] == 'default' or emission.part_state_get(param)[0] == '':
            signal = 'edit'
            #emission.signal_emit('wait-mode',"*")
            
            emission.signal_emit('edit-mode',"*")
            
        else:
            #print "button pressed"
            emission.signal_emit('edit_button_to_wait',"")
            #print emission.part_state_get(edje_object)[0]
            signal = 'normal'
            #ecore.MainLoop.iterate()
            for i in self.history_objects_list.item_list:
                    
              #if edje object state edit
              if i[1].part_state_get('edit-base')[0] == 'edit':
                    #destroy text in info field (missed etc)
                    self.remove_entry(i[3])
                    #i[1].signal_emit("remove_called","")
                    #i[1].destroy()
                    
                    #remove all edje stuff from history item to be deleted
                    i[2].remove_all()
                    
              #TODO: add "real delete" on SIM  
                    
            emission.signal_emit('edit_button_to_default',"")

        for i in self.history_objects_list.item_list:
            i[1].signal_emit(signal,"")
        
        print "edit-mode emitted"
    
    def top_bar(self,emission, source, param):
        print "top bar pressed"
        print dir(self.main)
        self.main.emit('back')
        #emission.delete()
    
    def call_contact(self, emission, source, param, contact):
        print "call contact called"
        number = contact.number.value
        name = unicode(contact)
        #self.extra_child.edj.part_swallow_get('contacts-items').visible_set(0)
        #self.extra_child.edj.part_swallow_get('contacts-items').delete()
        caller_service = Service('Caller')
        my_call = caller_service.call(emission, number, name)
        my_call.start()
        #try:
            #self.extra_child.edj.delete()
        #except Exception,e:
            #print e
    
    def remove_entry(self,entry):
        print "remove called"
        assert entry in self.history
        self.history.remove(entry)
    
    def load_phone_book(self,orig,orig_parent,emission, source, param):
        print "load phone book called"
        print dir(orig)
        print orig.group
        try:
          new_edje = gui.edje_window(orig_parent,'tele-people',orig.gsm,orig.phone_book)
        except Exception,e:
          print e
        orig.extra_child = new_edje
        #try:
          #orig_parent.add(new_edje)
        #except Exception,e:
          #print e
        print "done"
        try:
          contacts_edje = gui.edje_box(self,'V',1)
        except Exception,e:
          print e  
         
        #try: 
          #self.contacts_obj = gui.edje_window(orig_parent,'people',self)
        #except Exception,e:
          #print e 
        #self.contacts_obj.layer_set(17)
        try: 
          self.lists = gui.lists()
        except Exception,e:
          print e 
          
        try: 
          print "self.lists.generate_contacts_list(self,orig_parent,self.phone_book,contacts_edje,self.edje_obj)"
          self.lists.generate_contacts_list(self,orig_parent.etk_obj.evas,self.phone_book,contacts_edje,self.edje_obj,'tele-contacts_item')
        except Exception,e:
          print e 
        
        try: 
          to_2_swallowed = contacts_edje.scrolled_view
        except Exception,e:
          print e 
        
        try: 
          print "new_edje.add(to_2_swallowed,contacts_edje)"
          new_edje.add(to_2_swallowed,contacts_edje)
        except Exception,e:
          print e 
        
        try: 
          contacts_edje.box.show()
        except Exception,e:
          print e 
    
    def on_key(self, w, k):
        self.text.value += k  # The view will automatically be updated
        
    def on_del(self, w):
        self.text.value = self.text.value[:-1]
        
    def calling(self,orig,orig_parent,emission, source, param):  
        print "calling"
        number = emission.part_text_get("num_field-label")
        #print number
        #yield Caller(self.edje_obj, number)
        
    def on_call(self, b):
        yield Caller(self.window, self.text.value)
       
    def self_test(self,emission, source, param):
        print "emission: ", str(emission)
        print "source: ", str(source)
        print "param: ", str(param)
        #try:
            #eval(source + '(self,self.parent,emission, source, param)')
        #except Exception, e:
            #dir(e)

    def wait_mode(self,instance,edje_object, emission, source,param):
        emission.signal_emit('wait-mode',"*")
        #print dir(emission.part_object_get('layover'))
        print emission.part_object_get('layover').render_op_get()
        print "wait-mode emitted"
        emission.part_object_get('layover').render_op()
    
    def edit_btn_clicked(self,instance,edje_object, emission, source,param):
        #print "edit_btn in paroli-i-o"
        #print len(self.history_items)
        try:
            print "state: ",emission.part_state_get("edit-button")[0]
        except Exception,e:
            print e
        if emission.part_state_get("edit-button")[0] == 'default' or emission.part_state_get("edit-button")[0] == '':
            #print "edit detected"
            signal = 'edit'
            #emission.signal_emit('wait-mode',"*")
                  
            #print "after for"
            
            try:
              emission.signal_emit('edit-mode',"*")
            except Exception,e:
                  print e  
            
        else:
            #print "button pressed"
            #emission.signal_emit('edit_button_to_wait',"*")
            #print emission.part_state_get(edje_object)[0]
            signal = 'normal'
            #print "normal detected"
            for i in self.history_items:
                    
              #if edje object state edit
              if i[0].part_state_get('edit-base')[0] == 'edit':
                    #destroy text in info field (missed etc)
                    i[1].destroy()
                    
                    #remove all edje stuff from history item to be deleted
                    i[2].remove_all()
                    
              #TODO: add "real delete" on SIM  
                    
            emission.signal_emit('edit_button_to_default',"*")

        
        #print "after if/else"
        for i in self.history_items:
            print "# :",str(i)
            try:
              i[0].signal_emit(signal,"")
            except Exception,e:
              print e
        
        print "edit-mode emitted"

