import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtQuick.Controls.Material 2.12

import QtQuick.Dialogs 1.3

Item{
    TabBar {
        id: syncAddSourceMenu
        width: etiketApp.width-36-6
        TabButton {
            text: qsTr("qCoDes")
            font.capitalization: Font.MixedCase
        }
        TabButton {
            text: qsTr("core-tools")
            font.capitalization: Font.MixedCase
        }
        TabButton {
            text: qsTr("quantify")
            font.capitalization: Font.MixedCase
        }
    }

    FileDialog {
        id : fileDialog
        title: "Please choose a file"
        onAccepted: {
            qCoDesSyncItem.filePath = fileDialog.fileUrl.toString()
            console.log("You chose: " + fileDialog.fileUrl)
        }
        onRejected: {
            console.log("Canceled")
        }
    }
    FileDialog {
        id : folderDialog
        title: "Please choose a folder"
        selectFolder: true
        onAccepted: {
            quantifySyncItem.folder_location = folderDialog.folder.toString()
            console.log("You chose: " + folderDialog.folder)
        }
        onRejected: {
            console.log("Canceled")
        }
    }

    StackLayout {
        id : syncAddSourceStack
        anchors.top : syncAddSourceMenu.bottom
        anchors.bottom : parent.bottom
        width: etiketApp.width-36-6
        currentIndex: syncAddSourceMenu.currentIndex
        Item{
            id : qCoDesSyncItem
            width : parent.width - 30
            x : 15
            property var filePath : null
            property var errorMessage : ""
            
            ColumnLayout{
                width : parent.width
                Item{
                    height: 20
                }
                TextField {
                    id: qcodes_name_of_db
                    Layout.preferredHeight : 40
                    Layout.preferredWidth : parent.width
                    font.pixelSize : 14
                    focus : true
                    validator: RegularExpressionValidator { regularExpression: /[0-9A-Za-z _-]{3,}/ }
                    placeholderText: "Name that describes the datasource"
                }
                Item{ height: 2 }
                TextField {
                    id: qcodes_set_up
                    Layout.preferredHeight : 40
                    Layout.preferredWidth : parent.width
                    font.pixelSize : 14
                    focus : true
                    validator: RegularExpressionValidator { regularExpression: /[0-9A-Za-z _-]{1,}/ }
                    placeholderText: "set-up used for measurements"
                }

                Item{
                    Layout.preferredWidth : parent.width
                    Layout.preferredHeight : 40
                
                    Text{
                        id  : sync_to_qcodes
                        y : 11
                        text : "Sync to : "
                        font.pixelSize: 12
                        color: "white"
                    }
                    Item {
                        id : fillerScope
                        width : sync_to_qcodes.contentWidth +10
                        height : 45
                    }
                    ComboBox {
                        id : scope_selector_qcodes
                        anchors.left : fillerScope.right
                        currentIndex: sync_def_scope_model.currentIndex()
                        model: sync_def_scope_model
                        
                        width : parent.width - sync_to_qcodes.contentWidth - 10
                        height : 30+16
                        font.pixelSize: 16
                    }
                }

                Rectangle{
                    Layout.fillWidth : true
                    radius: 4
                    height : 40
                    border.width : 1
                    border.color : "gray"
                    color : "transparent"
                    RowLayout{
                        width : parent.width
                        height : 38
                        Item{width : 8}

                        Button{
                            Layout.preferredHeight : 40
                            Material.background: Material.color(Material.Red, Material.Shade400)
                            id : qcodesAddFile
                            text : "add file"
                            font.capitalization: Font.MixedCase
                            font.pixelSize : 14
                            onClicked : {
                                fileDialog.open()
                            }
                        }
                        Item{width : 2}
                        Text{
                            y : 12
                            text : (qCoDesSyncItem.filePath == null) ? "Please select a file": qCoDesSyncItem.filePath
                            Layout.fillWidth : true
                            elide : Text.ElideLeft
                            color : "white"
                        }
                        Item{width : 4}
                    }
                }
                Item{ height : 5}
                Item{
                    height : 35

                    Text{
                        visible : (qCoDesSyncItem.errorMessage == "") ? false : true
                        text :qCoDesSyncItem.errorMessage
                        color : Material.color(Material.Red, Material.Shade200)
                    }
                }
                
                Item{
                    Layout.fillWidth : true
                    Button{
                        anchors.right : parent.right
                        text : "add qCoDeS database"
                        font.pixelSize : 14
                        focus: true
                        font.capitalization: Font.MixedCase
                        Material.background: Material.color(Material.BlueGrey, Material.Shade700)
                        onClicked : {
                            qCoDesSyncItem.errorMessage = ""
                            if (!qcodes_name_of_db.acceptableInput){
                                qCoDesSyncItem.errorMessage = "Please provide a name with more than 3 characters.\n"
                                return
                            }
                            if (!qcodes_set_up.acceptableInput){
                                qCoDesSyncItem.errorMessage = "Please provide a valid set-up name (greater than 1 character).\n"
                                return
                            }
                            qCoDesSyncItem.errorMessage = sync_data_model.evaluateQCodesData(qcodes_name_of_db.text, 
                                                                    qcodes_set_up.text ,
                                                                    sync_def_scope_model.uuid_from_index(scope_selector_qcodes.currentIndex),
                                                                    qCoDesSyncItem.filePath)
                            
                            if (qCoDesSyncItem.errorMessage == ""){
                                popup.close()
                            }
                            }
                    }
                }

                }
        }
        
        Item{
            id : coreToolsSyncItem
            width : parent.width - 30
            x : 15
            property var errorMessage : ""
            
            ColumnLayout{
                width : parent.width
                Item{
                    height: 20
                }
                TextField {
                    id: core_tools_name
                    Layout.preferredHeight : 40
                    Layout.preferredWidth : parent.width
                    font.pixelSize : 14
                    focus : true
                    validator: RegularExpressionValidator { regularExpression: /[0-9A-Za-z _-]{3,}/ }
                    placeholderText: "Name that describes the datasource"
                }
                Item{ height: 2 }
                TextField {
                    id: core_tools_database
                    Layout.preferredHeight : 40
                    Layout.preferredWidth : parent.width
                    font.pixelSize : 14
                    focus : true
                    placeholderText: "Database name"
                }
                Item{ height: 2 }
                TextField {
                    id: core_tools_username
                    Layout.preferredHeight : 40
                    Layout.preferredWidth : parent.width
                    font.pixelSize : 14
                    focus : true
                    placeholderText: "Username"
                }
                Item{ height: 2 }
                TextField {
                    id: core_tools_password
                    Layout.preferredHeight : 40
                    Layout.preferredWidth : parent.width
                    font.pixelSize : 14
                    focus : true
                    placeholderText: "Password"
                    echoMode: TextInput.Password
                }
                Item{ height: 2 }
                TextField {
                    id: core_tools_port
                    Layout.preferredHeight : 40
                    Layout.preferredWidth : parent.width
                    font.pixelSize : 14
                    validator: IntValidator {bottom: 0; top: 9999;}
                    text : "5432"
                    focus : true
                    placeholderText: "Port (default value : 5432)"
                }
                Item{ height: 2 }
                TextField {
                    id: core_tools_host
                    Layout.preferredHeight : 40
                    Layout.preferredWidth : parent.width
                    font.pixelSize : 14
                    text : "localhost"
                    focus : true
                    placeholderText: "Host (default value : localhost)"
                }
                
                Item{ height : 5}
                Item{
                    height : 45
                    width : etiketApp.width-36-6-30
                    Text{
                        width : etiketApp.width-36-6-30
                        visible : (coreToolsSyncItem.errorMessage == "") ? false : true
                        text :coreToolsSyncItem.errorMessage
                        wrapMode: Text.WordWrap
                        font.pixelSize : 12
                        color : Material.color(Material.Red, Material.Shade200)
                    }
                }
                
                Item{
                    Layout.fillWidth : true
                    Button{
                        anchors.right : parent.right
                        text : "add core-tools database"
                        font.capitalization: Font.MixedCase
                        font.pixelSize : 14
                        focus: true
                        Material.background: Material.color(Material.BlueGrey, Material.Shade700)
                        onClicked : {
                            coreToolsSyncItem.errorMessage = ""
                            if (!core_tools_name.acceptableInput){
                                coreToolsSyncItem.errorMessage = "Please provide a name with more than 3 characters.\n"
                                return
                            }
                            coreToolsSyncItem.errorMessage = sync_data_model.evaluateCoreToolsData(
                                core_tools_name.text ,core_tools_database.text, core_tools_username.text,
                                core_tools_password.text, core_tools_port.text, core_tools_host.text)
                            
                            if (coreToolsSyncItem.errorMessage == ""){
                                core_tools_name.text = ""
                                core_tools_database.text = ""
                                core_tools_username.text = ""

                                core_tools_password.text = ""
                                core_tools_port.text = "5432"
                                core_tools_host.text = "localhost"

                                popup.close()
                            }
                        }
                    }
                }

                }
        }

        Item {
            id: quantifySyncItem
            width : parent.width - 30
            x : 15
            property var folder_location : null
            property var errorMessage : ""

            ColumnLayout{
                width : parent.width
                Item{
                    height: 20
                }
                TextField {
                    id: quantify_name
                    Layout.preferredHeight : 40
                    Layout.preferredWidth : parent.width
                    font.pixelSize : 14
                    focus : true
                    validator: RegularExpressionValidator { regularExpression: /[0-9A-Za-z _-]{3,}/ }
                    placeholderText: "Name describing the datasource"
                }
                Item{ height: 2 }
                TextField {
                    id: quantify_set_up
                    Layout.preferredHeight : 40
                    Layout.preferredWidth : parent.width
                    font.pixelSize : 14
                    focus : true
                    validator: RegularExpressionValidator { regularExpression: /[0-9A-Za-z _-]{1,}/ }
                    placeholderText: "set-up used for measurements"
                }

                Item{
                    Layout.preferredWidth : parent.width
                    Layout.preferredHeight : 40
                
                    Text{
                        id  : sync_to_quantify
                        y : 11
                        text : "Sync to : "
                        font.pixelSize: 12
                        color: "white"
                    }
                    Item {
                        id : fillerScope_quantify
                        width : sync_to_quantify.contentWidth +10
                        height : 45
                    }
                    ComboBox {
                        id : scope_selector_quantify
                        anchors.left : fillerScope_quantify.right
                        currentIndex: sync_def_scope_model.currentIndex()
                        model: sync_def_scope_model
                        
                        width : parent.width - sync_to_quantify.contentWidth - 10
                        height : 30+16
                        font.pixelSize: 16
                    }
                }

                Rectangle{
                    Layout.fillWidth : true
                    radius: 4
                    height : 40
                    border.width : 1
                    border.color : "gray"
                    color : "transparent"
                    RowLayout{
                        width : parent.width
                        height : 38
                        Item{width : 8}

                        Button{
                            Layout.preferredHeight : 40
                            Material.background: Material.color(Material.Red, Material.Shade400)
                            id : quantifyAddFile
                            text : "add folder"
                            font.capitalization: Font.MixedCase
                            font.pixelSize : 14
                            onClicked : {
                                folderDialog.open()
                            }
                        }
                        Item{width : 2}
                        Text{
                            y : 12
                            text : (quantifySyncItem.folder_location == null) ? "Please select a folder": quantifySyncItem.folder_location
                            Layout.fillWidth : true
                            elide : Text.ElideLeft
                            color : "white"
                        }
                        Item{width : 4}
                    }
                }
                Item{ height : 5}
                Item{
                    height : 35

                    Text{
                        visible : (quantifySyncItem.errorMessage == "") ? false : true
                        text :quantifySyncItem.errorMessage
                        color : Material.color(Material.Red, Material.Shade200)
                    }
                }
                
                Item{
                    Layout.fillWidth : true
                    Button{
                        anchors.right : parent.right
                        text : "add quantify database"
                        font.pixelSize : 14
                        focus: true
                        font.capitalization: Font.MixedCase
                        Material.background: Material.color(Material.BlueGrey, Material.Shade700)
                        onClicked : {
                            quantifySyncItem.errorMessage = ""
                            if (!quantify_name.acceptableInput){
                                quantifySyncItem.errorMessage = "Please provide a name with more than 3 characters.\n"
                                return
                            }
                            if (!quantify_set_up.acceptableInput){
                                quantifySyncItem.errorMessage = "Please provide a valid set-up name (greater than 1 character).\n"
                                return
                            }
                            quantifySyncItem.errorMessage = sync_data_model.evaluateQuantifyData(quantify_name.text, 
                                                                    quantify_set_up.text ,
                                                                    sync_def_scope_model.uuid_from_index(scope_selector_quantify.currentIndex),
                                                                    quantifySyncItem.folder_location)
                            
                            if (quantifySyncItem.errorMessage == ""){
                                popup.close()
                            }
                            }
                    }
                }

                }
        }
    }
}
