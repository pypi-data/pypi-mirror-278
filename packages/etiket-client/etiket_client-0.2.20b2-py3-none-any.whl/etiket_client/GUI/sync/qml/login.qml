import QtQuick 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtQuick.Controls.Material 2.12

Item {
    TextField {
        id: usernameInput
        width: parent.width * 0.8
        placeholderText: "username"
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 50
        selectByMouse: true
    }

    TextField {
        id: passwordInput
        width: parent.width * 0.8
        placeholderText: "Password"
        anchors.top: usernameInput.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 10
        echoMode: TextInput.Password
        selectByMouse: true
        KeyNavigation.tab : loginBotton
    }

    Text {
        anchors.top: passwordInput.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 20
        
        id: errorLogIn
        visible : false
        color: Material.color(Material.Red, Material.Shade300)
        font.pixelSize: 12
        text: "Username or password is incorrect, please try again."
        Layout.preferredHeight: 100
        
        SequentialAnimation {
            id : errorLogInAnimation
            NumberAnimation { target: errorLogIn; property: "anchors.horizontalCenterOffset"; to: 10; duration: 60 }
            NumberAnimation { target: errorLogIn; property: "anchors.horizontalCenterOffset"; to: -10; duration: 60 }
            NumberAnimation { target: errorLogIn; property: "anchors.horizontalCenterOffset"; to: 10; duration: 60 }
            NumberAnimation { target: errorLogIn; property: "anchors.horizontalCenterOffset"; to: -10; duration: 60 }
            NumberAnimation { target: errorLogIn; property: "anchors.horizontalCenterOffset"; to: 0; duration: 30 }
        }
    }

    Button {
        id : loginBotton
        text: "Login"
        width: parent.width * 0.4
        anchors.top: errorLogIn.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 20

        Material.accent: Material.BlueGrey

        function login() {
            errorLogIn.visible = false;
            var state = loginMgr.login(usernameInput.text, passwordInput.text);
            errorLogIn.visible = !state;
            errorLogInAnimation.restart();
        }

        onClicked: loginBotton.login()
        Keys.onReturnPressed: loginBotton.login()
        Keys.onEnterPressed: loginBotton.login()
    }

    Text {
        anchors.top: loginBotton.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 30

        text: "Click here if you don't have an account."
        font.pixelSize: 12
        color: "white"
    }
}