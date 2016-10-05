import os
import Pmw
import Tkinter


import md_visitors

class Md_Widget(Tkinter.Frame):
    """
    Display markdown files in a Tkinter Text Widget.
    """

    def __init__(self, parent, md_filepaths):
        """
        @param parent: Parent tkinter widget
        @param md_filepaths: List of .md files
        """
        
        # The parent widget
        self.__parent = parent

        self.__md_filepaths = md_filepaths
        
        self.__md_visitors  = [] 
        self.__text_view = None
        self.__md_file   = None

        # Create visitor objects
        self.__initalize_visitors()

        # Initalize widget for first .md file
        self.__initalize_widget(self.__md_filepaths[0])

    def __initalize_visitors(self):
        """
        Open file containing visitor specification. 
        Import specified visitors. 

        @param: visitor_spec_filepath: Visitor specification filepath.
        """
       
        visitor_spec_filename = "visitor_spec.txt" 
        visitor_spec_filepath = os.path.join(os.getcwd(), visitor_spec_filename)

        obj_file = open(visitor_spec_filepath)
        for line in obj_file:
            try:
                obj_path = "visitors.{}".format(line)
                visitor_obj = dynamic_import(obj_path)
                self.__md_visitors.append(visitor_obj()) 
            except ImportError, e:
                print e
                print "Unable to import %s" % line
    


    def __initalize_widget(self, md_filepath):
        """
        Initalize widget to display a single markdown file.

        If text view exists, destroy it so we can initalize 
        from scratch. Then, open the markdown file and allows 
        listeners to operate.
        """

        # Destroy if needed then recreate
        if self.__text_view:
            self.__text_view.pack_forget()
        self.__text_view = Pmw.ScrolledText(self.__parent)

        # Open file and count lines
        self.__md_file  = open(md_filepath)
        num_lines = sum(1 for line in self.__md_file)  
        self.__md_file.seek(0) # Remember to return to start!

        # Insert lines into TextView
        for i in range(num_lines):
            self.__text_view.insert(Tkinter.END, '\n')

        # Let visitors operate
        for v in self.__visitors:
            self.accept_tag_visitor(v)

        for v in self.__visitors:
            self.accept_md_visitor(v)
        
        # Pack it up
        self.__text_view.pack(side=Tkinter.TOP, expand=1, 
               fill=Tkinter.BOTH)
        self.__text_view.component('text').config(state=Tkinter.DISABLED)

    def match_file(self, re_pattern, tag_name):
        """
        Search lines given regex expression.
        Map matches to their line number. 
        Return a dictionary of line-match pairs.
        """
        matches = {}

        for row_number,line in enumerate(self.__md_file):
            # Widget rows start at 1 
            row_number += 1
            m = re_pattern.match(line)

            if m:
                #print m.group(), row_number #Uncomment for 
                                             #regex debugging
                matches[row_number] = m

        # Return file to start
        self.__md_file.seek(0)
        return matches

    def specific_insert(self, *args):
        """
        Specific insertion method. Allows implementation
        of private visitor methods for more 
        specific insertion operations.
        """
        self.__help_text_view.insert(*args)

    def match_insert(self, matches, tag_name):
        """
        General visitor insertion method.   

        @param matches: Dictionary of line-match pairs.
        @param tag_name: The formating tag name 
        """
        for row_number, m in matches.iteritems():
            self.__help_text_view.insert('{}.0'.format(row_number),
                                         m.group(), tag_name)


    def accept_tag_visitor(self, v):
        """
        Allow visitors to configure tags.
        """
        v.visit_tag_config(self)

    def accept_md_visitor(self, v):
        """
        Allow visitors to parse md_file.
        """
        v.visit_md_file(self)


def test_1():
    assert True

def dynamic_import(obj_path):
    """
    Return an object foo given a path:
    bar.foo
    """

    components = name.split('.')
    mod = __import__(components[0])
    
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
