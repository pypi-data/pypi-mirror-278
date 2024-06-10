"use strict";
(self["webpackChunknotebook_url"] = self["webpackChunknotebook_url"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var lz_string__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! lz-string */ "webpack/sharing/consume/default/lz-string/lz-string");
/* harmony import */ var lz_string__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(lz_string__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_5__);







console.log('notebook_to_url_ext is loaded!');
// Compress the notebook text and set as URL parameter
// Compress the notebook text and set as URL parameter
function compressNotebookContent(notebookPanel) {
    const notebookContent = JSON.stringify(notebookPanel.context.model.toJSON());
    const compressedContent = lz_string__WEBPACK_IMPORTED_MODULE_0__.compressToEncodedURIComponent(notebookContent);
    const newUrl = `${window.location.origin}${window.location.pathname}#notebook=${compressedContent}`;
    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Clipboard.copyToSystem(newUrl);
    alert('URL copied to clipboard');
}
// Decompress the URL parameter and load notebook content
function decompressNotebookContent() {
    const urlParams = new URLSearchParams(window.location.hash.slice(1));
    const compressedContent = urlParams.get('notebook');
    if (compressedContent) {
        const decompressedContent = lz_string__WEBPACK_IMPORTED_MODULE_0__.decompressFromEncodedURIComponent(compressedContent);
        return JSON.parse(decompressedContent);
    }
    return null;
}
// Add "Save to URL" button to the notebook toolbar
class SaveToUrlButtonExtension {
    createNew(panel) {
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ToolbarButton({
            className: 'saveToUrl',
            label: 'Save to URL',
            onClick: () => compressNotebookContent(panel),
            tooltip: 'Save notebook content to URL and copy to clipboard'
        });
        panel.toolbar.insertAfter('cellType', 'saveToUrl', button);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_5__.DisposableDelegate(() => {
            button.dispose();
        });
    }
}
const extension = {
    id: 'notebook_to_url_ext',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette, _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry],
    activate: (app, tracker, palette, menu, settingRegistry) => {
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
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.8817359c436149a535f0.js.map