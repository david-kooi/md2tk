
import os
import md_visitors
from utils import dynamic_import


def test_dynamic_import():
    """
    Open file containing visitor specification. 
    Import specified visitors. 

    @param: visitor_spec_filepath: Visitor specification 
    filepath.
    """

    visitor_spec_filename = "visitor_spec.txt" 
    visitor_spec_filepath = os.path.join(os.getcwd(), 
                            visitor_spec_filename)

    obj_file = open(visitor_spec_filepath)
    for line in obj_file:
        try:

            # Strip new line
            line = line.split('\n')[0]
            obj_path = "md2tk.md_visitors.{}".format(line)
           
            visitor_obj = dynamic_import(obj_path)
            print 'Imported: {}'.format(visitor_obj)

            # This is another way to do it
            #module = __import__('md_visitors',globals(), locals(), ['{}'.format(line)])
            #visitor_obj = getattr(module, '{}'.format(line))
        except ImportError, e:
            print e
            print "Unable to import %s" % line
            assert False

    assert True

