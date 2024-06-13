import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtQuick.Controls.Material 2.12


Item{
    anchors.fill : parent

    anchors.topMargin : 18
    anchors.leftMargin : 8+10
    anchors.rightMargin : 8+10
    anchors.bottomMargin : 8+10

    width : etiketApp.width - 36
    
    
    ColumnLayout{
        id : sync_list_contents
        width : parent.width
        RowLayout{
            width : parent.width
            Text{
                id : descriptionSync
                text : "Synchronisation manager"
                font.pixelSize: 20
                color: "white"
            }
            Item {
                Layout.fillWidth: true
            }
        }
        Item{
            width : sync_list_contents.width
            height:2
        }
        
        Rectangle{
            width : parent.width
            height : 1.8
        }


        ScrollView{
            id : sync_scroll
            width : sync_list_contents.width
            height : etiketApp.height - 200
            ScrollBar.vertical.policy: ScrollBar.AlwaysOn
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
            contentHeight: sync_data_model.count * 147
            clip: true
           
            ListView{
                id : sync_list
                width : sync_list_contents.width
                // height : sync_data_model.count * 147

                model : sync_data_model
                delegate : sync_data_delegate
                focus : true

                Component{
                    id : sync_data_delegate

                    
                    ColumnLayout{
                        id : syncColumn
                        width : sync_list_contents.width
                        Item{height : 5}
                        Item{
                            width: parent.width
                            height : 20

                            Rectangle {
                                y : 4
                                width: 10
                                height: 10
                                color: (status == 'pending') ? Material.color(Material.Amber) : Material.color(Material.Green)
                                radius: 180
                            }

                            Text{
                                x : 15
                                
                                text : name
                                font.pixelSize : 14
                                font.bold : true
                                color : "white"
                            }
                            
                            Text{
                                anchors.right : parent.right
                                text : "type : " + sourceType
                                font.pixelSize : 12
                                color : "white"
                            }
                        }

                        Text{
                            height : 20
                            text : "Status : " + status
                            font.pixelSize : 12
                            color : "white"
                        }

                        Text{
                            height : 20
                            text : "Number of datasets : " + total_items
                            font.pixelSize : 12
                            color : "white"
                        }
                        RowLayout{
                            Item{width : 3 }
                            Text{
                                height : 20
                                text : "Items remaining : " + item_remaining
                                font.pixelSize : 10
                                color : "white"
                            }
                        }
                        RowLayout{
                            Item{width : 3 }
                            Text{
                                height : 20
                                text : "Failed uploads : " + items_failed
                                font.pixelSize : 10
                                color : "white"
                            }
                        }
                        RowLayout{
                            Item{width : 3 }
                            Text{
                                height : 20
                            text : "Skipped uploads : " + items_skipped + " (no scope present)"
                                font.pixelSize : 10
                                color : "white"
                            }
                        }
                        Item{
                            height : 3
                        }
                        
                        Text{
                            visible : (sourceType == "Core-tools") ? true : false
                            height : 20
                            text : "Postgres database name : " + SourceInfo
                            font.pixelSize : 12
                            color : "white"
                        }

                        Text{
                            visible : (sourceType == "qCoDeS") ? true : false
                            height : 20
                            text : "Database file location : " + SourceInfo
                            font.pixelSize : 12
                            color : "white"
                        }

                        Text{
                            height : 20
                            text : "Last update : " + LastUpdate
                            font.pixelSize : 12
                            color : "white"
                        }

                        

                        Rectangle{
                            width : parent.width
                            height : 1
                            color : "gray"
                        }
                    }
                }

                
            }

            Timer {
                id: syncUpdater
                interval: 1000
                repeat: true
                running: true
                triggeredOnStart: true
                onTriggered: {
                    var currentScrollPosition = sync_list.contentY;
                    sync_data_model.update();
                    sync_list.forceLayout();
                    sync_list.contentY = currentScrollPosition;
                }
            }
        }
    }
    

    Button{
        anchors.bottom : parent.bottom
        anchors.right :  parent.right
        text : "add source"
        font.capitalization: Font.MixedCase
        onClicked : popup.open()
    }

    Button{
        anchors.bottom : parent.bottom
        anchors.left :  parent.left
        text : (sync_proc_mgr.sync_agent_state == true) ? "Kill sync" : "Start sync"
        font.capitalization: Font.MixedCase
        onClicked : (sync_proc_mgr.sync_agent_state == true) ? sync_proc_mgr.kill_sync_proc() : sync_proc_mgr.start_sync_proc()
        
    }

    Popup {
        id: popup
        x: 0
        y: 0
        padding: 3
        width: parent.width
        height: parent.height
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent
        
        Loader{source:"sync_add_new_source.qml"}
    }
}