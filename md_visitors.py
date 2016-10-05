from abc import ABCMeta, abstractmethod 



class VisitorParent(object):

    """
    Parent visitor class.

    All visitors must implement these abstract methods
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def visit_md_file(self, help_panel):
        pass

    @abstractmethod
    def visit_tag_config(self, help_panel):
        pass


class HeaderVisitor(VisitorParent):

    def __init__(self):
        self.__config = ConfigManager.ConfigManager.getInstance()
        self.__tag_name = 'header{}'
        self.__re_pattern = re.compile("^[#].*")

    def visit_md_file(self, help_panel):
        """
        Get matches from help_panel. Execute header specific
        insertion.
        """

        matches = help_panel.match_file(self.__re_pattern, self.__tag_name)
        self.__insert_matches(help_panel, matches)

    def __insert_matches(self, help_panel, matches):
        """
        Specific insertion operation.
        """

        for row_number, match in matches.iteritems():

            line = match.group()
            header_size = line.count('#') 

            text = line.split('#')[-1]
            text = text[1:]
 
            help_panel.insert('{}.0'.format(row_number), text, self.__tag_name.format(header_size))


    def visit_tag_config(self, help_panel):
        """
        Create various header sizes and their
        associated tags.
        """

        max_header_num = 5
        for header_num in range(max_header_num):
            # Start index at 1
            header_num += 1

            header_max_size = int(self.__config.get('helppanel', 'max_header_size'))
            header_min_size = int(self.__config.get('helppanel', 'min_header_size'))
            header_size_diff = header_max_size - header_min_size 
            header_num_diff = max_header_num - 1

            # Scale size between max and min possible header sizes 
            font_size = - ( (header_size_diff // header_num_diff) * (header_num - 1) ) + header_max_size 

            font = tkFont.Font(family="Helvetica", size=font_size, weight="bold")
            help_panel.create_tag(self.__tag_name.format(header_num), font=font)

class TextVisitor(VisitorParent):
    """
    Visitor for plain text.
    """
    def __init__(self):
        self.__config = ConfigManager.ConfigManager.getInstance()
        self.__tag_name = "standard_text"
        self.__re_pattern = re.compile("^([^#\s].*)") # Insert token if handler is written for it. 

    def visit_md_file(self, help_panel):
        """
        Get matches then use help_panel's general insertion method.
        """
        matches = help_panel.match_file(self.__re_pattern, self.__tag_name)
        help_panel.insert_matches(matches, self.__tag_name)

    def visit_tag_config(self, help_panel):
        """
        Configure tag
        """
        font_size = int(self.__config.get('helppanel', 'default_font_size'))
        font = tkFont.Font(family="Helvetica", size=font_size)
        help_panel.create_tag(self.__tag_name, font=font)




