const { app, BrowserWindow, ipcMain, dialog } = require("electron");
const path = require("path");


const DEFAULT_WINDOW_SIZE = [600, 300];
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


app.whenReady().then(() =>
{
    ipcMain.handle("selectFolder", async () =>
    {
        console.log("select");

        const { canceled, filePaths } = await dialog.showOpenDialog({ properties: ["openDirectory"] });

        console.log({ canceled: canceled, folderPath: filePaths[0] })
        return { canceled: canceled, folderPath: filePaths[0] };
    });

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