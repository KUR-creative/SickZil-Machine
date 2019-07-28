// TODO: decompose it. especially, remove magic string & numbers!
// TODO: https://stackoverflow.com/questions/47891156/understanding-markdirty-in-qml
//       for performance optimization
/*
 [ALL STATES]
window.state
window.tool
mask.is_dirty
mask.visible
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

    readonly property string pen: "pen"
    readonly property string rect: "rect"
    property string tool: pen

    property bool painting: true //: pen, false: eraser

    signal changeMaskVisibility(bool is_on); 
    signal changeBrushMode(bool painting);
    signal changeTool(string new_tool);

    function set_visibility(mask, is_visible) {
        mask.visible = is_visible;
        changeMaskVisibility(is_visible);
    }
    function toggle_visibility(mask) {
        set_visibility(mask, !(mask.visible));
    }

    function set_paint_mode(window, is_painting) {
        window.painting = is_painting;
        changeBrushMode(is_painting);
    }
    function toggle_paint_mode(window) {
        set_paint_mode(window, !(window.painting));
    }

    function set_tool(new_tool) {
        window.tool = new_tool
        changeTool(new_tool)
    }

    //-------------------------------------------------------------
    Connections {
        target: main
        onInitialize: {
            // window.state is set 'load' when loading image
            mask.is_dirty = false;
            set_visibility(mask, true);
            set_paint_mode(window, true);
        }
        onUpdateImage: {
            image.source = "" // unload image
            image.source = "image://imageUpdater/" + path
        }
        onWarning: {
            msgDialog.title = "project format error"
            msgDialog.text = msg;
            msgDialog.visible = true;
        }
        onProvideMask: {
            window.state = window.load_mask

            var old_url = mask.imgpath
            var url = "image://maskProvider/" + path
            mask.unloadImage(old_url)
            mask.imgpath = url 
            mask.loadImage(url);
        }
        onSaveMask: {
            if(mask.is_dirty){
                mask.save(path)
                mask.is_dirty = false;
            }
        }
        onRmtxtPreview: {
            set_visibility(mask,false)
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
                    main.gen_mask()
                    mask.is_dirty = true
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
                    main.rm_txt()
                    mask.is_dirty = true
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
                    toggle_visibility(mask)
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
                    var ctx = mask.getContext("2d");
                    ctx.globalCompositeOperation = 
                        window.painting ? "source-over"
                                        : "destination-out";
                }
            }
            // tools
            ToolButton {
                Image {
                    id: pen_tool
                    readonly property string pen_on:  "../resource/tools/pen_tool_on.png"
                    readonly property string pen_off: "../resource/tools/pen_tool_off.png"
                    source: pen_on 
                    x:     x_all; y:      y_all
                    width: w_all; height: h_all
                    function on()  { source = pen_on; }
                    function off() { source = pen_off; }
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: { 
                    window.set_tool(window.pen)
                }
            }
            ToolButton {
                Image {
                    id: rect_tool
                    readonly property string rect_on:  "../resource/tools/rect_tool_on.png"
                    readonly property string rect_off: "../resource/tools/rect_tool_off.png"
                    source: rect_off
                    x:     x_all; y:      y_all
                    width: w_all; height: h_all
                    function on()  { source = rect_on; }
                    function off() { source = rect_off; }
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: { 
                    window.set_tool(window.rect)
                }
            }

            //-------------------------------------------------------------
            Connections {
                target: window
                onChangeMaskVisibility: {
                    mask_toggle_btn.source = 
                        mask.visible ? mask_toggle_btn.on_img 
                                       : mask_toggle_btn.off_img
                    mask_toggle_btn.mask_on = !(mask_toggle_btn.mask_on);
                } 
                onChangeBrushMode: {
                    pen_toggle_btn.source =
                        painting ? pen_toggle_btn.pen 
                                 : pen_toggle_btn.eraser
                } 
                onChangeTool: {
                    if(new_tool == window.pen){
                        pen_tool.on(); rect_tool.off(); 
                    }else if(new_tool == window.rect){
                        pen_tool.off(); rect_tool.on();
                    }
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
                if (! up_pressed)   { main.display_prev(); }
                up_pressed = true;
            }
            else if(event.key == Qt.Key_Down) { 
                if (! down_pressed) { main.display_next(); }
                down_pressed = true;
            }
            // drawboard keys
            else if(event.key == Qt.Key_Plus)  { drawboard.inc_radius() }
            else if(event.key == Qt.Key_Minus) { drawboard.dec_radius() }
            // toggle keys
            else if(event.key == Qt.Key_Space) { toggle_visibility(mask) }
            else if(event.key == Qt.Key_T)     { toggle_paint_mode(window) }
        }
        Keys.onReleased: {
            // to prevent image loading error
            // (caused by continuous up/down key input)
            if(! event.isAutoRepeat){
                     if (event.key == Qt.Key_Up)   { up_pressed = false }
                else if (event.key == Qt.Key_Down) { down_pressed = false }
            }
        }

        //-------------------------------------------------------------
        ScrollView {
            id: drawboard
            objectName: "view"
            Layout.fillWidth: true
            Layout.fillHeight: true

            property int brush_radius: 10
            function inc_radius(){
                brush_radius += 1;
                overlay.requestPaint();
            }
            function dec_radius(){
                brush_radius -= (brush_radius > 1 ? 1 : 0);
                overlay.requestPaint();
            }

            /*
            logical structure
            ------ overlay ----- cursor, drawing effect, etc..
            ------- mask ------- (loaded) mask
            ------- image ------ loaded manga image
            */
            Image { 
                id: image
                objectName: "image"
                source: "../resource/startup.png"

                MouseArea {
                    id: mouse_area
                    anchors.fill: parent
                    onPressed: {
                        set_visibility(mask, true)
                        window.state = window.edit_mask;
                        // mask drawing for click
                        mask.mx = mouseX
                        mask.my = mouseY
                        mask.pressed_x = mouseX
                        mask.pressed_y = mouseY
                        if(window.tool == window.pen) {
                            mask.drawing = true
                            mask.request_paint(); 
                        }
                        // overlay
                        overlay.drawing = true
                        overlay.pressed_x = mouseX
                        overlay.pressed_y = mouseY
                    }
                    onReleased: {
                        mask.drawing = false
                        mask.released_x = mouseX
                        mask.released_y = mouseY
                        if(window.tool == window.rect){
                            mask.request_paint(); 
                        }
                        // overlay
                        overlay.drawing = false
                        overlay.pressed_x = mouseX
                        overlay.pressed_y = mouseY
                        overlay.requestPaint();
                    }

                    hoverEnabled: true
                    onPositionChanged: {
                        // mask drawing for drag
                        if(window.tool == window.pen) {
                            mask.request_paint(); 
                        }
                        // move cursor
                        overlay.mx = mouseX
                        overlay.my = mouseY
                        overlay.requestPaint();
                    }
                }

                Canvas {
                    id: mask
                    anchors.fill: parent

                    property bool drawing: false
                    property int mx: 0
                    property int my: 0
                    property int pressed_x: 0
                    property int pressed_y: 0
                    property int released_x: 0
                    property int released_y: 0

                    property string imgpath: ""
                    property bool is_dirty: false
                    function request_paint(){
                        mask.is_dirty = true
                        mask.requestPaint(); // TODO: use markdirty for performance
                    }

                    onImageLoaded: {
                        var ctx = getContext("2d");
                        ctx.clearRect(0,0, width,height) // TODO: use reset?
                        ctx.drawImage(imgpath, 0, 0);
                        requestPaint();
                    }
                    onPaint: {
                        var ctx = getContext("2d");
                        ctx.globalCompositeOperation = 
                            window.state == window.load_mask ? "source-over":
                            window.painting ? "source-over"
                                            : "destination-out";
                        if(mask.drawing) {
                            ctx.lineCap = 'round'
                            ctx.strokeStyle = "#FF0000"
                            ctx.fillStyle = "#FF0000"
                            if(window.tool == window.pen) {
                                //-------------------- for click --------------------
                                ctx.beginPath(); 
                                ctx.arc(
                                    mx, my,
                                    drawboard.brush_radius,
                                    0.0, Math.PI * 2,
                                    false
                                );
                                ctx.fill();
                                ctx.closePath();
                                //---------------------------------------------------

                                //-------------------- for drag ---------------------
                                ctx.beginPath(); 
                                ctx.lineWidth = drawboard.brush_radius * 2;
                                ctx.moveTo(mx, my);
                                mx = mouse_area.mouseX; my = mouse_area.mouseY;
                                ctx.lineTo(mx,my);
                                ctx.stroke();
                                ctx.closePath();
                                //---------------------------------------------------
                            }
                        }else{
                            if(window.state == window.edit_mask &&
                               window.tool == window.rect) 
                            {
                                ctx.lineCap = 'butt'
                                ctx.fillStyle = "#FF0000"
                                ctx.beginPath(); 
                                ctx.rect(
                                    pressed_x, pressed_y,
                                    released_x - pressed_x, released_y - pressed_y
                                );
                                ctx.fill();
                                ctx.closePath();
                            }
                        }
                    }
                } 

                Canvas {
                    id: overlay
                    anchors.fill: parent

                    property bool drawing: false
                    property int mx: 0
                    property int my: 0
                    property int pressed_x: 0
                    property int pressed_y: 0
                    property int released_x: 0
                    property int released_y: 0

                    onPaint: {
                        var ctx = getContext("2d");
                        ctx.reset();
                        if(window.tool == window.pen) {
                            ctx.strokeStyle = "#008888";
                            ctx.setLineDash([3, 1]);
                            ctx.lineWidth = 1.5;

                            ctx.beginPath();
                            ctx.arc(
                                mx, my,
                                drawboard.brush_radius,
                                0.0, Math.PI * 2,
                                false
                            );
                            ctx.stroke();
                            ctx.closePath();
                        } else if(window.tool == window.rect) {
                            if(drawing){
                                ctx.strokeStyle = "#00FF00";
                                ctx.lineWidth = 1.5;

                                ctx.beginPath();
                                ctx.rect(
                                    pressed_x, pressed_y,
                                    mx - pressed_x, my - pressed_y,
                                );
                                ctx.stroke();
                                ctx.closePath();
                            }
                        }
                    }
                }
            }
        }

        //-------------------------------------------------------------
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
    
    //=============================================================
    statusBar: StatusBar {
        RowLayout {
            anchors.fill: parent
            Label { text: "Read Only" }
        }
    }

    //for DEBUG
    /*
    Timer {
        interval: 250; running: true; repeat: true
        onTriggered: console.log("canvas.is_dirty:", canvas.is_dirty)
    }
    */
}
