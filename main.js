const { app, BrowserWindow, ipcMain, dialog, Menu } = require("electron");
const path = require("path");
const { homedir } = require("os");
const { existsSync, lstatSync, copyFileSync } = require("fs");
const { readdir } = require("fs/promises");


const DEFAULT_WINDOW_SIZE = [600, 400];
const BANNED_FILE_EXTENSIONS = [".asd"];
let win;


function createWindow()
{
    win = new BrowserWindow({
        width: DEFAULT_WINDOW_SIZE[0],
        height: DEFAULT_WINDOW_SIZE[1],
        icon: path.join(__dirname, "./assets/icons/icon.icns"),
        webPreferences: {
            preload: path.join(__dirname, "preload.js")
        }
    });

    win.removeMenu();
    win.loadFile("index.html");
}


async function selectFolder()
{
    const { canceled, filePaths } = await dialog.showOpenDialog({ properties: ["openDirectory"] });
    return { canceled: canceled, folderPath: filePaths[0] };
}


async function autoFindSpliceFolder()
{
    const attemptedPath = path.join(homedir(), "Splice");
    return existsSync(attemptedPath) ? attemptedPath : false;
}


async function copyFiles(event, data)
{
    const overwrite = data.overwrite;
    const spliceDir = data.spliceDirectory;
    const outputDir = data.outputDirectory;

    const allFilesAndDirectories = await readdir(spliceDir, { recursive: true });

    const validFilePaths = [];
    for (const childPath of allFilesAndDirectories)
    {
        const absolutePath = path.join(spliceDir, childPath);
        if (!lstatSync(absolutePath).isFile()) continue;

        const fileName = path.basename(childPath);
        const match = fileName.match(/.+(\..+)/);
        if (!match || !match[1]) continue;

        const fileExtension = match[1];
        if (BANNED_FILE_EXTENSIONS.includes(fileExtension.toLowerCase())) continue;

        const outputFilePath = path.join(outputDir, fileName);
        if (existsSync(outputFilePath) && !overwrite) continue;

        validFilePaths.push(absolutePath)
    }

    const numValidFiles = validFilePaths.length;
    for (let i = 0; i < numValidFiles; ++i)
    {
        const filePath = validFilePaths[i];
        const outputFilePath = path.join(outputDir, path.basename(filePath));

        console.log("Copying", filePath);
        copyFileSync(filePath, outputFilePath);

        let percent = Math.ceil(i / numValidFiles * 100);
        if (i === numValidFiles - 1) percent = 100;
        win.webContents.send("setProgress", percent);
    }
}


function showErrorBox(event, message)
{
    dialog.showErrorBox("Error!", message)
}


app.whenReady().then(() =>
{
    ipcMain.handle("selectFolder", selectFolder);
    ipcMain.handle("copyFiles", copyFiles);
    ipcMain.handle("autoFindSpliceFolder", autoFindSpliceFolder);

    ipcMain.on("showErrorBox", showErrorBox);

    createWindow();

    app.on("activate", () =>
    {
        if (BrowserWindow.getAllWindows().length === 0)
            createWindow();
    });
});


app.on("window-all-closed", () =>
{
    if (process.platform !== "darwin")
        app.quit();
})