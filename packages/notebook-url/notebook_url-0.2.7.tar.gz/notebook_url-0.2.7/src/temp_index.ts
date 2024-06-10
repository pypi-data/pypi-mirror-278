import * as LZString from 'lz-string';
import { NotebookPanel } from '@jupyterlab/notebook';
import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ToolbarButton } from '@jupyterlab/apputils';
import { Clipboard } from '@jupyterlab/apputils';

console.log('notebook_to_url_ext is loaded!', NotebookPanel);

// Compress the notebook text and set as URL parameter
function compressNotebookContent(notebookPanel: NotebookPanel): void {
    const notebookContent = JSON.stringify(notebookPanel.context.model.toJSON());
    const compressedContent = LZString.compressToEncodedURIComponent(notebookContent);
    const newUrl = `${window.location.origin}${window.location.pathname}#notebook=${compressedContent}`;
    Clipboard.copyToSystem(newUrl);
    alert('URL copied to clipboard');
}

// Decompress the URL parameter and load notebook content
function decompressNotebookContent(): any | null {
    const urlParams = new URLSearchParams(window.location.hash.slice(1));
    const compressedContent = urlParams.get('notebook');
    if (compressedContent) {
        const decompressedContent = LZString.decompressFromEncodedURIComponent(compressedContent);
        return JSON.parse(decompressedContent);
    }
    return null;
}

// Add "Save to URL" button to the notebook toolbar
function addSaveToUrlButton(app: JupyterFrontEnd): void {
    console.log( app)
    //@ts-ignore
    app?.shell?.layoutModified.connect(() => {
        const current = app.shell.currentWidget;
        if (current && current instanceof NotebookPanel) {
            const saveToUrlButton = new ToolbarButton({
                label: 'Save to URL',
                onClick: () => {
                    compressNotebookContent(current);
                },
                tooltip: 'Save notebook content to URL and copy to clipboard'
            });
            current.toolbar.insertItem(10, 'saveToUrl', saveToUrlButton);
        }
    });
}

const extension: JupyterFrontEndPlugin<void> = {
    id: 'notebook_to_url_ext',
    autoStart: true,
    activate: (app: JupyterFrontEnd) => {
        console.log('Activating notebook_to_url_ext', app);
        addSaveToUrlButton(app);

        app.restored.then(() => {
            const initialContent = decompressNotebookContent();
            const current = app.shell.currentWidget;
            if (initialContent && current && current instanceof NotebookPanel) {
                current.context.model.fromJSON(initialContent);
            }
        });
    }
};

export default extension;
