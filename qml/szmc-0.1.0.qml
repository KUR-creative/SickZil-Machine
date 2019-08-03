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
    title: "SickZil-Machine 0.1.0"
    visible: true
    width: 850; height: 750
    visibility: Window.Maximized

    // STATES
    // NOTE: USE SETTERS! do not directly set state vars! 
    readonly property string start_up:  "start_up"
    readonly property string load_mask: "load_mask"
    readonly property string edit_mask: "edit_mask"
    property string state: start_up

    readonly property string pen: "pen"
    readonly property string rect: "rect"
    readonly property string panning: "panning" 
    property string prev_tool: pen // for temporary tool changing(ex: panning)
    property string tool: pen

    property bool painting: true //: pen, false: eraser

    signal changeMaskVisibility(bool is_on); 
    signal changeBrushMode(bool painting);
    signal changeTool(string new_tool);

    // setters for state vars
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
        window.prev_tool = window.tool
        window.tool = new_tool
        changeTool(new_tool)
    }

    //-------------------------------------------------------------
    MessageDialog {
        id: msgDialog
    }
    MessageDialog {
        id: imgsToProjWarnDialog
        title: "Flat Image folder -> Manga Project folder"
        text: "You have chosen a folder that contains some images.\n"
            + 'Would you like to create a "Manga project folder" with these images?'
        standardButtons: StandardButton.Yes | StandardButton.No 
        onYes: {
            main.new_project(projectOpenDialog.fileUrl)
        }
        onNo: {
            console.log("Nope")
        }
    }
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
            // if image is out of screen
            if(image.x < -image.width  + 50 ||
               image.y < -image.height + 50 || // too small x,y
               image.x > image.width   - 50 ||
               image.y > image.height  - 50 ){ // too big x,y
                // then revert dragged position
                image.x = 0; image.y = 0
            }
        }
        onWarning: {
            msgDialog.title = "project format error"
            msgDialog.text = msg;
            msgDialog.visible = true;
        }

        onImgsToProjWarning: { 
            imgsToProjWarnDialog.open()
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
    }

    //=============================================================
    FileDialog {
        id: projectOpenDialog
        selectFolder: true
        title: "Select Manga Project Folder"
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
            //---------------------------------------------
            // 'ALL' tools
            ToolButton {
                Image {
                    source: "../resource/mask_all_btn.png"
                    x:     x_all; y:      y_all
                    width: w_all; height: h_all
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: genMaskAllDialog.open()
                MessageDialog {
                    id: genMaskAllDialog
                    title: "Generate Mask All"
                    text: "It can take a long time. Would you still like "
                        + "to create a mask for all images?\n"
                        + "NOTE: All previously saved masks will be OVERWRITTEN."
                    standardButtons: StandardButton.Yes | StandardButton.No 
                    onYes: {
                        main.gen_mask_all() 
                        set_visibility(mask, true)
                    }
                }
            }
            ToolButton {
                id: rmtxt_all_btn
                Image {
                    source: "../resource/rmtxt_all_btn.png"
                    x:     x_all; y:      y_all
                    width: w_all; height: h_all
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: rmTxtAllDialog.open()
                MessageDialog {
                    id: rmTxtAllDialog
                    title: "Remove Text All"
                    text: "It can take a long time. Do you still want "
                        + "to remove the text of all images?"
                    standardButtons: StandardButton.Yes | StandardButton.No 
                    onYes: {
                        main.rm_txt_all() 
                        set_visibility(mask, false) // TODO: don't do it in startup page.
                    }
                }
            }
            //---------------------------------------------
            Rectangle { Layout.leftMargin: 3.5; width: 2; height: h_all+2; color:"gray"}
            //---------------------------------------------
            // 'single image' tools
            ToolButton {
                Image {
                    source: "../resource/mask_btn.png"
                    x:     x_one; y:      y_one
                    width: w_one; height: h_one
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: { 
                    if(mask.is_dirty){
                        genMaskDialog.open()
                    }else{
                        main.gen_mask()
                        mask.is_dirty = true
                        set_visibility(mask, true)
                    }
                }
                MessageDialog {
                    id: genMaskDialog
                    title: "Generate Mask"
                    text: "WARNING: Edited mask will be overwritten!\n"
                        + "Do you want to generate mask anyway?"
                    standardButtons: StandardButton.Yes | StandardButton.No 
                    onYes: {
                        main.gen_mask()
                        mask.is_dirty = true
                        set_visibility(mask, true)
                    }
                }
            }
            ToolButton {
                id: rm_txt_btn
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
                    set_visibility(mask, false)
                }
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
            ToolButton {
                Image {
                    id: panning_tool
                    readonly property string panning_on:  "../resource/tools/panning_on.png"
                    readonly property string panning_off: "../resource/tools/panning_off.png"
                    source: panning_off
                    x:     x_all; y:      y_all
                    width: w_all; height: h_all
                    function on()  { source = panning_on; }
                    function off() { source = panning_off; }
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: { 
                    //window.set_tool(window.panning)
                }
            }

            //---------------------------------------------
            Rectangle { Layout.leftMargin: 3.5; width: 2; height: h_all+2; color:"gray"}
            //---------------------------------------------
            ToolButton {
                Image {
                    source: "../resource/restore_btn.png"
                    x :     x_all; y:      y_all
                    width: w_all; height: h_all
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: restorePrevImgDialog.open();
                MessageDialog {
                    id: restorePrevImgDialog
                    title: "Restore Previously Saved Image"
                    text: "WARNING: Current image will be overwritten!\n"
                        + "Do you want to restore previous image anyway?"
                    standardButtons: StandardButton.Yes | StandardButton.No 
                    onYes: main.restore_prev_image();
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
                        pen_tool.on(); rect_tool.off(); panning_tool.off()
                    }else if(new_tool == window.rect){
                        pen_tool.off(); rect_tool.on(); panning_tool.off()
                    }else if(new_tool == window.panning){
                        pen_tool.off(); rect_tool.off();panning_tool.on()
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
            // gen_mask / rm_txt shortcuts
            else if(event.key == Qt.Key_Return) { rm_txt_btn.clicked() }
            // drawboard keys
            else if(event.key == Qt.Key_Plus || // Equal for convinience
                    event.key == Qt.Key_Equal) { drawboard.inc_radius() }
            else if(event.key == Qt.Key_Minus) { drawboard.dec_radius() }
            // toggle keys
            else if(event.key == Qt.Key_Space) { toggle_visibility(mask) }
            else if(event.key == Qt.Key_T)     { toggle_paint_mode(window) }
            // tools keys
            else if(event.key == Qt.Key_N) { set_tool(window.pen) }  // peN
            else if(event.key == Qt.Key_R) { set_tool(window.rect) } // Rect
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

                Rectangle { // for drag.target hack
                    id: invisible_target
                    width: 0; height: 0; visible: false;
                }
                MouseArea {
                    id: mouse_area
                    anchors.fill: parent
                    acceptedButtons: Qt.LeftButton | Qt.MiddleButton | Qt.RightButton
                    drag.target: image
                    //-------------------------------------------------------------
                    onPressed: {
                        set_visibility(mask, true)
                        window.state = window.edit_mask;
                        // mask drawing for click
                        mask.mx = mouseX
                        mask.my = mouseY
                        mask.pressed_x = mouseX
                        mask.pressed_y = mouseY
                        if(mouse.button == Qt.LeftButton &&
                           window.tool != window.panning){
                            drag.target = invisible_target
                            mask.drawing = true
                            mask.request_paint(); 
                        }else if(mouse.button == Qt.MiddleButton){
                            window.set_tool(window.panning)
                            drag.target = image
                        }else if(mouse.button == Qt.RightButton){
                            drag.target = invisible_target
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
                        if(window.tool == window.panning){
                            window.set_tool(window.prev_tool)
                        }else if(window.tool == window.rect){
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
                        if(window.tool == window.pen &&
                           mask.drawing == true) {
                            mask.request_paint(); 
                        }
                        // move cursor
                        overlay.mx = mouseX
                        overlay.my = mouseY
                        overlay.requestPaint();

                        //console.log(mouse.button, window.prev_tool, window.tool)
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
        interval: 150; running: true; repeat: true
        onTriggered: console.log("mask.is_dirty:", mask.is_dirty, "window.tool", window.tool)
    }
    */
}
