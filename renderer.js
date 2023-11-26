const folderSelectButtons = document.querySelectorAll(".folder-select-row button");
const submitButton = document.querySelector("#submit-button");
const spliceFolderPathText = document.querySelector("#splice-folder-path-text");
const outputFolderPathText = document.querySelector("#output-folder-path-text");


let spliceDirectory;
let outputDirectory;


for (const button of folderSelectButtons)
{
    button.addEventListener("click", async event =>
    {
        const target = event.target;
        const isSpliceButton = target.id === "splice-folder-chooser-button";

        const resp = await window.electronAPI.selectFolder();
        const canceled = resp.canceled;
        const folderPath = resp.folderPath;

        if (canceled) return;

        if (isSpliceButton)
        {
            spliceDirectory = folderPath;
            spliceFolderPathText.textContent = folderPath;
        }
        else
        {
            outputDirectory = folderPath;
            outputFolderPathText.textContent = folderPath;
        }
    });
}


submitButton.addEventListener("click", () =>
{
    if (!spliceDirectory || !outputDirectory)
    {
        // TODO: error
        return;
    }
});