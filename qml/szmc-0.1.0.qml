// TODO: decompose it. especially, remove magic string & numbers!
// TODO: https://stackoverflow.com/questions/47891156/understanding-markdirty-in-qml
//       for performance optimization
/*
 [ALL STATES]
window.state
window.tool
window.painting
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
    title: make_title("startup-page")
    visible: true
    width: 850; height: 750
    visibility: Window.Maximized

    function make_title(projdir) {
        return main.config("program_name") 
             + " " + main.config("version") 
             + " : " + projdir
    }
    function set_title_project(projdir) {
        window.title = make_title(projdir)
    }

    function note_for_users(projdir) {
        msgDialog.title = "Note"
        msgDialog.text = "Edited images are saved \n in ["+projdir+"/images]\n\n" 
          + "You can edit masks \n in ["+projdir+"/masks] \nusing external tools.\n"
          + "\n" + "Happy SickZil!"
        msgDialog.visible = true;
    }

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
        objectName: "imgsToProjWarnDialog"
        title:main.config(objectName)["title"]
        text: main.config(objectName)["text"]
        standardButtons: StandardButton.Yes | StandardButton.No 
        onYes: {
            const projdir = main.new_project(projectOpenDialog.fileUrl);
            if(projdir) { 
                set_title_project(projdir) 
                note_for_users(projdir)
            }
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
                // then revert to dragged position
                image.x = 0; image.y = 0
            }
        }
        onWarning: {
            msgDialog.title = "project format error" // TODO: remove..
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
        objectName: "projectOpenDialog"
        selectFolder: true
        title: main.config(objectName)["title"]
        onAccepted: {
            const projdir = main.open_project(fileUrl)
            if(projdir) { 
                set_title_project(projdir) 
                note_for_users(projdir)
            }
        }
    }

    Action {
        id: openProjectAction
        objectName: "openProjectAction"
        text: main.config(objectName)["text"]
        onTriggered: projectOpenDialog.open()
    }

    menuBar: MenuBar {
        Menu {
            id: openMenu
            objectName: "openMenu"
            title: main.config(objectName)["title"]
            MenuItem { action: openProjectAction }
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
                id: gen_mask_all
                objectName: "gen_mask_all"
                tooltip: main.config(objectName)["tooltip"]
                Image {
                    id: genMaskAllBtnImg
                    objectName: "genMaskAllBtnImg"
                    source: main.config(objectName)["source"]
                    x:     x_all; y:      y_all
                    width: w_all; height: h_all
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: genMaskAllDialog.open()
                MessageDialog {
                    id: genMaskAllDialog
                    objectName: "genMaskAllDialog"
                    title:main.config(objectName)["title"]
                    text: main.config(objectName)["text"]
                    standardButtons: StandardButton.Yes | StandardButton.No 
                    onYes: {
                        main.gen_mask_all() 
                        set_visibility(mask, true)
                    }
                }
            }
            ToolButton {
                id: rmtxt_all_btn
                objectName: "rmtxt_all_btn"
                tooltip: main.config(objectName)["tooltip"]
                Image {
                    id: rmTxtAllBtnImg
                    objectName: "rmTxtAllBtnImg"
                    source: main.config(objectName)["source"]
                    x:     x_all; y:      y_all
                    width: w_all; height: h_all
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: rmTxtAllDialog.open()
                MessageDialog {
                    id: rmTxtAllDialog
                    objectName: "rmTxtAllDialog"
                    title:main.config(objectName)["title"]
                    text: main.config(objectName)["text"]
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
                id: genMaskBtn
                objectName: "genMaskBtn"
                tooltip: main.config(objectName)["tooltip"]
                Image {
                    id: genMaskBtnImg
                    objectName: "genMaskBtnImg"
                    source: main.config(objectName)["source"]
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
                    objectName: "genMaskDialog"
                    title: main.config(objectName)["title"]
                    text: main.config(objectName)["text"]
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
                objectName: "rm_txt_btn"
                tooltip: main.config(objectName)["tooltip"]
                Image {
                    id: rmTxtBtnImg
                    objectName: "rmTxtBtnImg"
                    source: main.config(objectName)["source"]
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
            // toggle buttons // TODO: change naming convention coherently
            ToolButton {
                id: maskToggleBtn
                objectName: "maskToggleBtn"
                tooltip: main.config(objectName)["tooltip"]
                Image {
                    id: mask_toggle_btn 
                    objectName: "mask_toggle_btn"
                    property bool mask_on: true
                    readonly property string on_img:  main.config(objectName)["on_img"]
                    readonly property string off_img: main.config(objectName)["off_img"]
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
                id: toggleDrawEraseBtn
                objectName: "toggleDrawEraseBtn"
                tooltip: main.config(objectName)["tooltip"]
                Image {
                    id: pen_toggle_btn
                    objectName: "pen_toggle_btn"
                    readonly property string pen:    main.config(objectName)["pen"]
                    readonly property string eraser: main.config(objectName)["eraser"]
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
                id: penToolBtn
                objectName: "penToolBtn"
                tooltip: main.config(objectName)["tooltip"]
                Image {
                    id: pen_tool
                    objectName: "pen_tool"
                    readonly property string pen_on:  main.config(objectName)["pen_on"]
                    readonly property string pen_off: main.config(objectName)["pen_off"]
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
                id: rectToolBtn
                objectName: "rectToolBtn"
                tooltip: main.config(objectName)["tooltip"]
                Image {
                    id: rect_tool
                    objectName: "rect_tool"
                    readonly property string rect_on:  main.config(objectName)["rect_on"]
                    readonly property string rect_off: main.config(objectName)["rect_off"]
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
                id: panningToolBtn
                objectName: "panningToolBtn"
                tooltip: main.config(objectName)["tooltip"]
                Image {
                    id: panning_tool
                    objectName: "panning_tool"
                    readonly property string panning_on:  main.config(objectName)["panning_on"]
                    readonly property string panning_off: main.config(objectName)["panning_off"]
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
                id: revertBtn
                objectName: "revertBtn"
                tooltip: main.config(objectName)["tooltip"]
                Image {
                    id: restoreBtnImg
                    objectName: "restoreBtnImg"
                    source: main.config(objectName)["source"]
                    x :     x_all; y:      y_all
                    width: w_all; height: h_all
                }
                Layout.preferredHeight: w_icon
                Layout.preferredWidth:  h_icon
                onClicked: restorePrevImgDialog.open();
                MessageDialog {
                    id: restorePrevImgDialog
                    objectName: "restorePrevImgDialog"
                    title:main.config(objectName)["title"]
                    text: main.config(objectName)["text"]
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
            else if(event.key == Qt.Key_Y) { // toggle Pen <-> Rect
                if(window.tool == window.pen) {
                    set_tool(window.rect) 
                }else if(window.tool == window.rect) {
                    set_tool(window.pen) 
                }
            } 
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
            objectName: "drawboard"
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
                source: main.config(objectName)["source"]

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

                    readonly property variant tool_style: main.config("toolStyle")

                    onPaint: {
                        var ctx = getContext("2d");
                        ctx.reset();
                        if(window.tool == window.pen) {
                            if(window.painting){
                                ctx.strokeStyle = tool_style["draw"]["strokeStyle"]
                                ctx.setLineDash(tool_style["draw"]["lineDash"]);
                                ctx.lineWidth = tool_style["draw"]["lineWidth"];
                            }else{
                                ctx.strokeStyle = tool_style["erase"]["strokeStyle"];
                                ctx.setLineDash(tool_style["erase"]["lineDash"]);
                                ctx.lineWidth = tool_style["erase"]["lineWidth"];
                            }

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
                                if(window.painting){
                                    ctx.strokeStyle = tool_style["draw"]["strokeStyle"]
                                    ctx.setLineDash(tool_style["draw"]["lineDash"]);
                                    ctx.lineWidth = tool_style["draw"]["lineWidth"];
                                }else{
                                    ctx.strokeStyle = tool_style["erase"]["strokeStyle"];
                                    ctx.setLineDash(tool_style["erase"]["lineDash"]);
                                    ctx.lineWidth = tool_style["erase"]["lineWidth"];
                                }

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
