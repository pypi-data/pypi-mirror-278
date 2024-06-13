import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtQuick.Controls.Material 2.12


ApplicationWindow {
    id: etiketApp
    height: 600
    width: 400
    visible: true
    
    title: qsTr("eTiKeT Settings Manager")

    Material.theme: Material.Dark
    Material.accent: Material.Blue

    StackView {
        id: stack
        width : parent.width
        height : parent.height
        initialItem: Loader{
            source : (loginMgr.loggedIn) ? 'settings_index.qml' : 'login.qml'
        }
        anchors.fill: parent
    }

    Connections{
        target: loginMgr
        function onLoginChanged(){
            if(loginMgr.loggedIn){
                stack.pop()
                stack.push('settings_index.qml')
            }
            else{
                stack.pop()
                stack.push('login.qml')
            }
        }
    }   
}
