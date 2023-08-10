# HackProbe - A Search Engine for JSON-based Cheat Sheets

---

## What is HackProbe?

HackProbe is a search engine for JSON-based cheat sheets. It is a simple FastAPI based API that can be used to search for commands that you need to carry out a certain task. It is currently in development and is not ready for production use.

> Note: I will provide you with a pretty big JSON file that you can use to test the API. You can also use it to create your own cheat sheet.

---

## How to use HackProbe?

Hackprobe uses Next.js as the frontend and FastAPI as the backend. To run the project, you need to have Node.js 14+ installed on your system.

```sh
cd app/
npm install
npm run dev
```

## Screenshots

Hackprobe is a single page website that allows quick command searching based on the provided `json` file
![image](https://github.com/TheFlash2k/HackProbe/assets/19727349/c3b09274-20ae-42a5-97ec-b50393ca144e)

## Is adding your own commands possible?

Yes! You can simply fork the project, and update the `cheat-sheet.json` to your own liking. However, what I'm currently working on is creating an Administrator panel, where you can easily add the commands and those commands will be stored in the `cheat-sheet.json` file automatically without you even having to worry about anything. Currently, however; you do need to manually add the commands in the json file.

### NOTE

This is currently a work in progress. I will update this README as I make progress on the project. I'm making this project in my spare time. If you want to contribute, please feel free to do so.

### Contributors

- [Muhammad Azeem](https://github.com/mazeem77) - Helped with the frontend of HackProbe.

---
