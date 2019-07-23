// TODO: decompose it. especially, remove magic string & numbers!
// TODO: https://stackoverflow.com/questions/47891156/understanding-markdirty-in-qml
//       for performance optimization
/*
 [ALL STATES]
window.state
window.edit_tool
canvas.is_dirty
canvas.visible
*/

import QtQuick 2.5
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.1
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Window 2.2


ApplicationWindow {
    id: window
    visible: true
    width: 850; height: 750
    //visibility: Window.Maximized

    // STATES
    readonly property string start_up:  "start_up"
    readonly property string load_mask: "load_mask"
    readonly property string edit_mask: "edit_mask"
    property string state: start_up

    property bool painting: true //: pen, false: eraser

    signal changeMaskVisibility(bool is_on); // TODO: ~Visibility
    signal changeBrushMode(bool painting);

    function set_visibility(canvas, is_visible) {
        canvas.visible = is_visible;
        changeMaskVisibility(is_visible);
    }
    function toggle_visibility(canvas) {
        set_visibility(canvas, !(canvas.visible));
    }

    function set_paint_mode(window, is_painting) {
        window.painting = is_painting;
        changeBrushMode(is_painting);
    }
    function toggle_paint_mode(window) {
        set_paint_mode(window, !(window.painting));
    }

    //-------------------------------------------------------------
    Connections {
        target: main
        onUpdateImage: {
            im.source = "" // unload
            im.source = "image://imageUpdater/" + path
        }
        onWarning: {
            msgDialog.title = "project format error"
            msgDialog.text = msg;
            msgDialog.visible = true;
        }
        onProvideMask: {
            window.state = window.load_mask

            var old_url = canvas.imgpath
            var url = "image://maskProvider/" + path
            canvas.unloadImage(old_url)
            canvas.imgpath = url 
            canvas.loadImage(url);
        }
        onSaveMask: {
            if(canvas.is_dirty){
                canvas.save(path)
                canvas.is_dirty = false
            }
        }
        onRmtxtPreview: {
            set_visibility(canvas,false)
        }
    }

    //=============================================================
    MessageDialog {
        id: msgDialog
    }

    FileDialog {
        id: projectOpenDialog
        selectFolder: true
        onAccepted: {
            main.open_project(projectOpenDialog.fileUrl)
        }
    }

    Action {
        id: openProject
        text: "Open Manga Project Folder" 
        onTriggered: projectOpenDialog.open()
    }

    menuBar: MenuBar {
        Menu {
            title: "&Open"
            MenuItem { action: openProject }
            MenuItem { 
                text: "Open &Mask" 
            }
        }
    }

    //-------------------------------------------------------------
    readonly property double w_icon:41
    readonly property double h_icon:w_icon

    readonly property double x_one: 3.4
    readonly property double y_one: 2.5
    readonly property double w_one: 35
    readonly property double h_one: 32

    readonly property double x_all: 3.1
    readonly property double y_all: 2.5
    readonly property double w_all: 35
    readonly property double h_all: w_all

    toolBar: ToolBar {
        RowLayout {
            // TODO: Refactor: Add SzmcToolBtn type
            // TODO: add disabled icon representation.
            ToolButton {
                Image {
                    source: "../resource/mask_btn.png"
                    x:     x_one; y:      y_one
                    width: w_one; height: h_one
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: { 
                    canvas.is_dirty = true
                    main.gen_mask()
                }
            }
            ToolButton {
                Image {
                    source: "../resource/rmtxt_btn.png"
                    x:     x_one; y:      y_one
                    width: w_one; height: h_one
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: {
                    canvas.is_dirty = true
                    main.rm_txt()
                }
            }
            ToolButton {
                Image {
                    source: "../resource/mask_all_btn.png"
                    x:     x_all; y:      y_all
                    width: w_all; height: h_all
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: { }
            }
            ToolButton {
                Image {
                    source: "../resource/rmtxt_all_btn.png"
                    x:     x_all; y:      y_all
                    width: w_all; height: h_all
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: { }
            }
            // toggle buttons
            ToolButton {
                Image {
                    id: mask_toggle_btn
                    property bool mask_on: true
                    readonly property string on_img:  "../resource/mask_on.png"
                    readonly property string off_img: "../resource/mask_off.png"
                    source: mask_toggle_btn.on_img
                    x:     x_all; y:      y_all
                    width: w_all; height: h_all
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: { 
                    toggle_visibility(canvas)
                }
            }
            ToolButton {
                Image {
                    id: pen_toggle_btn
                    readonly property string pen: "../resource/pen.png"
                    readonly property string eraser: "../resource/eraser.png"
                    source: pen
                    x:     x_all; y:      y_all
                    width: w_all; height: h_all
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: { 
                    toggle_paint_mode(window)
                    var ctx = canvas.getContext("2d");
                    ctx.globalCompositeOperation = 
                        window.painting ? "source-over"
                                        : "destination-out";
                }
            }

            Connections {
                target: window
                onChangeMaskVisibility: {
                    mask_toggle_btn.source = 
                        canvas.visible ? mask_toggle_btn.on_img 
                                       : mask_toggle_btn.off_img
                    mask_toggle_btn.mask_on = !(mask_toggle_btn.mask_on);
                } 
                onChangeBrushMode: {
                    pen_toggle_btn.source =
                        painting ? pen_toggle_btn.pen 
                                 : pen_toggle_btn.eraser
                } 
            }
        }
    }
    //-------------------------------------------------------------

    RowLayout {
        anchors.fill: parent
        spacing: 6

        //-------------------------------------------------------------
        focus: true
        property bool up_pressed: false
        property bool down_pressed: false
        Keys.onPressed: {
            // TODO: if up/down key pressed in startup page, 
            // IT DELETES THIS QML FILE!!!! WTF????
            if(event.key == Qt.Key_Up)   { 
                if(up_pressed == false){ 
                    main.display_prev(); 
                }
                up_pressed = true
            }
            else if(event.key == Qt.Key_Down) { 
                if(! down_pressed){ 
                    main.display_next(); 
                }
                down_pressed = true
            }
            else if(event.key == Qt.Key_Space){ 
                toggle_visibility(canvas)
            }
        }
        Keys.onReleased: {
            if (event.key == Qt.Key_Up && (! event.isAutoRepeat)) 
            {
                up_pressed = false
            }
            else if (event.key == Qt.Key_Down && (! event.isAutoRepeat))
            {
                down_pressed = false
            }
        }
        //-------------------------------------------------------------

        ScrollView {
            objectName: "view"
            Layout.fillWidth: true
            Layout.fillHeight: true

            Image { 
                id: "im"
                objectName: "image"
                source: "../resource/startup.png"

                MouseArea {
                    id: area
                    anchors.fill: parent
                    onPressed: {
                        set_visibility(canvas, true)
                        window.state = window.edit_mask;
                        canvas.lastX = mouseX
                        canvas.lastY = mouseY
                    }

                    onPositionChanged: {
                        canvas.is_dirty = true
                        canvas.requestPaint(); // TODO: use markdirty for performance
                    }

                }

                Canvas {
                    id: canvas
                    anchors.fill: parent

                    property int lastX: 0
                    property int lastY: 0

                    property string imgpath: ""
                    property bool is_dirty: false

                    onImageLoaded: {
                        var ctx = getContext("2d");
                        ctx.clearRect(0,0, width,height)
                        ctx.drawImage(imgpath, 0, 0);
                        requestPaint();
                    }
                    onPaint: {
                        var ctx = getContext("2d");
                        ctx.globalCompositeOperation = 
                            window.state == window.load_mask ? "source-over":
                            window.painting ? "source-over"
                                            : "destination-out";
                        ctx.lineCap = 'round'
                        ctx.strokeStyle = "#FF0000"
                        ctx.lineWidth = 40;
                        ctx.beginPath();

                        ctx.moveTo(lastX, lastY);

                        lastX = area.mouseX;
                        lastY = area.mouseY;
                        ctx.lineTo(lastX,lastY);
                        ctx.stroke();
                    }
                } 
            }
        }

        ScrollView {
            Layout.fillHeight: true
            Layout.preferredWidth: 400
            horizontalScrollBarPolicy: Qt.ScrollBarAlwaysOff
            ListView {
                width: 200; height: 200
                model: ImModel    
                delegate: 
                Button {
                    width: 400
                    height: 20
                    text: image + "      " + mask
                    style: ButtonStyle {
                        background: Rectangle {
                            color: {
                                displayed ? "yellow" : "white"
                            }
                        }
                    }
                    onClicked: { 
                        main.display(index); 
                    }
                }
            }
        }
    }
    
    statusBar: StatusBar {
        RowLayout {
            anchors.fill: parent
            Label { text: "Read Only" }
        }
    }

    //=============================================================
    /*
    //for DEBUG
    Timer {
        interval: 500; running: true; repeat: true
        onTriggered: console.log("canvas.visible:", canvas.visible)
    }
    */
}
