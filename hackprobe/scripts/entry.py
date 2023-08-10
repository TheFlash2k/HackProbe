class Entry:

    '''
    Entry class for HackProbe dataset.

    Attributes
    ----------
    commands : dict
        Dictionary of commands and their comments.
        The commands will be the key and the value will be another dictionary
        with the comment as the key and the value will be the comment itself.

    description : str
        Description of the entry.
    tags : list
        List of tags for the entry.

    Methods
    -------

    '''

    class CommandEntry:

        '''
        CommandEntry class for HackProbe dataset.

        Attributes
        ----------
        cmd : str
            Command name.
        description : str
            Description of the command.
        examples : list
            List of examples for the command.

        Methods
        -------

        '''

        def __init__(self, cmd : str, description : str, examples : list):
            self.cmd = cmd
            self.description = description
            self.examples = examples
        
        def __dict__(self):
            return {
                'cmd': self.cmd,
                'description': self.description,
                'examples': self.examples
            }
        
        def __str__(self):
            return f"CommandEntry(cmd={self.cmd}, description={self.description}, examples={self.examples})"
    
    def __init__(self, tags : list = [], description : str = "", commands : list[CommandEntry] = []):
        self.tags = tags
        self.description = description
        self.commands = commands

    commands : dict[str, CommandEntry]
    description : str
    tags : list
    
    def __dict__(self):
        return {
            'tags': [i.strip().lower() for i in self.tags],
            'description': self.description.strip(),
            'commands': [i.__dict__() for i in self.commands]
        }
    
    def __str__(self):
        return f"Entry(tags={self.tags}, description={self.description}, commands={self.commands})"