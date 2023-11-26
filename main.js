const { app, BrowserWindow, ipcMain, dialog } = require("electron");
const path = require("path");
const { homedir } = require("os");
const { existsSync, lstatSync } = require("fs");
const { readdir } = require("fs/promises");


const DEFAULT_WINDOW_SIZE = [600, 400];
const BANNED_EXTENSIONS = [".asd"];
let win;


function createWindow()
{
    win = new BrowserWindow({
        width: DEFAULT_WINDOW_SIZE[0],
        height: DEFAULT_WINDOW_SIZE[1],
        webPreferences: {
            preload: path.join(__dirname, "preload.js")
        }
    });

    // win.webContents.toggleDevTools();
    win.loadFile("index.html");
}


async function selectFolder()
{
    const { canceled, filePaths } = await dialog.showOpenDialog({ properties: ["openDirectory"] });
    console.log({ canceled: canceled, folderPath: filePaths[0] });
    return { canceled: canceled, folderPath: filePaths[0] };
}


async function autoFindSpliceFolder()
{
    const attemptedPath = path.join(homedir(), "Splice");

    if (!existsSync(attemptedPath)) return false;

    return attemptedPath;
}


async function copyFiles(event, directories)
{
    const spliceDir = directories.spliceDirectory;
    const outputDir = directories.outputDirectory;

    const allFilesAndDirectories = await readdir(spliceDir, { recursive: true });
    // const allFiles = allFilesAndDirectories.filter(child => lstatSync(path.join(spliceDir, child)).isFile());
    // const validFiles = allFiles.filter(file => )
    const validFilePaths = [];
    for (const childPath of allFilesAndDirectories)
    {
        const absolutePath = path.join(spliceDir, childPath);
        if (!lstatSync(absolutePath).isFile()) continue;

        const fileName = path.basename(childPath);
        const match = fileName.match(/.+(\..+)/);
        if (!match) continue;

        const fileExtension = match[0];
        if (BANNED_EXTENSIONS.includes(fileExtension)) continue;

        validFilePaths.push(childPath)
    }

    const numValidFiles = validFilePaths.length;
    for (let i = 0; i < numValidFiles; ++i)
    {
        const filePath = numValidFiles[i];
        console.log(filePath);

        // TODO: copy

        const percent = Math.ceil(i / numValidFiles * 100);
        console.log(percent)

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