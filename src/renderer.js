const folderSelectButtons = document.querySelectorAll(".folder-select-row button");
const spliceFolderChooserButton = document.querySelector("#splice-folder-chooser-button");
const submitButton = document.querySelector("#submit-button");
const spliceFolderPathText = document.querySelector("#splice-folder-path-text");
const outputFolderPathText = document.querySelector("#output-folder-path-text");
const autoFindSpliceFolderText = document.querySelector("#auto-found-text");
const spliceSection = document.querySelector("section#splice-section");
const progressBarLabel = document.querySelector("label[for='progress-bar']");
const progressBar = document.querySelector("#progress-bar");
const overwriteCheckbox = document.querySelector("#overwrite-checkbox");


let spliceDirectory;
// let outputDirectory;
let outputDirectory = "../output";


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


window.electronAPI.autoFindSpliceFolder().then(response =>
{
    if (!response) return;

    spliceDirectory = response;

    autoFindSpliceFolderText.style.display = "block";
    spliceFolderPathText.textContent = response;
    spliceSection.classList.add("disabled");
    spliceFolderChooserButton.disabled = true;
});


window.electronAPI.setProgress((event, value) =>
{
    progressBar.value = value;
    progressBarLabel.textContent = value + "%";
})


submitButton.addEventListener("click", () =>
{
    if (!spliceDirectory || !outputDirectory)
    {
        window.electronAPI.showErrorBox("The Splice and/or output directory was not set.");
        return;
    }

    window.electronAPI.copyFiles({ overwrite: overwriteCheckbox.checked, spliceDirectory: spliceDirectory, outputDirectory: outputDirectory });
});