const { contextBridge, ipcRenderer } = require("electron");


contextBridge.exposeInMainWorld("electronAPI", {
    // renderer -> main -> renderer
    selectFolder: () => ipcRenderer.invoke("selectFolder"),
    copyFiles: directories => ipcRenderer.invoke("copyFiles", directories)
});