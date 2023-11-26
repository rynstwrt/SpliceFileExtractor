const { contextBridge, ipcRenderer } = require("electron");


contextBridge.exposeInMainWorld("electronAPI", {
    // renderer -> main -> renderer
    selectFolder: () => ipcRenderer.invoke("selectFolder"),
    copyFiles: directories => ipcRenderer.invoke("copyFiles", directories),
    autoFindSpliceFolder: () => ipcRenderer.invoke("autoFindSpliceFolder"),

    // renderer -> main
    showErrorBox: message => ipcRenderer.send("showErrorBox", message),

    // main -> renderer
    setProgress: callback => ipcRenderer.on("setProgress", callback)
});