const { app, BrowserWindow } = require("electron");
const path = require("path");


const DEFAULT_WINDOW_SIZE = [800, 600];


function createWindow()
{
    const win = new BrowserWindow({
        width: DEFAULT_WINDOW_SIZE[0],
        height: DEFAULT_WINDOW_SIZE[1],
        webPreferences: {
            preload: path.join(__dirname, "preload.js")
        }
    });

    win.loadFile("index.html");
}


app.whenReady().then(() =>
{
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