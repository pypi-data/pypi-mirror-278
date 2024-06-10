import * as LZString from 'lz-string';
import { NotebookPanel, INotebookTracker } from '@jupyterlab/notebook';
import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ToolbarButton, ICommandPalette } from '@jupyterlab/apputils';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IDisposable, DisposableDelegate } from '@lumino/disposable';
import { Clipboard } from '@jupyterlab/apputils';

console.log('notebook_to_url_ext is loaded!');

// Compress the notebook text and set as URL parameter
// Compress the notebook text and set as URL parameter
function compressNotebookContent(notebookPanel: NotebookPanel): void {
    const notebookContent = JSON.stringify(notebookPanel.context.model.toJSON());
    const compressedContent = LZString.compressToEncodedURIComponent(notebookContent);
    const newUrl = `${window.location.origin}${window.location.pathname}#notebook=${compressedContent}`;

    Clipboard.copyToSystem(newUrl)
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
class SaveToUrlButtonExtension implements DocumentRegistry.IWidgetExtension<NotebookPanel, any> {
    createNew(panel: NotebookPanel): IDisposable {
        const button = new ToolbarButton({
            className: 'saveToUrl',
            label: 'Save to URL',
            onClick: () => compressNotebookContent(panel),
            tooltip: 'Save notebook content to URL and copy to clipboard'
        });

        panel.toolbar.insertAfter('cellType', 'saveToUrl', button);
        return new DisposableDelegate(() => {
            button.dispose();
        });
    }
}

const extension: JupyterFrontEndPlugin<void> = {
    id: 'notebook_to_url_ext',
    autoStart: true,
    requires: [INotebookTracker],
    optional: [ICommandPalette, IMainMenu, ISettingRegistry],
    activate: (app: JupyterFrontEnd, tracker: INotebookTracker, palette: ICommandPalette | null, menu: IMainMenu | null, settingRegistry: ISettingRegistry | null) => {
        console.log('Activating notebook_to_url_ext', app, tracker);

        const { docRegistry } = app;

        // Add the toolbar button
        const buttonExtension = new SaveToUrlButtonExtension();
        docRegistry.addWidgetExtension('Notebook', buttonExtension);

        // Handle restoring notebook content from URL
        app.restored.then(() => {
            const initialContent = decompressNotebookContent();
            if (initialContent && tracker.currentWidget) {
                tracker.currentWidget.context.model.fromJSON(initialContent);
            }

            tracker.widgetAdded.connect((sender, panel) => {
                const content = decompressNotebookContent();
                if (content) {
                    panel.context.model.fromJSON(content);
                }
            });
        });

        // Optional: Add commands to palette and menu
        if (palette) {
            const category = 'Notebook Operations';
            palette.addItem({ command: 'save-to-url', category });
        }

        if (menu) {
            menu.viewMenu.addGroup([{ command: 'save-to-url' }], 1000);
        }
    }
};

export default extension;
