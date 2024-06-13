"use strict";
(self["webpackChunkclimb_onyx_ui"] = self["webpackChunkclimb_onyx_ui"] || []).push([["lib_index_js"],{

/***/ "./lib/App.js":
/*!********************!*\
  !*** ./lib/App.js ***!
  \********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ReactAppWidget: () => (/* binding */ ReactAppWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var climb_onyx_ui__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! climb-onyx-ui */ "webpack/sharing/consume/default/climb-onyx-ui/climb-onyx-ui");
/* harmony import */ var climb_onyx_ui__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(climb_onyx_ui__WEBPACK_IMPORTED_MODULE_2__);


//import App from '../../react-prototype/src/App'

class ReactAppWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(route, s3) {
        super();
        this.routeHandler = route;
        this.s3PathHandler = s3;
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement((climb_onyx_ui__WEBPACK_IMPORTED_MODULE_2___default()), { httpPathHandler: this.routeHandler, s3PathHandler: this.s3PathHandler });
    }
}


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI),
/* harmony export */   requestAPIResponse: () => (/* binding */ requestAPIResponse)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}, param = ['', '']) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, 'climb-onyx-ui', endPoint);
    let url = new URL(requestUrl);
    if (param[0] != '')
        url.searchParams.append(param[0], param[1]);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(url.toString(), init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}
async function requestAPIResponse(endPoint = '', init = {}, param = ['', '']) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, 'climb-onyx-ui', endPoint);
    let url = new URL(requestUrl);
    if (param[0] != '')
        url.searchParams.append(param[0], param[1]);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(url.toString(), init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.NetworkError(error);
    }
    return response;
}


/***/ }),

/***/ "./lib/icon.js":
/*!*********************!*\
  !*** ./lib/icon.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   chatIcon: () => (/* binding */ chatIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_dna_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./../style/icons/dna.svg */ "./style/icons/dna.svg");


const chatIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'jitsi:chat',
    svgstr: _style_icons_dna_svg__WEBPACK_IMPORTED_MODULE_1__
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/htmlviewer */ "webpack/sharing/consume/default/@jupyterlab/htmlviewer");
/* harmony import */ var _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _App__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./App */ "./lib/App.js");
/* harmony import */ var _icon__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./icon */ "./lib/icon.js");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);








class OpenS3FileWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget {
    constructor() {
        const body = document.createElement('div');
        const existingLabel = document.createElement('label');
        existingLabel.textContent = 'S3 file name:';
        const input = document.createElement('input');
        input.value = '';
        input.placeholder = 's3://example-bucket/example-file.html';
        body.appendChild(existingLabel);
        body.appendChild(input);
        super({ node: body });
    }
    get inputNode() {
        return this.node.getElementsByTagName('input')[0];
    }
    getValue() {
        return this.inputNode.value;
    }
}
/**
 * Initialization data for the climb-onyx-ui extension.
 */
const plugin = {
    id: 'climb-onyx-ui:plugin',
    description: 'climb-onyx-ui.',
    autoStart: true,
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.ILauncher, _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__.IHTMLViewerTracker],
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__.IDocumentManager],
    activate: (app, palette, documentManager, launcher, htmlTracker) => {
        console.log('JupyterLab extension @climb-onyx-ui is activated!');
        const command = 'onyx_extension';
        const s3_command = 's3_onyx_extension';
        const category = 'Onyx';
        const s3_open_function = (s3_link) => {
            (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('s3', {}, ['s3location', s3_link])
                .then(data => {
                documentManager.open(data['temp_file']);
            })
                .catch(reason => {
                console.error(`The climb-onyx-ui server extension appears to be missing.\n${reason}`);
            });
        };
        const routeHandler = async (route) => {
            return (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPIResponse)('reroute', {}, ['route', route]);
        };
        // Create a single widget
        let widget;
        app.commands.addCommand(command, {
            label: 'Onyx',
            caption: 'Onyx',
            icon: _icon__WEBPACK_IMPORTED_MODULE_6__.chatIcon,
            execute: () => {
                if (!widget || widget.disposed) {
                    const content = new _App__WEBPACK_IMPORTED_MODULE_7__.ReactAppWidget(routeHandler, s3_open_function);
                    content.addClass('onyx-Widget');
                    widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content });
                    widget.title.label = 'Onyx';
                    widget.title.closable = true;
                }
                if (!tracker.has(widget)) {
                    tracker.add(widget);
                }
                if (!widget.isAttached) {
                    // Attach the widget to the main work area if it's not there
                    app.shell.add(widget, 'main');
                }
                // Activate the widget
                app.shell.activateById(widget.id);
            }
        });
        palette.addItem({ command, category: category });
        if (launcher) {
            launcher.add({
                command: command,
                category: category
            });
        }
        app.commands.addCommand(s3_command, {
            label: 'Onyx open s3 document',
            caption: 'Onyx open s3 document',
            icon: _icon__WEBPACK_IMPORTED_MODULE_6__.chatIcon,
            execute: () => {
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                    body: new OpenS3FileWidget(),
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'GO' })],
                    focusNodeSelector: 'input',
                    title: 'Open site'
                })
                    .then(result => {
                    if (result.button.label === 'Cancel') {
                        return;
                    }
                    if (!result.value) {
                        return;
                    }
                    const s3_link = result.value;
                    s3_open_function(s3_link);
                })
                    .catch(reason => {
                    console.error(`The climb-onyx-ui server extension appears to be missing.\n${reason}`);
                });
            }
        });
        palette.addItem({ command: s3_command, category: category });
        if (launcher) {
            launcher.add({
                command: s3_command,
                category: category
            });
        }
        if (htmlTracker) {
            htmlTracker.widgetAdded.connect((sender, panel) => {
                panel.trusted = true;
            });
        }
    }
};
const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.WidgetTracker({
    namespace: 'climb-onyx-ui'
});
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./style/icons/dna.svg":
/*!*****************************!*\
  !*** ./style/icons/dna.svg ***!
  \*****************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" version=\"1.1\" width=\"256\" height=\"256\" viewBox=\"0 0 256 256\" xml:space=\"preserve\">\r\n\r\n<defs>\r\n</defs>\r\n<g style=\"stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;\" transform=\"translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)\" >\r\n\t<path d=\"M 73.352 33.287 c -1.16 0 -2.35 -0.064 -3.563 -0.193 c -0.824 -0.088 -1.42 -0.827 -1.332 -1.651 c 0.088 -0.825 0.841 -1.413 1.65 -1.333 c 7.211 0.774 13.366 -0.99 17.333 -4.956 c 0.586 -0.586 1.535 -0.586 2.121 0 s 0.586 1.536 0 2.121 C 85.631 31.205 79.962 33.287 73.352 33.287 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(0,0,0); fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n\t<path d=\"M 26.214 90 c -0.384 0 -0.768 -0.146 -1.061 -0.439 c -0.586 -0.586 -0.586 -1.535 0 -2.121 c 5.682 -5.683 6.724 -15.295 2.858 -26.374 C 24.045 49.694 24.94 39.392 30.467 32.8 c 4.991 -5.954 13.106 -8.365 22.838 -6.79 c 0.818 0.132 1.374 0.903 1.241 1.721 s -0.907 1.366 -1.72 1.241 c -8.652 -1.401 -15.775 0.645 -20.061 5.755 c -4.831 5.762 -5.531 15.001 -1.92 25.35 c 4.259 12.209 2.958 22.955 -3.57 29.483 C 26.982 89.854 26.598 90 26.214 90 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(0,0,0); fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n\t<path d=\"M 42.32 64.459 c -1.732 0 -3.535 -0.144 -5.399 -0.434 c -0.818 -0.128 -1.379 -0.895 -1.251 -1.713 c 0.127 -0.819 0.897 -1.372 1.713 -1.252 c 8.575 1.34 15.636 -0.731 19.881 -5.823 c 4.804 -5.764 5.493 -14.99 1.892 -25.314 c -4.259 -12.21 -2.958 -22.956 3.57 -29.483 c 0.586 -0.586 1.535 -0.586 2.121 0 s 0.586 1.536 0 2.121 c -5.682 5.682 -6.724 15.294 -2.859 26.374 c 3.958 11.344 3.076 21.631 -2.419 28.224 C 55.577 61.946 49.567 64.459 42.32 64.459 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(0,0,0); fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n\t<path d=\"M 1.5 65.286 c -0.384 0 -0.768 -0.146 -1.061 -0.439 c -0.586 -0.586 -0.586 -1.535 0 -2.121 c 5.047 -5.047 12.812 -7.013 21.865 -5.536 c 0.817 0.134 1.372 0.904 1.239 1.722 c -0.134 0.818 -0.907 1.372 -1.722 1.239 c -8.073 -1.316 -14.914 0.35 -19.26 4.696 C 2.268 65.14 1.884 65.286 1.5 65.286 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(0,0,0); fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n\t<path d=\"M 61.713 51.758 c -0.384 0 -0.768 -0.146 -1.061 -0.439 L 38.685 29.351 c -0.586 -0.585 -0.586 -1.536 0 -2.121 c 0.586 -0.586 1.535 -0.586 2.121 0 l 21.968 21.968 c 0.586 0.586 0.586 1.535 0 2.121 C 62.48 51.611 62.097 51.758 61.713 51.758 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(0,0,0); fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n\t<path d=\"M 50.258 63.213 c -0.384 0 -0.768 -0.146 -1.061 -0.439 L 27.229 40.806 c -0.586 -0.585 -0.586 -1.536 0 -2.121 c 0.586 -0.586 1.535 -0.586 2.121 0 l 21.968 21.968 c 0.586 0.586 0.586 1.535 0 2.121 C 51.025 63.066 50.642 63.213 50.258 63.213 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(0,0,0); fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n\t<path d=\"M 82.111 31.79 c -0.384 0 -0.768 -0.146 -1.061 -0.439 L 58.646 8.946 c -0.586 -0.585 -0.586 -1.536 0 -2.121 c 0.586 -0.586 1.535 -0.586 2.121 0 l 22.404 22.405 c 0.586 0.585 0.586 1.536 0 2.121 C 82.879 31.644 82.495 31.79 82.111 31.79 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(0,0,0); fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n\t<path d=\"M 29.133 84.769 c -0.384 0 -0.768 -0.146 -1.061 -0.439 L 5.667 61.925 c -0.586 -0.586 -0.586 -1.535 0 -2.121 s 1.535 -0.586 2.121 0 l 22.405 22.404 c 0.586 0.586 0.586 1.535 0 2.121 C 29.9 84.622 29.517 84.769 29.133 84.769 z\" style=\"stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(0,0,0); fill-rule: nonzero; opacity: 1;\" transform=\" matrix(1 0 0 1 0 0) \" stroke-linecap=\"round\" />\r\n</g>\r\n</svg>";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.a14e165931759c58dbb3.js.map