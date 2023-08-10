import sheet from '@/assets/cheat-sheet.json';

const Search = async (req, res) => {
  try {
    switch (req.method) {
      case "POST": {
        const term = req.body.term;
        let searchTerm = term
        let filteredArray = [];
        searchTerm.forEach((searchTerm, index) => {
          let commands = sheet;
          const filteredCommands = commands.filter(command =>
            command.tags.some(tag => tag.includes(searchTerm.toLowerCase()))
          );
          filteredArray.push(filteredCommands);
        });

        let intersection = filteredArray.reduce((accumulator, currentArray) =>
          accumulator.filter(value => currentArray.includes(value))
        );

        return res.status(200).json({
          message: "Search successful",
          results: intersection,
        });
      }
      default:
        return res.status(405).json({
          message: "Method Not Allowed",
        });
    }
  } catch (error) {
    return res.status(500).json({
      message: "Server Error",
      error,
    });
  }
};

export default Search;
