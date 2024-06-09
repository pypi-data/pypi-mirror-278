"use strict";
(self["webpackChunkjupyterlab_gridwidth"] = self["webpackChunkjupyterlab_gridwidth"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! jupyterlab-celltagsclasses */ "webpack/sharing/consume/default/jupyterlab-celltagsclasses/jupyterlab-celltagsclasses");
/* harmony import */ var jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__);
/*
 * for attaching keybindings later on, see
 * https://towardsdatascience.com/how-to-customize-jupyterlab-keyboard-shortcuts-72321f73753d
 */
/* eslint-disable prettier/prettier */






const PLUGIN_ID = 'jupyterlab-gridwidth:plugin';
const ALL_GRIDWIDTHS = [
    '1-2',
    '1-3',
    '2-3',
    '1-4',
    '2-4',
    '3-4',
    '1-5',
    '2-5',
    '3-5',
    '4-5',
    '1-6',
    '2-6',
    '3-6',
    '4-6',
    '5-6',
];
const plugin = {
    id: PLUGIN_ID,
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.INotebookTracker, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry],
    activate: (app, palette, notebookTracker, settingRegistry) => {
        console.log('extension jupyterlab-gridwidth is activating');
        const adjust_windowing_mode = () => {
            // force notebook windowing-mode to 'defer'
            // will be done - or not, depending on turn_off_windowing_mode
            // once our settings are loaded
            settingRegistry.load('@jupyterlab/notebook-extension:tracker').then((nbSettings) => {
                const former = nbSettings.get('windowingMode').composite;
                if (former === 'full') {
                    nbSettings.set('windowingMode', 'defer'),
                        console.warn('jupyterlab-gridwidth: windowing mode FORCED back to "defer"');
                }
                else {
                    console.log(`jupyterlab-gridwidth: windowing mode already ${former} - unchanged`);
                }
            }, (err) => console.error(`jupyterlab-gridwidth: Could not set windowing mode: ${err}`));
        };
        let command;
        // gridwidth-1-2..gridwidth-1-6
        const ALL_GRIDWIDTHS_FULL = ALL_GRIDWIDTHS.map(gridwidth => `gridwidth-${gridwidth}`);
        for (const gridwidth of ALL_GRIDWIDTHS) {
            const [num, den] = gridwidth.split('-');
            command = `gridwidth:toggle-${num}-${den}`;
            app.commands.addCommand(command, {
                label: `Toogle Cell to ${num}/${den} of Full Width`,
                execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.Scope.Multiple, (cell) => {
                    (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.md_toggle_multi)(cell, 'tags', `gridwidth-${gridwidth}`, ALL_GRIDWIDTHS_FULL);
                })
            });
            palette.addItem({ command, category: 'gridwidth' });
            app.commands.addKeyBinding({
                command,
                keys: [`Alt ${num}`, `Alt ${den}`],
                selector: '.jp-Notebook'
            });
        }
        // a shortcut to cancel all gridwidths
        command = 'gridwidth:cancel';
        app.commands.addCommand(command, {
            label: 'Restore Full Cell Width',
            execute: () => (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells)(notebookTracker, jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.Scope.Multiple, (cell) => {
                (0,jupyterlab_celltagsclasses__WEBPACK_IMPORTED_MODULE_4__.md_toggle_multi)(cell, 'tags', '', ALL_GRIDWIDTHS_FULL);
            })
        });
        palette.addItem({ command, category: 'gridwidth' });
        app.commands.addKeyBinding({
            command,
            keys: ['Alt 0'],
            selector: '.jp-Notebook'
        });
        notebookTracker.widgetAdded.connect((tracker, panel) => {
            let button;
            function loadSetting(setting) {
                // Read the settings and convert to the correct type
                const show_toolbar_button = setting.get('show_toolbar_button')
                    .composite;
                // actually this is typed as MenuBar
                const menubar = panel.toolbar;
                if (show_toolbar_button) {
                    if (button) {
                        console.debug('gridwidth: button already on');
                        return;
                    }
                    console.debug('gridwidth: adding button', panel.content.node);
                    button = new CellWidthMenu(app, tracker).button;
                    menubar.insertItem(10, 'gridWidth', button);
                }
                else {
                    if (button === undefined) {
                        console.debug('gridwidth: button already off');
                        return;
                    }
                    console.debug('gridwidth: disposing button', panel.content.node);
                    button.dispose();
                    button = undefined;
                }
                const windowing_mode_defer = setting.get('windowing_mode_defer')
                    .composite;
                if (windowing_mode_defer) {
                    adjust_windowing_mode();
                }
            }
            Promise.all([app.restored, settingRegistry.load(PLUGIN_ID)]).then(([_, setting]) => {
                loadSetting(setting);
                setting.changed.connect(loadSetting);
            });
        });
    }
};
// a lumino menu & a toolbar button to invoke the menu
class CellWidthMenu {
    constructor(app, notebookTracker) {
        this.menuOpen = false;
        this.preventOpen = false;
        this.button = this.createButton(app, notebookTracker);
    }
    createButton(app, notebookTracker) {
        // create a lumino menu
        const menu = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Menu({ commands: app.commands });
        menu.title.label = 'Cell Width';
        ALL_GRIDWIDTHS.forEach(gridwidth => {
            const command = `gridwidth:toggle-${gridwidth}`;
            menu.addItem({ command });
        });
        menu.addItem({ type: 'separator' });
        menu.addItem({ command: 'gridwidth:cancel' });
        /** About to Close Event: When the aboutToClose event of the menu is emitted
         * (which happens just before the menu is actually closed),
         * the this.menuOpen property is set to false to indicate the menu is not open.
         * Simultaneously, this.preventOpen is set to true to prevent the menu from immediately reopening due to subsequent events.
         * A setTimeout call is used to reset this.preventOpen to false in the next event loop cycle. */
        menu.aboutToClose.connect(() => {
            this.menuOpen = false;
            this.preventOpen = true;
            // console.log('menu about to close event');
            setTimeout(() => {
                this.preventOpen = false;
                // console.log('menu successfully closed and can be opened again.');
            }, 0);
            // console.log('menu is waiting to be closed... prevent it to open...');
        });
        // create a toolbar button to envok the menu
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
            // the icon is similar to the previous split-cell extension button icon
            iconClass: 'fa fa-arrows-h',
            /** Button Click Event: When the toolbar button is clicked, the click event handler checks the state of this.menuOpen.
             * The this.menuOpen is then set to true, indicating the menu is now open.
             * If it's true, the menu is currently open and should be closed.
             * If this.menuOpen is false and this.preventOpen is also false, the menu is not open and should be opened.
             * The rect object represents the button's position, and menu.open positions the menu at the bottom-left of the button.*/
            onClick: () => {
                // console.log('button clicked');
                if (this.menuOpen) {
                    // Actually not envoked most of the time, no need to manually close the menu here,
                    // because the menu will be closed automatically when this onClick event emits.
                    menu.close();
                    // console.log('menu closed');
                }
                else if (!this.preventOpen) {
                    const rect = button.node.getBoundingClientRect();
                    menu.open(rect.left, rect.bottom);
                    this.menuOpen = true;
                    // console.log('menu opened');
                }
            },
            tooltip: 'Toogle Cell Width'
        });
        return button;
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.990b35638d0e302a5a09.js.map